from dataclasses import dataclass, field
from typing import Generic, TypeVar
from uuid import uuid4

from qutip_qip.typing import Int
from qutip_qip.utils import convert_type_input_to_sequence

# TODO: Add typing bound constraint to this
P = TypeVar("P")


@dataclass(frozen=True, slots=True)
class Op:
    uuid: str = field(default_factory=lambda: uuid4().hex)
    _name: str
    params: tuple[P, ...] = ()

    @property
    def name(self) -> str:  # e.g. "MultiSWAP(3)" for drawing
        if not self.params:
            return self._name
        else:
            return f"{self._name}({', '.join(map(str, self.params))})"

    creg_count: int = 0
    qreg_dim: tuple[int, ...] = ()

    @property
    def qreg_count(self) -> int:
        return len(self.qreg_dim)

    unitary: bool = True
    self_inverse: bool = False


# Think of Parametric Op as Op Factory, takes params and returns a Op
# TODO: Update this typing when updating min Python version to 3.12
class ParametricOp(Generic[P]):
    def __call__(self, *params) -> Op: ...
    def validate_params(self, *params: P) -> None: ...


# Class to keep track of this Op on this qubit, cbit
@dataclass(frozen=True, slots=True)
class OpInstruction:
    op: Op
    qreg: tuple[int, ...] = tuple()
    creg: tuple[int, ...] = tuple()
    style: dict = field(default_factory=dict)  # For circuit draw

    def __post_init__(self):
        if not (isinstance(self.op, Op) or issubclass(self.op, Op)):
            raise TypeError("op must be a subclass or instance of type Op")

        convert_type_input_to_sequence(self.qreg, "qreg", Int)
        convert_type_input_to_sequence(self.creg, "creg", Int)
