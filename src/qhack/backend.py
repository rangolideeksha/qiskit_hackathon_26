"""Backend helpers.

By default everything runs on the local Aer simulator so labs work offline.
Set QISKIT_IBM_TOKEN in a .env file to target real IBM hardware later.
"""

from __future__ import annotations

import os

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator


def get_sampler_backend():
    """Return a runnable backend.

    Falls back to the local Aer simulator. Wire in qiskit-ibm-runtime here
    once you have a token and want to submit to real hardware.
    """
    return AerSimulator()


def run_counts(circuit: QuantumCircuit, shots: int = 1024) -> dict[str, int]:
    """Transpile, run on the local simulator, and return measurement counts."""
    backend = get_sampler_backend()
    tqc = transpile(circuit, backend)
    result = backend.run(tqc, shots=shots).result()
    return result.get_counts()


def has_ibm_token() -> bool:
    return bool(os.environ.get("QISKIT_IBM_TOKEN"))
