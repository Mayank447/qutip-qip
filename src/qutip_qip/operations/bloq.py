import math
from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import uuid4

from qutip_qip.operations import OpInstruction
from qutip_qip.operations.conditional import Cbz, Cbnz
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
    __slots__ = (
        "_qreg_dim",
        "_aux_qreg_dim",
        "_num_creg",
        "_num_aux_creg",
        "_global_phase",
        "_op_instructions",
    )

    def __init__(
        self, num_qreg: int, num_creg: int = 0, qreg_dim: tuple[int, ...] = ()
    ) -> None:
        if num_qreg < 0:
            raise ValueError("num_qreg must be greater than or equal to 0.")

        if num_creg < 0:
            raise ValueError("num_creg must be greater than or equal to 0.")

        if len(qreg_dim) and len(qreg_dim) != num_qreg:
            raise ValueError(
                f"Lenght of qreg_dim={qreg_dim} must be equal to num_qreg={num_qreg}"
            )

        self._qreg_dim = qreg_dim
        if len(self._qreg_dim) == 0:
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
    def num_aux_qreg(self) -> int:
        return len(self._aux_qreg_dim)

    @property
    def num_creg(self) -> int:
        return self._num_creg

    @property
    def num_aux_creg(self) -> int:
        return self._num_aux_creg

    @property
    def instructions(self) -> tuple[OpInstruction, ...]:
        return tuple(self._op_instructions)

    @property
    def global_phase(self) -> float:
        return self._global_phase

    def add_global_phase(self, phase: float) -> None:
        self._global_phase += phase
        self._global_phase %= 2 * math.pi

    def add_aux_qreg(self, count: Int = 1, dim: Int = 2) -> None:
        if not (isinstance(count, Int) and count > 0):
            raise TypeError(f"count must be of type int, got {count}")

        if not (isinstance(dim, Int) and dim > 0):
            raise TypeError(f"dim must be of type int, got {dim}")

        self._aux_qreg_dim.append([dim] * count)

    def add_aux_creg(self, count: Int = 1) -> None:
        if not (isinstance(count, Int) and count > 0):
            raise TypeError(f"count must be of type int, got {count}")
        self._num_aux_creg += count

    @property
    def qreg(self) -> tuple[int, ...]:
        return tuple(range(self.num_qreg))

    @property
    def aux_qreg(self) -> tuple[int, ...]:
        return tuple(range(self.num_qreg, self.num_qreg + self.num_aux_qreg))

    @property
    def creg(self) -> tuple[int, ...]:
        return tuple(range(self.num_creg))

    @property
    def aux_creg(self) -> tuple[int, ...]:
        return tuple(range(self.num_qcreg, self.num_creg + self.num_aux_creg))

    def add_op(self, op, qreg=(), creg=()) -> None:
        # Type checking is handled internally within OpInstruction
        # We just check each element of qreg, creg are within the limit
        if isinstance(qreg, Int):
            qreg = [qreg]
        if isinstance(creg, Int):
            creg = [creg]

        check_limit("qreg", qreg, 0, self.num_qreg + self.num_aux_qreg - 1)
        check_limit("creg", creg, 0, self.num_creg + self.num_aux_creg - 1)

        self._op_instructions.append(
            OpInstruction(op=op, qreg=tuple(qreg), creg=tuple(creg))
        )

    @contextmanager
    def if_test(self, creg, value: Int) -> None:
        if type(creg) is Int:
            creg = [creg]

        # TODO test each element in creg is an int
        check_limit("creg", creg, 0, self.num_creg + self.num_aux_creg - 1)

        if (value < 0) or (value >= 2 ** len(creg)):
            raise ValueError("Check value not in the limit")

        label = uuid4().hex
        for index, cbit in enumerate(creg):
            if (value >> index) & 1 == 1:
                # If does not match for cbit_value=1, then branch to label (don't execute the conditional if)
                self.add_op(Cbz(label), creg=creg)
            else:
                # If does not match for cbit_value=0, then branch to label
                self.add_op(Cbnz(label), creg=creg)

    def build(self) -> Bloq:
        return Bloq(
            qreg_dim=self._qreg_dim,
            num_creg=self.num_creg,
            aux_qreg_dim=self._aux_qreg_dim,
            num_aux_creg=self.num_aux_qreg,
            global_phase=self.global_phase,
            instructions=self.instructions,
        )
