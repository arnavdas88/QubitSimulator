import numpy as np

from qubitsim.base import QuantumGate
from qubitsim.utils import controlled_gate, expand_single_qubit


class XGate(QuantumGate):
    def get_unitary(self, n):
        return expand_single_qubit(self.targets[0], n, np.array([[0,1],[1,0]], dtype=complex))


class HGate(QuantumGate):
    def get_unitary(self, n):
        H = (1/np.sqrt(2))*np.array([[1,1],[1,-1]], dtype=complex)
        return expand_single_qubit(self.targets[0], n, H)


class ZGate(QuantumGate):
    def get_unitary(self, n):
        Z = np.array([[1,0],[0,-1]], dtype=complex)
        return expand_single_qubit(self.targets[0], n, Z)


class CXGate(QuantumGate):
    def __init__(self, control, target):
        super().__init__((control, target))

    def get_unitary(self, n):
        return controlled_gate(self.targets[0], self.targets[1], n)


class IGate(QuantumGate):
    def __init__(self, target):
        super().__init__((target,))

    def get_unitary(self, n):
        return np.eye(2**n, dtype=complex)

class ToffoliGate(QuantumGate):
    def __init__(self, control1, control2, target):
        super().__init__((control1, control2, target))

    def get_unitary(self, n):
        dim = 2**n
        U = np.zeros((dim, dim), dtype=complex)

        for i in range(dim):
            bits = list(format(i, f'0{n}b'))

            # both controls must be 1
            if bits[self.targets[0]] == '1' and bits[self.targets[1]] == '1':
                flipped = bits.copy()
                t = self.targets[2]
                flipped[t] = '1' if bits[t] == '0' else '0'
                j = int("".join(flipped), 2)
                U[j, i] = 1
            else:
                U[i, i] = 1

        return U