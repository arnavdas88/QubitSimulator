import re
import warnings

from qubitsim.base import Backend
from qubitsim.core import QuantumCircuit
from qubitsim.backend import DefaultBackend


def parse_qasm(filename: str, backend: Backend = None):
    with open(filename, "r") as f:
        _data = f.read()
    return circuit_from_qasm(_data, backend)


def circuit_from_qasm(_data, backend: Backend = None):
    _data = re.sub(r"\.qubit (\d+)", r".qubit \1", _data)
    _data = re.sub(r"\.qubit (\d+)", r".qubit \1", _data)
    _data = re.split("\n\.(qubit\s\d+|begin|end)", _data)
    _data.pop(6)
    _data.pop(5)
    _data.pop(3)
    _data.pop(1)
    _data.pop(0)

    _data[0] = re.sub(r"qubit x(\d+)", r"qubit x\1 (2)", _data[0])

    _qregs = [ "".join(x.split("#")[0]) for x in _data[0].split("\n") ] 
    _qregs = [_qreg for _qreg in _qregs if _qreg]

    # _qregs = [
    #     int(re.findall("\d+", _dims)[0]) for _dims in re.findall("\d+\)", _data[0])
    # ]

    if backend is None:
        backend = DefaultBackend()

    _gates = list(filter(None, _data[1].split("\n")))
    _found_tofs = list(filter(lambda s: re.match("^Toffoli", s), _gates))


    # Toffoli gates in the below code forces the dimension of the qubit to auto-update,
    # that may not be a desirable behaviour. 
    if _found_tofs:
        warnings.warn("Toffoli circuits may result in unexpected behaviour.")
    #     _toffolis = list(
    #         map(
    #             int,
    #             set(
    #                 (
    #                     re.sub(
    #                         r"Toffoli x\d+[, ]+x(\d+)[, ]+x\d+",
    #                         r"\1",
    #                         ";".join(_found_tofs),
    #                     )
    #                 ).split(";")
    #             ),
    #         )
    #     )

    #     _qregs = [
    #         _element + 1 if _index in _toffolis else _element
    #         for _index, _element in enumerate(_qregs)
    #     ]
    qc = QuantumCircuit(len(_qregs), backend=backend)

    for _gate in _gates:
        if re.search("^X", _gate) or (
            re.search("^RX", _gate) and re.search("180$", _gate)
        ):
            _gate_qreg = int(re.findall("\d+", _gate.split()[1])[0])
            qc.x(_gate_qreg)

        elif re.search("^H", _gate):
            _gate_qreg = int(re.findall("\d+", _gate.split()[1])[0])
            qc.h(_gate_qreg)

        elif re.search("^Z", _gate):
            _gate_qreg = int(re.findall("\d+", _gate.split()[1])[0])
            qc.z(_gate_qreg)

        elif re.search("^CX", _gate) or re.search("^CNOT", _gate):
            _control = int(re.findall("\d+", _gate.split()[1])[0])
            _target = int(re.findall("\d+", _gate.split()[2])[0])

            qc.cx(control=_control, target=_target)

        elif re.search("^Toffoli", _gate):
            ints = list(map(int, re.findall("\d+", _gate)))
            # _gate_qreg = (ints[:-1], ints[-1])
            # qc.toffoli(_gate_qreg, _plus)
            qc.ccx(*ints)

    qc.measure()

    return qc