---
jupyter:
  jupytext:
    text_representation:
      extension: .md
      format_name: markdown
      format_version: '1.3'
      jupytext_version: 1.14.4
  kernelspec:
    display_name: Python [conda env:.conda-nqn-2023]
    language: python
    name: conda-env-.conda-nqn-2023-py
---

# Fermi-Hubbard Model


Some of the simplest (while still interesting) problems involve 1D spin chains or a Hubbard model, either with fermions or bosons. A [Hubbard model](https://en.wikipedia.org/wiki/Hubbard_model) For fermions, the Pauli's exclusion principle ensures that no two of them can have the exact same quantum numbers.

```python
from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.tools.monitor import job_monitor
from qiskit import Aer

backend = Aer.get_backend("aer_simulator")
```

```python
# Create a quantum circuit acting on a single qubit
circuit = QuantumCircuit(23, 23)
circuit.name = "Single qubit random"
circuit.h(0)
circuit.measure(0, 0)

theta_2 = 0.01
theta = 2 * theta_2
i = 5

circuit.rx(theta_2, i)
circuit.ry(theta, i)
circuit.rx(theta, i)
circuit.ry(theta, i)
circuit.rx(theta_2, i)

# Print out the circuit

circuit.measure(i, i)
circuit.draw("mpl")
```

```python
import numpy as np


class Circuit:
    """Return a circuit for Nq qubits.

    Attributes:
    ----------

    Nq : int
        Number of qubits.
    iter_t: int
        Number of iterations (min=1).
    min_inc : float
        Rotation angle, calulated by default.
    """

    def __init__(self, Nq=3, iter_t=1, min_inc=None):
        self.Nq = Nq
        self.t = iter_t - 1
        if min_inc is None:
            min_inc = np.pi * 10 ** (-3)
        self.min_inc = min_inc

    def get_circuit(self, qc=None):
        """Return circuit for single time step evolution."""

        if qc is None:
            qc = QuantumCircuit(self.Nq, self.Nq)

        theta = self.min_inc

        for i in range(self.Nq):
            qc.rx(theta, i)
            qc.ry(2 * theta, i)
            qc.rx(2 * theta, i)
            qc.ry(2 * theta, i)
            qc.rx(theta, i)

        for i in range(1, self.Nq - 1):
            qc.rx(theta, i)
            qc.ry(2 * theta, i)
            qc.rx(2 * theta, i)
            qc.ry(2 * theta, i)
            qc.rx(theta, i)

        return qc

    def get_circuit_steps(self):
        """Return circuit for t time steps."""

        qc = self.get_circuit()

        for i in range(self.t):
            self.get_circuit(qc)

        for i in range(self.Nq):
            qc.measure(i, i)

        # qc.draw()

        return qc
```

```python
obj = Circuit(Nq=3, iter_t=1)
qc = obj.get_circuit_steps()
qc.draw("mpl")
```

```python
circuit = qc
job = backend.run(circuit, shots=100)
job_monitor(job)

result = job.result()

# The result object is native to the Qiskit package, so we can use Qiskit's tools to print the result as a histogram.
plot_histogram(result.get_counts(circuit), title="Result")
```

```python
backend = provider.get_backend("ionq.qpu")
cost = backend.estimate_cost(circuit, shots=100)
print(f"Estimated cost: {cost.estimated_total} {cost.currency_code}")
```

```python

```
