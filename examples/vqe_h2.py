"""VQE for the H2 ground-state energy. (Hackathon core algorithm)

This is the whole idea behind "quantum-accelerated catalyst design": the useful
number for chemistry is a molecule's ground-state energy, and VQE estimates it by
minimizing <psi(theta)|H|psi(theta)> over a parameterized circuit.

Pipeline (the transferable part):
    1. molecular Hamiltonian -> qubit Hamiltonian (sum of Pauli strings)
    2. ansatz: a parameterized state-prep circuit |psi(theta)>
    3. Estimator: measures the energy expectation value for given theta
    4. classical optimizer: adjusts theta to push the energy down

Here H2 is hard-coded (STO-3G, parity mapping + 2-qubit reduction, R=0.735 A) so it
runs with core deps only. For real molecules you generate H with Qiskit Nature
(see docs/vqe_and_hardware.md) -- the four steps above are identical.

Run: uv run python examples/vqe_h2.py
Expect total energy ~ -1.1373 Ha (literature equilibrium value).
"""

import numpy as np
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp
from qiskit.primitives import StatevectorEstimator
from scipy.optimize import minimize

# Electronic Hamiltonian as a weighted sum of Pauli strings.
H = SparsePauliOp(
    ["II", "IZ", "ZI", "ZZ", "XX"],
    coeffs=[-1.05237325, 0.39793742, -0.39793742, -0.0112801, 0.1809312],
)
# Constant nuclear-repulsion energy added back at the end (Z_A Z_B / R).
NUCLEAR_REPULSION = 0.7199689


def hardware_efficient_ansatz() -> QuantumCircuit:
    """A transparent 4-parameter ansatz: RY layer, entangle, RY layer.

    "Hardware-efficient" = built from the gates a device runs natively, cheap in
    depth. The alternative (UCCSD) is chemistry-motivated but deeper -- the
    depth-vs-accuracy trade-off is a real decision on NISQ hardware like AQT.
    """
    theta = ParameterVector("theta", 4)
    qc = QuantumCircuit(2)
    qc.ry(theta[0], 0)
    qc.ry(theta[1], 1)
    qc.cx(0, 1)
    qc.ry(theta[2], 0)
    qc.ry(theta[3], 1)
    return qc


def main() -> None:
    ansatz = hardware_efficient_ansatz()
    estimator = StatevectorEstimator()

    def electronic_energy(x: np.ndarray) -> float:
        result = estimator.run([(ansatz, [H], [x])]).result()
        return float(result[0].data.evs[0])

    result = minimize(
        electronic_energy,
        x0=np.zeros(ansatz.num_parameters),
        method="COBYLA",
        options={"maxiter": 500},
    )

    vqe_total = result.fun + NUCLEAR_REPULSION
    exact_total = float(np.min(np.linalg.eigvalsh(H.to_matrix()))) + NUCLEAR_REPULSION

    print(ansatz.draw(output="text"))
    print(f"\nVQE total energy   : {vqe_total:.6f} Ha")
    print(f"exact (diag)       : {exact_total:.6f} Ha   (literature H2 min ~ -1.1373)")
    print(f"error              : {abs(vqe_total - exact_total):.2e} Ha")


if __name__ == "__main__":
    main()
