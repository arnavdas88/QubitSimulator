from qubitsim.core import QuantumCircuit
from qubitsim.qasm import parse_qasm


def circ1():
    qc = QuantumCircuit(2)

    qc.h(0)
    qc.cx(0, 1)

    state = qc.run()
    print("State:", state)

    result, probs = qc.measure()
    print("Measurement:", result)
    print("Probabilities:", probs)

def circ2(decompose = True):
    qc = QuantumCircuit(3)

    qc.x(0)
    qc.x(1)

    qc.ccx(0, 1, 2, decomposition=decompose)

    state = qc.run()
    print("State:", state)

    result, probs = qc.measure()
    print("Measurement:", result)
    print("Probabilities:", probs)


def circ3():
    qc = parse_qasm("./sample.qasm", None)

    state = qc.run()
    print("State:", state)

    result, probs = qc.measure()
    print("Measurement:", result)
    print("Probabilities:", probs)

if __name__ == "__main__":
    circ1()
    circ2(True)
    circ2(False)
    circ3()
    