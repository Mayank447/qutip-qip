from contextlib import contextmanager
from dataclasses import dataclass
from qutip_qip.operations import OpInstruction


@dataclass(frozen=True)
class Bloq:
    qreg_dim: tuple[int, ...]
    aux_qreg_dim: tuple[int, ...] = ()

    qreg_count: int
    creg_count: int
    instructions: tuple[OpInstruction, ...]

    # qreg_dim, qreg_count, creg_count etc. has been copied here, although
    # these we can directly access from the associated Op, so that Op and Bloq remain separate
    # The only linking between them happens via the BloqRepository.


class BloqBuilder:
    def add_aux_qreg(self, count=1, dim=2) -> tuple[int, ...]: ...
    def add_op(self, op, qregs, cregs=()) -> None: ...

    @contextmanager
    def if_test(self, creg, value: int, check="EQ") -> None: ...
