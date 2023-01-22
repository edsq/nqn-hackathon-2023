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

```python
import numpy as np
from numpy import linalg as la
import random

%matplotlib inline
#%matplotlib notebook
import matplotlib.pyplot as plt
import math
from scipy.integrate import solve_ivp
import cmath

# import matplotlib.animation as animation
from matplotlib.ticker import FormatStrFormatter
```

```python
# make a matrix random
def get_uniform(dim, t, U):
    M = np.zeros((dim, dim), dtype=complex)
    for i in range(dim):
        for j in range(dim):

            if j == i + 1:
                M[i][j] = t
            if i == j + 1:
                M[i][j] = np.conj(t)

            if i == j:
                M[i][i] = 0
            # if i==j and i%2 == 0: M[i][i] = t#2*t/3
            # if i== j and i%2 != 0: M[i][i] = 0#t/3
    # these terms close the ring
    # M[0][dim-1] = np.conj(t)
    # M[dim-1][0] = t

    return M
```

```python
def get_eigenstate(M, k):
    w, v = la.eigh(M)
    vAbs = np.absolute(v[k])
    wAbs = np.absolute(w)
    return vAbs

    # plt.plot(np.real(M.diagonal()))
    # plt.plot(w)
```

```python
def increment_randomness(M, rand, incs, dim):
    for i in range(dim):
        M[i][i] = M[i][i] + rand[i] / incs
    return M
```

```python
def plot_sequence_of_Hamiltonians(dim, rand, k, t, U, incs):
    M = get_uniform(dim, t, U)
    fig, ax = plt.subplots()
    plt.xlabel("Position")
    plt.ylabel("Probability")

    # for a in ax.flat:
    # a.set(xlabel='Position', ylabel='Probability')

    ax.yaxis.set_major_formatter(FormatStrFormatter("%.3f"))

    ax.set_title("Eigenstate " + str(k) + " Probability Distribution")
    # txt="I need the caption to be present a little below X-axis"
    # ax[0].figtext(0.5, -.05, txt, wrap=True, horizontalalignment='center', fontsize=12)
    vAbs = get_eigenstate(M, k)
    plt.plot(np.square(vAbs))  # plot norm square of each state

    for i in range(incs):
        vAbs = get_eigenstate(increment_randomness(M, rand, incs, dim), k)
        ax.plot(np.square(vAbs))
```

Considering only single particle states, the Hilbert space is reduced to the span of single local excitations. The Hamiltonian is the total system energy for each state along the diagnonal. If the ground state of each is taken to be zero, then it is simply the energy of the local excitations along the diagonal. The transisitons are local, thus

are represented in matrix form using the kronecker product.

```python
def init():

    TimeEvolutionStatic()
    # runAnimatedTimeEvolution()


def get_parameters():
    hbar = 1
    dim, hop_strength, U = 23, 1, 0
    incs = 1

    H = get_uniform(dim, hop_strength, U)
    rand = np.asarray([random.uniform(-U / 2, U / 2) for _ in range(dim)])
    H = increment_randomness(H, rand, incs, dim)

    initial_state = np.zeros(dim, dtype=complex)
    initial_state[int(dim / 2)] = 1  # [int(dim/2)]
    return H, dim, hbar, initial_state


def get_time_range():
    T = 100
    timesteps = 500
    return T, timesteps


def time_evolve(t, state, hbar, H):
    return 1 / 1j / hbar * (H @ state)


def TimeEvolutionStatic():
    H, dim, hbar, initial_state = get_parameters()
    T, timesteps = get_time_range()
    sol = solve_ivp(
        time_evolve,
        [0, T],
        np.array(initial_state),
        t_eval=np.linspace(0, T, timesteps),
        args=(hbar, H),
    )
    probabilities = np.square(np.abs(sol.y[:, -1].T))

    plt.figure(1)
    plt.plot(range(dim), np.square(np.abs(initial_state)))

    fig, ax = plt.subplots()
    ax.yaxis.set_major_formatter(FormatStrFormatter("%.2f"))
    ax.set_title("Time Evolution of Lattice Centered Spike")
    plt.xlabel("Position")
    plt.ylabel("Probability")

    plt.figure(2)
    frames = 1 + 1
    for a in range(1, frames):

        plt.hist(np.square(np.abs(sol.y[:, int(a * timesteps / frames)].T)), bins=dim)
        plt.figure(3)
        plt.plot(
            range(dim), np.square(np.abs(sol.y[:, int(a * timesteps / frames)].T))
        )  # int(a*timesteps/frames)
```

```python
init()
```

```python

```
