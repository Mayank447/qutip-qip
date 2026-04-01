# qutip-qip

[![Tests](https://github.com/qutip/qutip-qip/actions/workflows/test.yml/badge.svg?branch=master)](https://github.com/qutip/qutip-qip/actions/workflows/test.yml)
[![Documentation Status](https://readthedocs.org/projects/qutip-qip/badge/?version=latest)](https://qutip-qip.readthedocs.io/en/latest/)
[![Coverage Status](https://coveralls.io/repos/github/qutip/qutip-qip/badge.svg)](https://coveralls.io/github/qutip/qutip-qip)
[![Maintainability](https://qlty.sh/gh/qutip/projects/qutip-qip/maintainability.svg)](https://qlty.sh/gh/qutip/projects/qutip-qip)
[![PyPI version](https://badge.fury.io/py/qutip-qip.svg)](https://badge.fury.io/py/qutip-qip)
[![DOI](https://img.shields.io/badge/DOI-10.22331%2Fq--2022--01--24--630-blue.svg)](https://doi.org/10.22331/q-2022-01-24-630)
![Python Version](https://img.shields.io/pypi/pyversions/qutip-qip)
[![license](https://img.shields.io/badge/license-New%20BSD-blue.svg)](http://en.wikipedia.org/wiki/BSD_licenses#3-clause_license_.28.22Revised_BSD_License.22.2C_.22New_BSD_License.22.2C_or_.22Modified_BSD_License.22.29)

The qutip-qip is the QuTiP family package for Quantum Information Processing.
Compared to other libraries for quantum information processing, qutip-qip puts additional emphasis on the physics layer and the interaction with the QuTiP package.

The package offers two different approaches for simulating Quantum Circuits, one with calculating unitary evolution under quantum gates by matrix product. Another with `Processor` using open system solvers in QuTiP to simulate Quantum Circuit on noisy quantum devices like Super Conducting Qubits, Spin Chains etc. at a Pulse level.


## Quick start

To install the package, use

```bash
pip install qutip-qip
```

```python
from qutip_qip.circuit import QubitCircuit
from qutip_qip.operations.gates import H, CX

qc = QubitCircuit(2)
qc.add_gate(H, 0)
qc.add_gate(CX, 0, 1)
qc.draw()
```

This simple example creates an entangled state known as a Bell state.

```python
import qutip
from qutip_qip.device import SCQubits

processor = SCQubits(num_qubits=2)
processor.load_circuit(qc)
init_state = qutip.basis([3, 3], [0, 0])
result = processor.run_state(init_state)
```


## Documentation and tutorials

The documentation and tutorials for `qutip-qip` can be found at [qutip-qip.readthedocs.io/](https://qutip-qip.readthedocs.io/en/stable/).

Code examples used in the publication [*Pulse-level noisy quantum circuits with QuTiP*](https://quantum-journal.org/papers/q-2022-01-24-630), updated for the latest code version can be found in the [pulse-paper](https://github.com/qutip/qutip-qip/tree/master/pulse-paper) folder.


## Migrating from qutip.qip

The `qutip-qip` package was previosuly a module ``qutip.qip`` under [QuTiP (Quantum Toolbox in Python)](http://qutip.org/index.html). From QuTiP 5.0, the community decided to decrease the size of the core QuTiP package, in order to simplify maintenance and for the sub-packages to evolve more quickly. If you were using the `qutip` package and now want to try out the new features included in this package, you can simply install this package and replace all the `qutip.qip` in your import statement with `qutip_qip`. Everything should work smoothly as usual.


## Installation from source

which makes sure that you are up to date with the latest `pip` version. Contribution guidelines are available [*here*](https://qutip-qip.readthedocs.io/en/latest/contribution-code.html).

## Testing

To test the installation, choose the correct branch that matches with the version, e.g., `qutip-qip-0.2.X` for version 0.2. Then download the source code and run from the `qutip-qip` directory

If you would like to know the future development plan and ideas, have a look at the [Discussion panel](https://github.com/qutip/qutip-qip/discussions) as well as the [qutip documentation for ideas](https://qutip.readthedocs.io/en/stable/development/ideas.html).

```
pytest tests
```

## Community

This project and everyone participating in it are governed by the [Code of Conduct](https://github.com/qutip/qutip-qip/blob/master/CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

### Questions and Discussions
You can ask questions or answer other users' questions on our [Discussion Forum](https://github.com/qutip/qutip-qip/discussions) on GitHub or in the [QuTiP Discussion group](https://groups.google.com/forum/#!forum/qutip). You may also suggest new features or improvements you would like to see in the project. We encourage you to engage with the community and share your ideas and knowledge.

### Reporting Bugs/Issues
If you find a bug or issue, it is best to first search the existing [Issue](https://github.com/qutip/qutip-qip/issues) list. If you don't find a related issue, please report the bug by opening a new issue:

- Create a new [Issue](https://github.com/qutip/qutip-qip/issues/new) on GitHub.
- Provide as much context as you can about what you're running into.
- Provide the python and package versions by running `qutip.about()` command.

We will then take care of the issue as soon as possible.

### Contributing
If you'd like to contribute to `qutip-qip`, please take a look at the [CONTRIBUTING.md](https://github.com/qutip/qutip-qip/blob/master/CONTRIBUTING.md) file.


## Citing qutip-qip

If you use `qutip-qip` in your research, please cite this [paper](https://quantum-journal.org/papers/q-2022-01-24-630). The BibTeX file can found [here](https://github.com/qutip/qutip-qip/tree/master/doc/source/qutip_qip.bib).


## Support

[![Powered by NumFOCUS](https://img.shields.io/badge/powered%20by-NumFOCUS-orange.svg?style=flat&colorA=E1523D&colorB=007D8A)](https://numfocus.org)
[![Unitary Fund](https://img.shields.io/badge/Supported%20By-UNITARY%20FUND-brightgreen.svg?style=flat)](https://unitary.fund)

This package is supported and maintained by the same developers group as QuTiP.

QuTiP development is supported by [Nori's lab](http://dml.riken.jp/) at RIKEN, by the University of Sherbrooke, by Chalmers University of Technology, by Macquarie University and by Aberystwyth University, [among other supporting organizations](http://qutip.org/#supporting-organizations).
