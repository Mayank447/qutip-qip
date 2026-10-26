import inspect
from abc import abstractmethod
from dataclasses import MISSING, fields
from functools import cache, lru_cache
from typing import ClassVar

from qutip import Qobj
from qutip_qip.operations.gateclass import Gate, class_or_instance_method
from qutip_qip.operations.op import Op
from qutip_qip.operations.utils import controlled_gate_unitary
from qutip_qip.typing import Int


class Controlled(Op):
    """
    Abstract class for defining a Controlled Op.
    """

    config = Op.config | {"num_ctrl_qreg", "ctrl_value", "target"}
    is_controlled = True
    num_ctrl_qreg: ClassVar[int] = 1
    ctrl_value: ClassVar[int | None] = None  # None: all controls in |1>

    # Abstract class attribute i.e. subclasses need to define
    # target = RX   for example
    @property
    @abstractmethod
    def target(self) -> type[Op]: ...

    _derived = {
        "num_qreg": lambda n, t: n + t.num_qreg,
        "qreg_dim": lambda n, t: (2,) * n + t.qreg_dim,
        "num_creg": lambda n, t: t.num_creg,
        "self_inverse": lambda n, t: t.self_inverse,
    }

    def __init_subclass__(cls) -> None:
        if not inspect.isabstract(cls):
            target, num_ctrl_qreg = cls.target, cls.num_ctrl_qreg
            if not (
                isinstance(
                    target, type
                )  # It must not be an instance e.g. RX(0.5), rather the class itself
                and issubclass(target, Op)
                and not inspect.isabstract(target)
            ):
                raise TypeError(
                    f"{cls.__name__}: target must be a concrete Op, got {target!r}."
                )

            if not target.unitary:
                raise TypeError(f"{cls.__name__}: target must be unitary.")

            if not isinstance(num_ctrl_qreg) or num_ctrl_qreg < 1:
                raise ValueError(
                    f"{cls.__name__}: num_ctrl_qreg must be an integer >= 1."
                )

            if cls.ctrl_value is None:
                cls.ctrl_value = (1 << num_ctrl_qreg) - 1

            if not isinstance(cls.ctrl_value, Int) or not 0 <= cls.ctrl_value < (
                1 << num_ctrl_qreg
            ):
                raise ValueError(
                    f"{cls.__name__}: ctrl_value must be an integral in [0, 2**num_ctrl_qreg)."
                )

            for attr, rule in cls._derived.items():
                if target.is_derived:  # e.g. MCX(n)
                    setattr(
                        cls,
                        attr,
                        property(
                            lambda self, rule=rule: rule(
                                self.num_ctrl_qreg, self.target_op()
                            )
                        ),
                    )
                else:
                    setattr(cls, attr, rule(num_ctrl_qreg, target))

            # The target Op's parameters e.g. theta in RX, become parameter of the Controlled Op as well.
            cls.__annotations__ = {f.name: f.type for f in fields(target)} | vars(
                cls
            ).get("__annotations__", {})
            for f in fields(target):
                if f.default is not MISSING:
                    setattr(cls, f.name, f.default)

        super().__init_subclass__()

    def validate_params(self) -> None:
        # Run the validate_params method by buidling the target
        # For non-parametric target Op like X, validate_params is just pass be default, so it passes
        # For Parametric target Op (say RX), when we call CRX(theta), RX(theta) gets constructed which validates the params
        self.target_op()

    @class_or_instance_method
    def target_op(cls_ins) -> Op | type[Op]:
        if isinstance(cls_ins, type):
            return cls_ins.target
        return cls_ins.target(*cls_ins.params)


class ControlledGate(Controlled, Gate):
    r"""
    Abstract base class for controlled quantum gates.

    A controlled gate applies a target unitary operation only when the control
    qubits are in a specific state.

    Attributes
    ----------
    target_gate : :class:`.Gate`
        The gate to be applied to the target qubits.

    num_ctrl_qubits : int
        The number of qubits acting as controls.

    ctrl_value : int
        The decimal value of the control state required to execute the
        unitary operator on the target qubits.

        Example:
        If the gate should execute when the 0-th qubit is $|1\rangle$ set ``ctrl_value=1``.
        If the gate should execute when two control qubits are $|10\rangle$ (binary 10), set ``ctrl_value=0b10``.
    """

    __slots__ = ("_target_inst",)
    target_gate: type[Gate]

    def __init_subclass__(cls, **kwargs) -> None:
        """
        Validates the subclass definition.
        """

        super().__init_subclass__(**kwargs)
        if inspect.isabstract(cls):
            return

        # Must have a target_gate
        target_gate = getattr(cls, "target_gate", None)
        if target_gate is None or not issubclass(target_gate, Gate):
            raise TypeError(
                f"Class '{cls.__name__}' attribute 'target_gate' must be a Gate class, "
                f"got {type(target_gate)} with value {target_gate}."
            )

        # Check num_ctrl_qubits is a positive integer
        num_ctrl_qubits = getattr(cls, "num_ctrl_qubits", None)
        if (type(num_ctrl_qubits) is not int) or (num_ctrl_qubits < 1):
            raise TypeError(
                f"Class '{cls.__name__}' attribute 'num_ctrl_qubits' must be a positive integer, "
                f"got {type(num_ctrl_qubits)} with value {num_ctrl_qubits}."
            )

        # Check num_ctrl_qubits < num_qubits
        if not cls.num_ctrl_qubits < cls.num_qubits:
            raise ValueError(
                f"{cls.__name__}: 'num_ctrl_qubits' must be less than the 'num_qubits'"
            )

        # Check num_ctrl_qubits + target_gate.num_qubits = num_qubits
        if cls.num_ctrl_qubits + cls.target_gate.num_qubits != cls.num_qubits:
            raise AttributeError(
                f"'num_ctrls_qubits' {cls.num_ctrl_qubits} + 'target_gate qubits' {cls.target_gate.num_qubits} must be equal to 'num_qubits' {cls.num_qubits}"
            )
        cls._validate_control_value()

        # If the target gate is parametric e.g. RX, so is the overall controlled gate e.g. CRX
        cls.is_parametric = cls.target_gate.is_parametric

        # Default self_inverse
        # Don't replace cls.__dict__ with hasattr() that does a MRO search
        if "self_inverse" not in cls.__dict__:
            cls.self_inverse = cls.target_gate.self_inverse

        # In the circuit plot, only the target gate is shown.
        # The control has its own symbol.
        if "latex_str" not in cls.__dict__:
            cls.latex_str = cls.target_gate.latex_str

        if not cls.is_controlled:
            raise ValueError(
                f"Class '{cls.name}' method 'is_controlled' must be set to True."
            )

    def __init__(self, *args, **kwargs) -> None:
        self._target_inst = self.target_gate(*args, **kwargs)

    def __getattr__(self, name: str) -> any:
        """
        If an attribute (like 'arg_value') or method (like 'validate_params')
        isn't found on the ControlledGate, Python falls back to this method.
        We forward the request to the underlying target gate instance.
        """
        return getattr(self._target_inst, name)

    def __setattr__(self, name, value) -> None:
        """
        Intercept attribute assignment. If it's our internal storage variable,
        set it normally on this instance. Otherwise, forward the assignment
        to the underlying target gate.
        """
        if name == "_target_inst":
            super().__setattr__(name, value)
        else:
            setattr(self._target_inst, name, value)

    # Although target_gate is specified as a class attribute, It has been
    # been made an abstract method to make ControlledGate abstract (required in Metaclass)
    # This is because Python currently doesn't support abstract class attributes.
    @property
    @abstractmethod
    def target_gate() -> type[Gate]:
        pass

    @classmethod
    def _validate_control_value(cls) -> None:
        """
        Internal validation for the control value.

        Raises
        ------
        TypeError
            If ctrl_value is not an integer.
        ValueError
            If ctrl_value is negative or exceeds the maximum value
            possible for the number of control qubits ($2^N - 1$).
        """

        if type(cls.ctrl_value) is not int:
            raise TypeError(f"Control value must be an int, got {cls.ctrl_value}")

        if cls.ctrl_value < 0 or cls.ctrl_value > (1 << cls.num_ctrl_qubits) - 1:
            raise ValueError(
                f"Control value can't be negative and can't be greater than "
                f"2^num_ctrl_qubits - 1, got {cls.ctrl_value}"
            )

    @class_or_instance_method
    def get_qobj(cls_or_self, dtype: str = "dense") -> Qobj:
        """
        Construct the full Qobj representation of the controlled gate.

        Returns
        -------
        qobj : qutip.Qobj
            The unitary matrix representing the controlled operation.
        """
        if isinstance(cls_or_self, type):
            target_gate = cls_or_self.target_gate
        else:
            target_gate = cls_or_self._target_inst

        return controlled_gate_unitary(
            U=target_gate.get_qobj(dtype),
            num_controls=cls_or_self.num_ctrl_qubits,
            control_value=cls_or_self.ctrl_value,
        )

    @class_or_instance_method
    def inverse(cls_or_self) -> Gate | type[Gate]:
        if cls_or_self.self_inverse:
            inverse_gate = cls_or_self

        # Non-parametrized Gates e.g. S
        elif isinstance(cls_or_self, type):
            inverse_gate = get_controlled_gate(
                cls_or_self.target_gate.inverse(),
                cls_or_self.num_ctrl_qubits,
                cls_or_self.ctrl_value,
            )

        else:
            target_inv_inst = cls_or_self._target_inst.inverse()
            inverse_gate_class = type(target_inv_inst)
            params = target_inv_inst.arg_value

            inverse_gate = get_controlled_gate(
                inverse_gate_class,
                cls_or_self.num_ctrl_qubits,
                cls_or_self.ctrl_value,
            )(*params)

        return inverse_gate

    @classmethod
    def __str__(cls) -> str:
        return f"Gate({cls.name}, target_gate={cls.target_gate}, num_ctrl_qubits={cls.num_ctrl_qubits}, control_value={cls.ctrl_value})"

    def __eq__(self, other) -> bool:
        # Returns false for CRX(0.5), CRY(0.5)
        if type(self) is not type(other):
            return False

        # Returns false for CRX(0.5), CRX(0.6)
        if self.is_parametric and self._target_inst != other._target_inst:
            return False

        return True

    def __hash__(self) -> int:
        if self.is_parametric:
            return hash((type(self), self._target_inst))
        return hash(type(self))


def get_controlled_gate(
    gate: type[Gate],
    n_ctrl_qubits: int = 1,
    control_value: int | None = None,
    gate_name: str | None = None,
) -> ControlledGate:
    """
    Gate Factory for Controlled Gate that takes a gate and num_ctrl_qubits.
    """

    if control_value is None:
        control_value = (1 << n_ctrl_qubits) - 1

    if gate_name is None:
        gate_name = f"{'C' * n_ctrl_qubits}{gate.name}"

    class _CustomControlledGate(ControlledGate):
        __slots__ = ()
        name = gate_name
        latex_str = rf"{gate_name}"

        num_ctrl_qubits = n_ctrl_qubits
        num_qubits = n_ctrl_qubits + gate.num_qubits
        ctrl_value = control_value
        target_gate = gate

    return _CustomControlledGate
