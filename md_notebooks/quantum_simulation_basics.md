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

<!-- #region -->
# Quantum Simulation Basics

We're aiming to simulate a Hamiltonian that looks like:

$$
\hat{H} = \hat{A} + \hat{B}
$$

The time evolution operator is thus:

$$
\hat{U}(t) = e^{\hat{H} t / i \hbar} = e^{(\hat{A} + \hat{B}) t / i \hbar}
$$

In our circuit, we have something like $\hat{A} = \hat{X}$, $\hat{B} = \hat{Y}$, where $\hat{X}$ and $\hat{Y}$ are the Pauli X and Y operators, respectively.  We know how to implement $e^{\hat{X}}$ and $e^{\hat{Y}}$ individually in a circuit (these are just rotation operators), so we would like to write our time evolution operator as the product of exponentials of single operators.  However,

$$
e^{(\hat{A} + \hat{B}) t /i \hbar} \neq e^{\hat{A} t / i \hbar} e^{\hat{B} t / i \hbar}
$$

Because, in general, $[A, B] \neq 0$.  This is encapuslated in the [Baker-Campbell-Hausdorff formula](https://en.wikipedia.org/wiki/Baker–Campbell–Hausdorff_formula).


## Exponentiating Hamiltonian - a first approximation

Let's examine the error we incur by approximating $e^{(\hat{A} + \hat{B}) t /i \hbar} \approx e^{\hat{A} t / i \hbar} e^{\hat{B} t / i \hbar}$.  Evolve forward in time by one time step:

$$
\begin{aligned}
| \psi(\Delta t) \rangle &= e^{\hat{H} \Delta t / i \hbar} | \psi(0) \rangle \\
                         &= e^{(\hat{A} + \hat{B}) t /i \hbar} | \psi(0) \rangle \\
                         &\approx e^{\hat{A} t / i \hbar} e^{\hat{B} t / i \hbar} | \psi(0) \rangle \\
\end{aligned}
$$

If we Taylor expand the true time propagator:

$$
\begin{aligned}
e^{(\hat{A} + \hat{B}) \Delta t /i \hbar} &= 1 + (\hat{A} + \hat{B}) \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2}(\hat{A} + \hat{B})^2 \left(\frac{\Delta t}{i \hbar}\right)^2 + \mathcal{O}(\Delta t^3) \\
    &= 1 + (\hat{A} + \hat{B}) \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2}(\hat{A}^2 + \hat{A} \hat{B} + \hat{B} \hat{A} + \hat{B}^2) \left(\frac{\Delta t}{i \hbar}\right)^2 + \mathcal{O}(\Delta t^3) \\
\end{aligned}
$$

Meanwhile, expanding our approximate operator $e^{\hat{A} t / i \hbar} e^{\hat{B} t / i \hbar}$:

$$
\begin{aligned}
e^{\hat{A} \Delta t / i \hbar} e^{\hat{B} \Delta t / i \hbar} &= \left(1 + \hat{A} \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2} \hat{A}^2 \left(\frac{\Delta t}{i \hbar}\right)^2 \right) \left(1 + \hat{B} \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2} \hat{B}^2 \left(\frac{\Delta t}{i \hbar}\right)^2 \right) + \mathcal{O}(\Delta t^3) \\
    &= 1 + \hat{A} \left(\frac{\Delta t}{i \hbar}\right) + \hat{B} \left(\frac{\Delta t}{i \hbar}\right) + \hat{A} \hat{B} \left(\frac{\Delta t}{i \hbar}\right)^2 + \frac{1}{2} \hat{A}^2 \left(\frac{\Delta t}{i \hbar}\right)^2 + \frac{1}{2} \hat{B}^2 \left(\frac{\Delta t}{i \hbar}\right)^2 + \mathcal{O}(\Delta t^3) \\
    &= 1 + (\hat{A} + \hat{B}) \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2}(\hat{A}^2 + 2 \hat{A} \hat{B} + \hat{B}^2) \left(\frac{\Delta t}{i \hbar}\right)^2 + \mathcal{O}(\Delta t^3)
\end{aligned}
$$

So we can see that our error at each time step is:

$$
e^{(\hat{A} + \hat{B}) \Delta t /i \hbar} - e^{\hat{A} \Delta t / i \hbar} e^{\hat{B} \Delta t / i \hbar} = \frac{1}{2}(- \hat{A} \hat{B} + \hat{B} \hat{A}) \left(\frac{\Delta t}{i \hbar}\right)^2 + \cdots = \mathcal{O}(\Delta t^2)
$$

Thus after $N = T / \Delta t$ timesteps, the global error will be $\mathcal{O}(\Delta t)$.  This is pretty bad, but we can do better.

## The Suzuki-Trotter Expansion

To improve our error, we employ the Suzuki-Trotter expansion:

$$
|\psi(t + \Delta t) \rangle \approx e^{\hat{B} \Delta t / 2 i \hbar} e^{\hat{A} \Delta t / i \hbar} e^{\hat{B} \Delta t / 2 i \hbar} |\psi(t) \rangle
$$

To see the truncation error in this method, we expand the exponentials as before.  To simplify the algebra, let $h = \Delta t / i \hbar$.  In what follows, we automatically discard terms of order $\mathcal{O}(h^3)$ and higher.

$$
\begin{aligned}
e^{\hat{B} h/2} e^{\hat{A} h} e^{\hat{B} h/2} &= \left(1 + \hat{B} \frac{h}{2} + \frac{1}{2} \hat{B}^2 \left(\frac{h}{2}\right)^2 \right) \left(1 + \hat{A} h + \frac{1}{2} \hat{A}^2 h^2 \right) \left(1 + \hat{B} \frac{h}{2} + \frac{1}{2} \hat{B}^2 \left(\frac{h}{2}\right)^2 \right) + \mathcal{O}(h^3) \\
    &= \left(1 + \hat{B} \frac{h}{2} + \frac{1}{2} \hat{B}^2 \left(\frac{h}{2}\right)^2 \right)
        \left[\left(1 + \hat{B} \frac{h}{2} + \frac{1}{2} \hat{B}^2 \left(\frac{h}{2}\right)^2 \right)
            + \hat{A} h + \frac{1}{2} \hat{A} \hat{B} h^2 + \frac{1}{2} \hat{A}^2 h^2
        \right] + \mathcal{O}(h^3) \\
    &= \left(1 + \hat{B} \frac{h}{2} + \frac{1}{2} \hat{B}^2 \left(\frac{h}{2}\right)^2 \right)
        \left[1 + \left(\hat{A} + \frac{1}{2}\hat{B}\right)h + \frac{1}{2}\left(\hat{A}^2 + \hat{A}\hat{B} + \frac{1}{4}\hat{B}^2 \right) h^2
        \right] + \mathcal{O}(h^3) \\
    &= 1 + \left(\hat{A} + \frac{1}{2}\hat{B}\right)h + \frac{1}{2}\left(\hat{A}^2 + \hat{A}\hat{B} + \frac{1}{4}\hat{B}^2 \right) h^2 \\
    &\quad + \frac{1}{2}\hat{B} h + \frac{1}{2} \hat{B}\hat{A} h^2 + \frac{1}{4}\hat{B}^2 h^2 \\
    &\quad + \frac{1}{8} \hat{B}^2 h^2 + \mathcal{O}(h^3) \\
    &= 1 + (\hat{A} + \hat{B}) h + \frac{1}{2}(\hat{A}^2 + \hat{A} \hat{B} + \hat{B} \hat{A} + \hat{B}^2) h^2 + \mathcal{O}(h^3) \\
    &= 1 + (\hat{A} + \hat{B}) \left(\frac{\Delta t}{i \hbar}\right) + \frac{1}{2}(\hat{A}^2 + \hat{A} \hat{B} + \hat{B} \hat{A} + \hat{B}^2) \left(\frac{\Delta t}{i \hbar}\right)^2 + \mathcal{O}(\Delta t^3)
\end{aligned}
$$

Thus the local truncation error is

$$
e^{(\hat{A} + \hat{B}) \Delta t /i \hbar} - e^{\hat{B} \Delta t / 2 i \hbar} e^{\hat{A} \Delta t / i \hbar} e^{\hat{B} \Delta t / 2 i \hbar} = \mathcal{O}(\Delta t^3)
$$

and so the global truncation error will be $\mathcal{O}(\Delta t^2)$, which is manageable.
<!-- #endregion -->
