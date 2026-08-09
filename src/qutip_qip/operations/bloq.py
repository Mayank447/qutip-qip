import math
from contextlib import contextmanager
from dataclasses import dataclass, field
from uuid import uuid4

from qutip_qip.operations import OpInstruction


@dataclass(frozen=True, slots=True)
class Bloq:
    uuid: str = field(default_factory=lambda: uuid4().hex)
    qreg_dim: tuple[int, ...] = ()
    aux_qreg_dim: tuple[int, ...] = ()

    qreg_count: int = 0
    creg_count: int = 0
    global_phase: float = 0.0
    instructions: tuple[OpInstruction, ...] = ()

    # Op and Bloq are kept separate and qreg_dim, qreg_count, creg_count etc. have been copied here.
    # The only linking between them happens via the BloqRepository.


class BloqBuilder:
    def __init__(
        self, num_qreg: int, num_creg: int = 0, qreg_dim: tuple[int, ...] | None = None
    ) -> None:
        self._num_qreg = num_qreg
        self._num_creg = num_creg
        self._op_instructions = []
        self._global_phase = 0.0

        if (qreg_dim is not None) and (len(qreg_dim) != num_qreg):
            raise ValueError(
                f"Lenght of qreg_dim={qreg_dim} must be equal to num_qreg={num_qreg}"
            )

        if self._qreg_dim is None:
            self._qreg_dim = (2,) * num_qreg
        else:
            self._qreg_dim = tuple(qreg_dim)

    @property
    def num_qreg(self) -> int:
        return self._num_qreg

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

    def add_aux_qreg(self, count=1, dim=2) -> tuple[int, ...]: ...
    def add_op(self, op, qregs, cregs=()) -> None: ...

    @contextmanager
    def if_test(self, creg, value: int, check="EQ") -> None: ...

    def build(self) -> Bloq: ...
