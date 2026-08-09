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

    # qreg_dim, qreg_count, creg_count etc. has been copied here, although these
    # can be directly access from the associated Op, they are separate so that Op and Bloq
    # remain separate. The only linking between them happens via the BloqRepository.


class BloqBuilder:
    def __init__(self, num_qreg: int, num_creg: int = 0) -> None:
        self.num_qreg = num_qreg
        self.num_creg = num_creg

    def add_aux_qreg(self, count=1, dim=2) -> tuple[int, ...]: ...
    def add_op(self, op, qregs, cregs=()) -> None: ...

    @contextmanager
    def if_test(self, creg, value: int, check="EQ") -> None: ...

    def add_global_phase(self, phase: float) -> None: ...

    def build(self) -> Bloq: ...
