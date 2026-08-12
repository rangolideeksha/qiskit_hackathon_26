# 15-Hour Quantum Study Plan — NQCC Hackathon Primer

**Target:** NQCC UK Quantum Hackathon, 18–20 Aug (Warwick) · **Toolchain:** IBM Qiskit (confirmed)
**Courses:** [Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information) · [Fundamentals of Quantum Algorithms](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms)

> Exams/badges are optional — the goal is practical understanding, not certification.

Each lab hour maps to a folder in this repo. Runnable reference implementations live in [`examples/`](../examples).

---

## Setup (do before Hour 4)

- [ ] Create IBM Quantum Platform account
- [ ] Generate and save API token (put it in `.env`, see `.env.example`)
- [ ] `uv sync` to build the project venv
- [ ] Test-run a trivial circuit on a simulator: `uv run python examples/bell_state.py`

---

## Course 1 — Basics of Quantum Information · `course1_basics/`

- [ ] **Hour 1 — Single systems.** States as vectors, measurements, unitary operations. Review pace; pin down IBM's notation conventions.
- [ ] **Hour 2 — Multiple systems.** Tensor products, entanglement, measurements on composite systems. Trace a few examples by hand.
- [ ] **Hour 3 — Quantum circuits lesson.** Gates, circuit diagrams, how IBM formalizes circuit computations.
- [ ] **Hour 4 — Qiskit lab.** Set up environment; rebuild the circuits from Hours 2–3 in code. Inspect statevectors and measurement histograms.
- [ ] **Hour 5 — Teleportation & superdense coding.** Trace both circuits carefully, then implement teleportation in Qiskit.
- [ ] **Hour 6 — CHSH game / inequality.** Work through the strategy and why quantum beats classical. *(Optional: Course 1 exam.)*

---

## Course 2 — Fundamentals of Quantum Algorithms · `course2_algorithms/`

- [ ] **Hour 7 — Quantum query model.** Deutsch and Deutsch–Jozsa. Focus on the query framework and phase kickback.
- [ ] **Hour 8 — Bernstein–Vazirani & Simon's algorithm.** Simon's is the bridge to exponential speedups.
- [ ] **Hour 9 — Qiskit lab.** Implement Deutsch–Jozsa, Bernstein–Vazirani, and Simon's; verify speedup behavior on a simulator.
- [ ] **Hour 10 — Phase estimation part 1: the QFT circuit.** Build it for 3–4 qubits; understand the controlled-phase pattern.
- [ ] **Hour 11 — Phase estimation part 2.** Assemble the full algorithm from the QFT. Densest material — go slow.
- [ ] **Hour 12 — Integer factorization / Shor's.** Order finding and how the number theory connects to the circuit.
- [ ] **Hour 13 — Qiskit lab.** Build QFT and a small phase-estimation circuit; run order finding for a small number.
- [ ] **Hour 14 — Grover's algorithm.** Oracle, diffusion operator, geometric intuition, optimal iteration count. Implement in Qiskit.
- [ ] **Hour 15 — Consolidation.** Rework your two or three hardest circuits. *(Optional: Course 2 exam.)*

---

## When the problem statement lands

Note the domain (healthcare / energy / engineering), and whether it looks like optimization, simulation, or something else. Likely additions then: Qiskit primitives (Sampler/Estimator), error mitigation, and a variational algorithm (VQE or QAOA) — the family most likely to show up in a hackathon build.
