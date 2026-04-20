import numpy as np

from qubitsim.backend import NumpyBackend
from qubitsim.gates import CXGate, HGate, IGate, ToffoliGate, XGate, ZGate


class Moment:
    def __init__(self, n_qubits):
        self.n_qubits = n_qubits
        self.gates = [None] * n_qubits

    def add_gate(self, gate):
        for t in gate.targets:
            self.gates[t] = gate

    def finalize(self):
        # Fill empty with Identity
        for i in range(self.n_qubits):
            if self.gates[i] is None:
                self.gates[i] = IGate(i)

    def build_unitary(self, backend):
        self.finalize()
        ops = []
        used = set()

        for i in range(self.n_qubits):
            if i in used:
                continue

            gate = self.gates[i]

            # Multi-qubit gate (e.g., CX, CCX)
            if len(gate.targets) > 1:
                U = gate.get_unitary(self.n_qubits)
                return U  # already full operator

            # Single qubit
            ops.append(gate.get_unitary(1))
            used.add(i)

        return backend.kron(ops)


class OperatorFlow:
    def __init__(self):
        self.stack = []

    def push(self, moment):
        self.stack.append(moment)

    def execute(self, state, backend, n_qubits):
        U_total = np.eye(2**n_qubits, dtype=complex)

        # Reverse order (QuDiet style)
        for moment in reversed(self.stack):
            U = moment.build_unitary(backend)
            U_total = backend.dot(U, U_total)

        return backend.dot(U_total, state)


class QuantumCircuit:
    def __init__(self, n_qubits, backend=None):
        self.n_qubits = n_qubits
        self.backend = backend or NumpyBackend()
        self.flow = OperatorFlow()

        # Initialize |0...0>
        self.state = np.zeros(2**n_qubits, dtype=complex)
        self.state[0] = 1

    def h(self, q):
        m = Moment(self.n_qubits)
        m.add_gate(HGate((q,)))
        self.flow.push(m)

    def x(self, q):
        m = Moment(self.n_qubits)
        m.add_gate(XGate((q,)))
        self.flow.push(m)

    def z(self, q):
        m = Moment(self.n_qubits)
        m.add_gate(ZGate((q,)))
        self.flow.push(m)

    def cx(self, control, target):
        m = Moment(self.n_qubits)
        m.add_gate(CXGate(control, target))
        self.flow.push(m)

    def ccx(self, c1, c2, target, decomposition = False):
        if decomposition:
            # decomposition (simple version)
            self.cx(c2, target)
            self.cx(c1, target)
        else:
            m = Moment(self.n_qubits)
            m.add_gate(ToffoliGate(c1, c2, target))
            self.flow.push(m)

    def run(self):
        self.state = self.flow.execute(self.state, self.backend, self.n_qubits)
        return self.state

    def measure(self):
        probs = np.abs(self.state)**2
        outcome = np.random.choice(len(probs), p=probs)
        return format(outcome, f'0{self.n_qubits}b'), probs