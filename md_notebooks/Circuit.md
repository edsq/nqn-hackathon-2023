---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python 3 (ipykernel)
    language: python
    name: python3
---

# Fermi-Hubbard Model


Some of the simplest (while still interesting) problems involve 1D spin chains or a Hubbard model, either with fermions or bosons. A [Hubbard model](https://en.wikipedia.org/wiki/Hubbard_model) For fermions, the Pauli's exclusion principle ensures that no two of them can have the exact same quantum numbers.

```python
from qiskit import QuantumCircuit
from qiskit.extensions import Initialize
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit import Aer

backend = Aer.get_backend("aer_simulator")
```

```python
import numpy as np


class Circuit:
    """Return a circuit for Nq qubits.

    Attributes:
    ----------

    psi : numpy.array
        Initial state vector (default provided).
    Nq : int
        Number of qubits.
    iter_t: int
        Number of iterations (min=1).
    min_inc : float
        Rotation angle, calulated by default.
    """

    def __init__(
        self, psi=None, Nq=3, iter_t=1, min_inc=np.pi * 10 ** (-1), U=0.5, J=1.0
    ):
        self.Nq = Nq
        if psi is None:
            # Set the initial state to be a particle halfway on the lattice
            # This is represented by the bit string with the half-most significant bit set
            psi = np.zeros(2**Nq)
            psi[2 ** (Nq // 2)] = 1
        psi = psi / np.linalg.norm(psi)
        self.psi = psi

        self.t = iter_t - 1

        self.min_inc = min_inc
        self.U = U
        self.J = J

    def initialize(self):
        qc = QuantumCircuit(self.Nq, self.Nq)

        init_gate = Initialize(self.psi)
        init_gate.label = r"$\psi$"
        qc.append(init_gate, qc.qubits)

        qc.save_statevector(label="psi_i")

        return qc

    def get_circuit(self, qc=None):
        """Return circuit for single time step evolution."""

        if qc is None:
            qc = self.initialize()

        theta = -self.min_inc

        alpha = theta * self.J
        beta = theta * self.U

        for i in range(self.Nq):
            qc.rx(alpha, i)
            qc.ry(2 * alpha, i)
            qc.rx(alpha, i)
            qc.rz(2 * beta, i)
            qc.rx(alpha, i)
            qc.ry(2 * alpha, i)
            qc.rx(alpha, i)

        for i in range(1, self.Nq - 1):
            qc.rx(alpha, i)
            qc.ry(2 * alpha, i)
            qc.rx(alpha, i)
            qc.rz(2 * beta, i)
            qc.rx(alpha, i)
            qc.ry(2 * alpha, i)
            qc.rx(alpha, i)

        return qc

    def get_circuit_steps(self):
        """Return circuit for t time steps."""

        qc = self.get_circuit()

        for i in range(self.t):
            self.get_circuit(qc)

        qc.barrier()

        for i in range(self.Nq):
            qc.measure(i, i)

        return qc
```

```python
obj = Circuit(Nq=6, iter_t=1)
qc = obj.get_circuit_steps()
qc.draw("mpl")
```

```python
circuit = qc
job = backend.run(circuit, shots=100)
job_monitor(job)

result = job.result()
n_res = []

for i in range(obj.Nq):
    n_res.append(result.get_counts(circuit))

n_res = np.asarray(n_res)

# The result object is native to the Qiskit package, so we can use Qiskit's tools to print the result as a histogram.
plot_histogram(result.get_counts(circuit), title="Result")
```

```python

```
