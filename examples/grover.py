"""Grover's search. (Course 2, Hour 14)

Searches an unstructured 3-qubit space for a marked item using an oracle
and the diffusion operator, with the optimal number of iterations.

Run: uv run python examples/grover.py
"""

import math
from qiskit import QuantumCircuit
from qhack import run_counts


def phase_oracle(marked: str) -> QuantumCircuit:
    """Flip the phase of the |marked> basis state (bitstring, e.g. '101')."""
    n = len(marked)
    qc = QuantumCircuit(n)
    # Map marked state to all-ones so a multi-controlled Z hits it.
    for i, bit in enumerate(reversed(marked)):
        if bit == "0":
            qc.x(i)
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    for i, bit in enumerate(reversed(marked)):
        if bit == "0":
            qc.x(i)
    return qc


def diffuser(n: int) -> QuantumCircuit:
    qc = QuantumCircuit(n)
    qc.h(range(n))
    qc.x(range(n))
    qc.h(n - 1)
    qc.mcx(list(range(n - 1)), n - 1)
    qc.h(n - 1)
    qc.x(range(n))
    qc.h(range(n))
    return qc


def grover_circuit(marked: str) -> QuantumCircuit:
    n = len(marked)
    iterations = max(1, round(math.pi / 4 * math.sqrt(2 ** n)))
    qc = QuantumCircuit(n, n)
    qc.h(range(n))
    for _ in range(iterations):
        qc.compose(phase_oracle(marked), inplace=True)
        qc.compose(diffuser(n), inplace=True)
    qc.measure(range(n), range(n))
    return qc


def main() -> None:
    marked = "101"
    counts = run_counts(grover_circuit(marked), shots=1024)
    top = max(counts, key=counts.get)
    print("counts:", counts)
    print(f"marked={marked}  found={top}  success={'yes' if top == marked else 'no'}")


if __name__ == "__main__":
    main()
