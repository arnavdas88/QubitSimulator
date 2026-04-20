import numpy as np
from functools import reduce

from qubitsim.base import Backend


class NumpyBackend(Backend):
    def kron(self, ops):
        return reduce(np.kron, ops)

    def dot(self, a, b):
        return a @ b

DefaultBackend = NumpyBackend