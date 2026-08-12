"""Deutsch-Jozsa. (Course 2, Hour 9)

Decides whether an oracle is constant or balanced in a single query.
All-zeros measurement => constant; anything else => balanced.

Run: uv run python examples/deutsch_jozsa.py
"""

from qiskit import QuantumCircuit
from qhack import run_counts


def dj_oracle(kind: str, n: int) -> QuantumCircuit:
    """Build an n-qubit oracle acting on n input qubits + 1 output qubit."""
    oracle = QuantumCircuit(n + 1)
    if kind == "constant":
        # f(x) = 0 (identity) or f(x) = 1 (flip output). Pick f(x)=1.
        oracle.x(n)
    elif kind == "balanced":
        # Balanced: XOR of all input bits onto the output qubit.
        for q in range(n):
            oracle.cx(q, n)
    else:
        raise ValueError("kind must be 'constant' or 'balanced'")
    return oracle


def dj_circuit(kind: str, n: int = 3) -> QuantumCircuit:
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(dj_oracle(kind, n), inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def main() -> None:
    for kind in ("constant", "balanced"):
        counts = run_counts(dj_circuit(kind, n=3), shots=1024)
        top = max(counts, key=counts.get)
        verdict = "constant" if top == "000" else "balanced"
        print(f"oracle={kind:9s} -> measured {top} -> decided {verdict}")


if __name__ == "__main__":
    main()
