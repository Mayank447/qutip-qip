************
Installation
************

.. _prerequisites:

Prerequisites
=============
This package is built upon QuTiP, of which the installation guide can be found at on `QuTiP Installation <http://qutip.org/docs/latest/installation.html>`_.
The only difference is that C++ compilers are not required here
since there is no run-time compiling for qutip-qip.


In particular, following packages are necessary for running qutip-qip

.. code-block:: bash

    numpy scipy qutip

The following to packages are used for plotting and testing:

.. code-block:: bash

    matplotlib pytest

In addition

.. code-block:: bash

    sphinx numpydoc sphinx_rtd_theme

are used to build and test the documentation.

.. _circuit_plot_packages:

Additional software for Plotting Circuits
=========================================

.. _installation:

Install qutip-qip from source code
==================================

To install the package, download to source code from `GitHub website <https://github.com/qutip/qutip-qip>`_ and run

.. code-block:: bash

    pip install .

under the directory containing the ``pyproject.toml`` file.

If you want to edit the code, use instead

.. code-block:: bash

    pip install -e .

To test the installation from a download of the source code, run from the `qutip-qip` directory

.. code-block:: bash

    pytest tests

