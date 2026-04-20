class Backend:
    def kron(self, ops):
        raise NotImplementedError

    def dot(self, a, b):
        raise NotImplementedError

class QuantumGate:
    def __init__(self, targets):
        self.targets = targets  # tuple of qubit indices

    def get_unitary(self, n_qubits):
        raise NotImplementedError