.. _introduction:

************
Introduction
************

The qutip-qip package
=====================

The qutip-qip is a QuTiP family package for Quantum Information Processing. 
Compared to other libraries for quantum information processing, qutip-qip puts additional emphasis on the physics layer and the interaction with the QuTiP package.
It offers two different approaches for simulating quantum circuits, one with :class:`.QubitCircuit` calculating unitary evolution under quantum gates by matrix product, 
another by system solvers in QuTiP to simulate a Quantum circuits on a noisy quantum device like Super Conducting Qubits, Spin Chains etc. on a Pulse level.


.. _quickstart:

Installation
============
The minimal Python version supported is Python 3.10. To install the package ``qutip-qip`` from PyPI, use

.. code-block:: bash

    pip install qutip-qip


Quick start
===========
.. code-block:: python

    from qutip_qip.circuit import QubitCircuit
    from qutip_qip.operations import H, CX

    qc = QubitCircuit(2)
    qc.add_gate(H, 0)
    qc.add_gate(CX, 0, 1)
    qc.draw()

This simple example creates an entangled state known as a Bell state.


Migrating from ``qutip.qip``
============================

The qutip-qip package used to be a module ``qutip.qip`` under `QuTiP (Quantum Toolbox in Python) <http://qutip.org/index.html>`_.
From QuTiP 5.0, in order to simplify maintenance and several QuTiP modules became QuTiP family packages.
These are maintained by the QuTiP team but hosted under different repositories in the `QuTiP organization <https://github.com/qutip>`_.
If you were using the ``qutip`` package (v4 or earlier) and now want to try out the new features included in this package, 
you can simply install this package and replace all the ``qutip.qip`` in your import statement with ``qutip_qip``.


Citing
===========

If you use ``qutip-qip`` in your research, please cite the `article <https://quantum-journal.org/papers/q-2022-01-24-630>`_
as

.. code-block:: text

    Boxi Li, Shahnawaz Ahmed, Sidhant Saraogi, Neill Lambert, Franco Nori, Alexander Pitchford, & Nathan Shammah. (2022). Pulse-level noisy quantum circuits with QuTiP. Quantum, 6, 630.

The bibtex can be downloaded directly :download:`here<qutip_qip.bib>` or
copy-pasted using :

.. code-block:: text

    @article{Li2022pulselevelnoisy,
        doi = {10.22331/q-2022-01-24-630},
        url = {https://doi.org/10.22331/q-2022-01-24-630},
        title = {Pulse-level noisy quantum circuits with {Q}u{T}i{P}},
        author = {Li, Boxi and Ahmed, Shahnawaz and Saraogi, Sidhant and Lambert, Neill and Nori, Franco and Pitchford, Alexander and Shammah, Nathan},
        journal = {{Quantum}},
        issn = {2521-327X},
        publisher = {{Verein zur F{\"{o}}rderung des Open Access Publizierens in den Quantenwissenschaften}},
        volume = {6},
        pages = {630},
        month = jan,
        year = {2022}
    }
