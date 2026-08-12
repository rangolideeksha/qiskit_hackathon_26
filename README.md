# qiskit_hackathon_26

Qiskit walkthrough and practice repo for the **NQCC UK Quantum Hackathon 2026** (Warwick, 18–20 Aug). Structured around two IBM Quantum Learning courses, with runnable reference circuits and a per-project `uv`-managed environment.

## Quickstart

Requires [`uv`](https://docs.astral.sh/uv/). Everything runs offline on the Aer simulator — no IBM account needed to start.

```bash
uv sync                                   # build the project venv from pyproject.toml + uv.lock
uv run python examples/bell_state.py      # smoke test
```

`uv sync` creates a `.venv/` scoped to this repo, so the environment never leaks between projects. Add a dependency with `uv add <pkg>`; it updates `pyproject.toml` and `uv.lock` together. For the Jupyter extras: `uv sync --extra notebooks`.

## Layout

```
qiskit_hackathon_26/
├── pyproject.toml          # deps + uv config (Qiskit 2.x, Aer, ibm-runtime)
├── uv.lock                 # pinned, reproducible resolution
├── .python-version         # 3.13 (latest with Qiskit wheels; >=3.10 supported)
├── .env.example            # copy to .env for your IBM Quantum token
├── docs/
│   └── study_plan.md       # the 15-hour primer, hours mapped to folders
├── src/qhack/              # shared helpers (run_counts, backend selection)
├── examples/               # runnable reference circuits (all verified)
│   ├── bell_state.py       # entanglement smoke test
│   ├── teleportation.py    # teleport + verify (measures 0 every time)
│   ├── deutsch_jozsa.py    # constant vs. balanced in one query
│   ├── qft.py              # QFT from scratch, checked vs. analytic DFT
│   └── grover.py           # search with optimal iteration count
├── course1_basics/         # Basics of Quantum Information — labs, Hours 1–6
└── course2_algorithms/     # Fundamentals of Quantum Algorithms — labs, Hours 7–15
```

## Examples

Each script prints its circuit and a correctness check:

```bash
uv run python examples/teleportation.py   # -> teleport verified (out=0): 1024 / 1024
uv run python examples/qft.py             # -> QFT matches the analytic DFT matrix: True
uv run python examples/grover.py          # -> marked=101  found=101  success=yes
```

Copy from these into `course1_basics/` and `course2_algorithms/` as you work each lab hour.

## Study plan

The full 15-hour primer lives in [`docs/study_plan.md`](docs/study_plan.md), grounded in two IBM courses:
[Basics of Quantum Information](https://quantum.cloud.ibm.com/learning/en/courses/basics-of-quantum-information) and
[Fundamentals of Quantum Algorithms](https://quantum.cloud.ibm.com/learning/en/courses/fundamentals-of-quantum-algorithms). Exams/badges are optional — the goal is practical understanding.

## Running on real IBM hardware

The examples default to the local simulator. To target IBM Quantum, copy `.env.example` to `.env`, add your API token from [quantum.cloud.ibm.com](https://quantum.cloud.ibm.com/), and wire `qiskit-ibm-runtime` into `src/qhack/backend.py`. Never commit `.env` — it's git-ignored.
