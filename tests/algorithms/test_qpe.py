import unittest
import numpy as np
from numpy.testing import assert_, assert_equal
from qutip import Qobj, sigmaz, tensor

from qutip_qip.operations import Controlled, get_unitary_gate
from qutip_qip.operations import gates as std
