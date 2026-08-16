# Hackathon prep — VQE, chemistry, and your hardware

Team 3 · Johnson Matthey · Quantum-accelerated catalyst design for sequential hydrogenation
Emulation: AWS · Primary: AWS **AQT** (trapped ion) · Backup: **Google / Alice & Bob** (cat qubits) · SDK: Qiskit

---

## 1. What the use case actually asks for

"Catalyst design for sequential hydrogenation" is, computationally, a **ground-state
energy** problem. Hydrogenation adds H2 across bonds one step at a time; whether a
catalyst helps is decided by the **energy differences** along that path:

- energies of reactant, each intermediate, and product,
- binding energy of species adsorbed on the catalyst site,
- activation barriers between steps.

Every one of those is a ground-state energy of some molecular Hamiltonian. The quantum
method for estimating ground-state energies on near-term hardware is **VQE** (Variational
Quantum Eigensolver). So the deliverable is almost certainly: *a VQE pipeline that
computes relative energies along a small hydrogenation pathway, runs on the AWS emulator,
and is demonstrated (or projected) on AQT.*

Your `examples/vqe_h2.py` is the smallest complete version of this. Everything scales up
from those four steps.

## 2. VQE in four steps (maps directly to the code)

1. **Hamiltonian → Pauli sum.** A molecule's electronic Hamiltonian becomes a weighted
   sum of Pauli strings via a fermion-to-qubit mapping (Jordan–Wigner, or **parity**
   which allows a 2-qubit reduction). `SparsePauliOp` holds it.
2. **Ansatz.** A parameterized circuit `|psi(theta)>`. Two families:
   - *hardware-efficient* (RY/RZ + CX layers): shallow, device-friendly, but can hit
     "barren plateaus" and may miss chemistry.
   - *UCCSD* (chemistry-motivated, from Qiskit Nature): more accurate, much deeper.
   On NISQ hardware the depth-vs-accuracy trade-off is a genuine design decision.
3. **Estimator primitive.** Returns `<psi(theta)|H|psi(theta)>`. `StatevectorEstimator`
   for exact simulation; `BackendEstimator` / `BraketEstimator` for shots on a device.
4. **Classical optimizer** (COBYLA, SPSA on noisy hardware) nudges `theta` downhill.

The variational principle guarantees the result is an **upper bound** on the true ground
energy — lower is better, and you can trust you never went below the truth.

## 3. Building a real molecular Hamiltonian (Qiskit Nature)

`vqe_h2.py` hard-codes H2 so it runs with core deps. For arbitrary geometries — which you
need for a reaction path — generate it:

```bash
uv sync --extra chem          # installs qiskit-nature + pyscf
```

```python
from qiskit_nature.second_q.drivers import PySCFDriver
from qiskit_nature.second_q.mappers import ParityMapper

problem = PySCFDriver(atom="H 0 0 0; H 0 0 0.735", basis="sto3g").run()
mapper  = ParityMapper(num_particles=problem.num_particles)
H = mapper.map(problem.hamiltonian.second_q_op())     # SparsePauliOp
nuclear = problem.hamiltonian.nuclear_repulsion_energy  # add to VQE result
```

Change `atom=...` to walk a bond length or swap in your intermediate — the rest of the
VQE loop is unchanged. That is how you get a **potential energy curve** / reaction profile.

### The hard constraint: qubit count

**AQT gives you 12 physical qubits.** Qubits ≈ 2 × spatial orbitals, so you must keep the
active space tiny. Levers, in order of reach:
- **freeze core** orbitals (don't correlate the inner electrons),
- **active-space selection** (a handful of frontier orbitals near the reaction),
- **parity mapping + two-qubit reduction** (what H2 uses to fit in 2 qubits),
- symmetry tapering to drop more qubits.

Design the chemistry to fit the hardware, not the other way around. A defensible small
model system that tells a real hydrogenation story beats an ambitious one that won't run.

## 4. Running Qiskit on AWS Braket

Development is in Qiskit; execution is on Braket. The bridge is
**`qiskit-braket-provider`** (v0.11+ supports Qiskit 2.0 and ships `BraketEstimator` /
`BraketSampler` primitives — ideal for VQE).

```bash
uv sync --extra braket
# configure AWS creds once: aws configure   (or env vars)
```

```python
from qiskit_braket_provider import BraketProvider, BraketLocalBackend

# 1) local emulator — free, fast, use for all development
local = BraketLocalBackend()

# 2) managed emulators + real QPUs
provider = BraketProvider()
provider.backends(statuses=["ONLINE"])          # discover devices
sv1 = provider.get_backend("SV1")               # 34-qubit statevector emulator
aqt = provider.get_backend("...")               # AQT IBEX Q1 (check exact name at runtime)

job = sv1.run(transpiled_circuit, shots=1000)
```

Workflow discipline: **debug on `BraketLocalBackend`, validate on SV1, spend real
QPU shots on AQT only when the pipeline is solid.** QPU tasks cost money and queue.

## 5. Your hardware, and why it shapes the design

**AWS AQT — IBEX Q1 (primary).** Trapped-ion, calcium-40 ions, **12 fully-connected
qubits**. Metrics: Quantum Volume 128, two-qubit gate fidelity ~98.7%, single-qubit
~99.97%. Native entangler is a Mølmer–Sørensen (XX-type) gate; all-to-all connectivity
means **no SWAP overhead** — a big win for chemistry ansätze whose excitation terms couple
distant orbitals. Hosted in Innsbruck (EU, `eu-north-1`). Implication: keep circuits shallow
(2-qubit gates are your error budget), exploit all-to-all so you don't waste depth routing.

**Google / Alice & Bob — cat qubits (backup).** A different philosophy: **bosonic cat
qubits** that are *bias-preserving* — bit-flips are exponentially suppressed in hardware,
so mostly phase-flips remain and a lightweight repetition code cleans those up. This is an
**error-correction story**, not a "more raw qubits" story. Good framing if the judges ask
about the path to fault tolerance; less about running a big VQE today. Know the one-liner:
*cat qubits trade one error type away at the hardware level to make correction cheaper.*

**AWS emulators.** `BraketLocalBackend` (local), **SV1** (statevector, ~34 qubits), TN1
(tensor network), DM1 (density matrix — use to model noise). Do 95% of your work here.

## 6. NISQ realities to budget for

- **Shots & noise:** on hardware the energy is a sampled mean — use enough shots and a
  noise-robust optimizer (**SPSA** over COBYLA).
- **Error mitigation:** zero-noise extrapolation, measurement-error mitigation. Braket/Qiskit
  primitives expose some of this; even mentioning it well scores points.
- **Chemical accuracy** is ~1.6 mHa (1 kcal/mol). You likely won't hit it on a real device
  for anything nontrivial — be honest, show the emulator result as ground truth and the
  hardware result with error bars.

## 7. A realistic deliverable shape

1. Pick a **minimal but meaningful** model of one hydrogenation step (small active space).
2. Build H per geometry with Qiskit Nature; VQE on the local emulator = your reference.
3. Compute a **relative energy** (e.g. reaction or binding energy) — differences cancel
   systematic errors and are what JM actually cares about.
4. Run the same circuit through `qiskit-braket-provider` on SV1, then a short AQT run.
5. Discuss: qubit budget, ansatz depth vs AQT's 2-qubit fidelity, mitigation, and why
   all-to-all connectivity suits this problem. That narrative is the score.

**Questions to ask the JM mentors early:** which specific reaction/catalyst? how big a
system do they expect? is a qualitative energy *trend* enough, or do they want a number?

---

### Sources
- [qiskit-braket-provider v0.11 — new primitives & compilation (AWS)](https://aws.amazon.com/blogs/quantum-computing/qiskit-braket-provider-v0-11-new-primitives-and-flexible-circuit-compilation)
- [Getting started with the Qiskit-Braket provider](https://qiskit-community.github.io/qiskit-braket-provider/tutorials/0_tutorial_qiskit-braket-provider_overview.html)
- [Amazon Braket launches AQT trapped-ion QPU (AWS blog)](https://aws.amazon.com/blogs/quantum-computing/amazon-braket-launches-trapped-ion-quantum-computer-from-alpine-quantum-technologies/)
- [AWS: new AQT processor on Braket](https://aws.amazon.com/about-aws/whats-new/2025/11/amazon-braket-alpine-quantum-technologies/)
- [Alice & Bob — cat qubits profile](https://quantumzeitgeist.com/alice-and-bob/)
- [Qiskit Nature — ground state solvers tutorial](https://qiskit-community.github.io/qiskit-nature/tutorials/03_ground_state_solvers.html)
- [IBM Quantum Learning — VQE module](https://quantum.cloud.ibm.com/learning/en/modules/computer-science/vqe)
