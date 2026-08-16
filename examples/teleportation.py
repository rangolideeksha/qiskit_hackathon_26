"""Quantum teleportation. (Course 1, Hour 5)

Prepares an arbitrary state on qubit 0, teleports it to qubit 2 using an
entangled pair and two classical bits, then verifies by inverting the prep.
If teleportation is correct, qubit 2 measures '0' every time.

Run: uv run python examples/teleportation.py
"""

import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qhack import run_counts


def teleportation_circuit(theta: float = np.pi / 3) -> QuantumCircuit:
    q = QuantumRegister(3, "q")      # q0 = message, q1/q2 = entangled pair
    crz = ClassicalRegister(1, "crz")
    crx = ClassicalRegister(1, "crx")
    out = ClassicalRegister(1, "out")
    qc = QuantumCircuit(q, crz, crx, out)

    # Prepare the state to teleport on q0.
    qc.ry(theta, 0)
    qc.barrier()
    print(qc.draw(output="text"))

    # Entangle q1 and q2 (Bell pair).
    qc.h(1)
    qc.cx(1, 2)
    qc.barrier()
    print(qc.draw(output="text"))

    # Bell measurement on q0, q1.
    qc.cx(0, 1)
    qc.h(0)
    qc.measure(0, crz)
    qc.measure(1, crx)
    qc.barrier()
    print(qc.draw(output="text"))

    # Corrections on q2 conditioned on the classical bits.
    with qc.if_test((crx, 1)):
        qc.x(2)
    with qc.if_test((crz, 1)):
        qc.z(2)
    print(qc.draw(output="text"))

    # Verify: undo the prep on q2. Correct teleportation => always measures 0.
    qc.ry(-theta, 2)
    qc.measure(2, out)
    return qc


def main() -> None:
    qc = teleportation_circuit()
    counts = run_counts(qc, shots=1024)
    # 'out' is the leftmost classical register in the bitstring.
    verified = {k: v for k, v in counts.items() if k[0] == "0"}
    print("raw counts:", counts)
    print("teleport verified (out=0):", sum(verified.values()), "/ 1024")


if __name__ == "__main__":
    main()
