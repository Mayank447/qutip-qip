from dataclasses import dataclass, field
from typing import Generic, TypeVar

# TODO: Add typing bound constraint to this
P = TypeVar("P")


@dataclass(frozen=True, slots=True)
class Op:
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
        pass

    def __str__(self):
        print(f"op={self.op}, qreg={self.qreg}, creg={self.creg}, style({self.style})")
