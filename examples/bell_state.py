"""Bell state — the simplest entanglement demo. (Course 1, Hour 4)

Run: uv run python examples/bell_state.py
Expect roughly 50/50 over '00' and '11', and never '01' or '10'.
"""

from qiskit import QuantumCircuit
from qhack import run_counts


def bell_circuit() -> QuantumCircuit:
    qc = QuantumCircuit(2, 2)
    qc.h(0)
    qc.cx(0, 1)
    qc.measure([0, 1], [0, 1])
    return qc


def main() -> None:
    qc = bell_circuit()
    print(qc.draw(output="text"))
    counts = run_counts(qc, shots=1024)
    print("counts:", counts)


if __name__ == "__main__":
    main()
