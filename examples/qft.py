"""Quantum Fourier Transform. (Course 2, Hours 10-11)

Builds an n-qubit QFT from scratch (Hadamards + controlled phases + swaps)
and checks it against the analytic discrete Fourier transform matrix, which
is an unambiguous ground truth (no convention guessing).

Run: uv run python examples/qft.py
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.quantum_info import Operator


def qft_circuit(n: int) -> QuantumCircuit:
    """QFT with Qiskit's little-endian qubit ordering (qubit 0 = least significant)."""
    qc = QuantumCircuit(n)
    for j in reversed(range(n)):
        qc.h(j)
        for k in reversed(range(j)):
            qc.cp(np.pi / 2 ** (j - k), k, j)
    for i in range(n // 2):
        qc.swap(i, n - 1 - i)
    return qc


def dft_matrix(n: int) -> np.ndarray:
    """Analytic DFT: F[a, b] = omega^(a*b) / sqrt(N), omega = exp(2*pi*i / N)."""
    N = 2 ** n
    omega = np.exp(2j * np.pi / N)
    return np.array([[omega ** (a * b) for b in range(N)] for a in range(N)]) / np.sqrt(N)


def matches_up_to_global_phase(u: np.ndarray, d: np.ndarray) -> bool:
    mask = np.abs(d) > 1e-9
    if not np.allclose(np.abs(u), np.abs(d)):
        return False
    ratio = u[mask] / d[mask]
    return bool(np.allclose(ratio, ratio[0]))


def main() -> None:
    n = 3
    qc = qft_circuit(n)
    print(qc.draw(output="text"))
    match = matches_up_to_global_phase(Operator(qc).data, dft_matrix(n))
    print(f"\n{n}-qubit QFT matches the analytic DFT matrix: {match}")


if __name__ == "__main__":
    main()
