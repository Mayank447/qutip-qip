import math
from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import uuid4

from qutip_qip.operations import Op, OpInstruction
from qutip_qip.typing import Int
from qutip_qip.utils import check_limit


@dataclass(frozen=True, slots=True)
class Bloq:
    uuid: str = field(default_factory=lambda: uuid4().hex)
    qreg_dim: tuple[Int, ...] = ()
    aux_qreg_dim: tuple[Int, ...] = ()

    @property
    def num_qreg(self) -> int:
        return len(self.qreg_dim)

    @property
    def num_aux_qreg(self) -> int:
        return len(self.aux_qreg_dim)

    num_creg: Int = 0
    num_aux_creg: Int = 0
    global_phase: float = 0.0
    instructions: tuple[OpInstruction, ...] = ()

    # Op and Bloq are kept separate and qreg_dim, qreg_count, creg_count etc. have been copied here.
    # The only linking between them happens via the BloqRepository.


class BloqBuilder:
    def __init__(
        self, num_qreg: int, num_creg: int = 0, qreg_dim: tuple[int, ...] | None = None
    ) -> None:
        if num_qreg < 0:
            raise ValueError("num_qreg must be greater than or equal to 0.")

        if num_creg < 0:
            raise ValueError("num_creg must be greater than or equal to 0.")

        if qreg_dim and len(qreg_dim) != num_qreg:
            raise ValueError(
                f"Lenght of qreg_dim={qreg_dim} must be equal to num_qreg={num_qreg}"
            )

        self._qreg_dim = qreg_dim
        if self._qreg_dim is None:
            self._qreg_dim = (2,) * num_qreg

        self._aux_qreg_dim = []
        self._num_creg = num_creg
        self._num_aux_creg = 0
        self._global_phase = 0.0
        self._op_instructions = []

    @property
    def num_qreg(self) -> int:
        return len(self._qreg_dim)

    @property
    def num_creg(self) -> int:
        return self._num_creg

    @property
    def instructions(self) -> list[OpInstruction]:
        return self._op_instructions

    @property
    def global_phase(self) -> float:
        return self._global_phase

    def add_global_phase(self, phase: float) -> None:
        self._global_phase += phase
        self._global_phase %= 2 * math.pi

    def add_aux_qreg(self, count: int = 1, dim: int = 2) -> tuple[int, ...]: ...

    def add_op(self, op, qreg=(), creg=()) -> None:
        # Type checking is handled internally within OpInstruction
        # We just check each element of qreg, creg are within the limit
        if type(qreg, Int):
            qreg = [qreg]

        if type(creg, Int):
            creg = [creg]

        check_limit("qreg", qreg, 0, self.num_qreg - 1)
        check_limit("creg", creg, 0, self.num_creg - 1)

        self._op_instructions.append(
            OpInstruction(op=op, qreg=tuple(qreg), creg=tuple(creg))
        )

    @contextmanager
    def if_test(self, creg, value: int, check="EQ") -> None: ...

    def build(self) -> Bloq: ...
