import numpy as np
from functools import reduce


def expand_single_qubit(target, n, gate):
    I = np.eye(2)
    ops = []
    for i in range(n):
        ops.append(gate if i == target else I)
    return reduce(np.kron, ops)


def controlled_gate(control, target, n):
    dim = 2**n
    U = np.zeros((dim, dim), dtype=complex)

    for i in range(dim):
        bits = list(format(i, f'0{n}b'))

        if bits[control] == '1':
            flipped = bits.copy()
            flipped[target] = '1' if bits[target] == '0' else '0'
            j = int("".join(flipped), 2)
            U[j, i] = 1
        else:
            U[i, i] = 1

    return U

def bin_to_Nbase(target, base=2):
    if isinstance(base, int):
        base = [base] * len(target)
    else:
        assert len(target) == len(base)

    # base[0] = 1 # Anything to the power of 0 is 1
    scale = np.array(base[::-1]).cumprod()
    scale = [1, *scale[:-1]]
    return np.sum(scale[::-1] * np.array(target))


def Nbase_to_bin(_repr, base=[2]):
    base = base[::-1]
    digits = []
    while _repr:
        _base = base[len(digits)]
        digits += [int(_repr % _base)]
        _repr //= _base
    if len(digits) < len(base):
        digits += [
            0,
        ] * (len(base) - len(digits))
    return digits[::-1]