#!/usr/bin/env python
# coding: utf-8

# # Introduction

# The Fermi-Hubbard model is an important tool for studying the behavior of fermionic particles in atomic lattices. This has relevance to a variety of physical problems, especially the study of superconductivity and magnetism, and can also model the behavior of atoms suspended in an optical lattice. The objective of our project is to simulate the dynamics of spin-1/2 particles in a Fermi-Hubbard system with a same-site interaction between particles of opposing spin. The simulation shall be performed on a trapped ion quantum computer.

# ## Fermi-Hubbard Hamiltonian
# 
# The Hamiltonian for a Fermi-Hubbard system is
# 
# $$
# \hat{H} = -J \sum_{j, s}^{L} ({\hat{c}_{j,s}}^{\dagger}\hat{c}_{j+1,s} + {\hat{c}_{j+1,s}}^{\dagger}\hat{c}_{j,s}) + U \sum_{j}^{L} \hat{n}_{j,\uparrow} \hat{n}_{j,\downarrow}
# $$
# 
# where $J$ is the hopping (or tunneling) strength, $L$ is the number of lattice sites, and $U$ is the interaction strength for fermions with opposing spin located at the same site. The index s tracks the spin of the operators. The operators ${\hat{c}_{j}}^{\dagger}$ and $\hat{c}_{j}$ are second-quantized fermionic creation and annihilation operators. The terms in the first summation over the lattice sites represent the kinetic energy of particles in the model and their motion forward or backward along the lattice. The tunneling strength $J$ is an overlap integral of adjacent orbitals in the lattice which determines the likelihood of a fermion tunneling through the potential barrier between adjacent lattice sites. The terms in the second summation describe the Coulomb interaction. The interaction strength $U$ is formally a two body integral accounting for Coulomb repulsion and spin-spin interaction.

# ## Second-quantization and Pauli matrices
# 
# In order to perform a quantum simulation of this problem on a quantum computer, it is necessary to translate the Hamiltonian into a form expressed using universal quantum gates, which are represented by Pauli matrices. The Pauli matrices are
# 
# $$
# \hat{\sigma}_x = \hat{X} = \left(\begin{matrix} 0 & 1 \\ 1 & 0 \end{matrix}\right), \quad \hat{\sigma}_y = \hat{Y} = \left(\begin{matrix} 0 & -i \\ i & 0 \end{matrix}\right), \quad \hat{\sigma}_z = \hat{Z} = \left(\begin{matrix} 1 & 0 \\ 0 & -1 \end{matrix}\right)
# $$
# 
# The second-quantized fermionic operators in the Hamiltonian need to be expressed in terms of these spin matrices. We can attempt to construct them using the Pauli matrices in the following way:
# 
# $$
# \hat{f}_{j} = \frac{\hat{X_j} + i\hat{Y_j}}{2} = \left( \begin{matrix} 0 & 1 \\ 0 & 0 \end{matrix}\right), \quad {\hat{f}_{j}}^{\dagger} = \frac{\hat{X_j} - i\hat{Y_j}}{2} = \left( \begin{matrix} 0 & 0 \\ 1 & 0\end{matrix}\right)
# $$
# 
# The subscript j indicates the lattice site that the operator acts on.
# 
# However, spin operators and fermionic operators don't share the same commutative and anti-commutative properties. The Pauli spin operators have the following commutation and anti-commutation properties:
# 
# $$
# [\hat{\sigma}_i, \hat{\sigma}_j] = 2i \epsilon_{ijk} \hat{\sigma}_k, \quad \{ \hat{\sigma}_i, \hat{\sigma}_j \} = 2 \delta_{ij} I
# $$
# 
# where $\epsilon_{ijk}$ is the Levi-Civita tensor, $\delta_{ij}$ is the Kronecker delta, and $I$ is the 2x2 identity matrix. The summation over the index k in the first equation is expressed using Einstein notation, for simplicity.
# 
# The fermionic creation and annihilation operators have the following properties:
# 
# $$
# \{ \hat{c}_{i}, {\hat{c}_{j}}^{\dagger} \} = \delta_{ij}, \quad \{ \hat{c}_{i}, \hat{c}_{j} \} = 0, \quad \{ {\hat{c}_{i}}^{\dagger}, {\hat{c}_{j}}^{\dagger} \} = 0
# $$
# 
# The fermionic operators for different lattice sites don't commute, i.e. $[\hat{c}_{i}, {\hat{c}_{j}}^{\dagger}] \neq 0$, but the spin operators for different sites do. This inconsistency prevents us from making a direct association between the two, and we must make use of a suitable tranformation relation that ensures the anti-symmetry of a fermionic state.

# ## The Jordan-Wigner Transform
# 
# One such transformation that can be used is the Jordan-Wigner tranformation, given by
# 
# $$
# \hat{c}_j = e^{\left( -i\pi\sum_{k=1}^{j-1} {\hat{f}_k}^{\dagger} \hat{f}_k \right)} \hat{f}_j, \quad {\hat{c}_j}^{\dagger} = e^{\left( +i\pi\sum_{k=1}^{j-1} {\hat{f}_k}^{\dagger} \hat{f}_k \right)} {\hat{f}_j}^{\dagger}, \quad {\hat{c}_j}^{\dagger} \hat{c}_j = {\hat{f}_j}^{\dagger} \hat{f}_j
# $$
# 
# The number operators are equal in terms of both spin and fermionic operators.
# 
# We can expand the exponents in the transformation equations and express them in the following form that is suitable for conversion into a quantum circuit:
# 
# $$
# e^{\left( \pm i\pi\sum_{k=1}^{j-1} {\hat{f}_k}^{\dagger} \hat{f}_k \right)} = \prod_{k=1}^{j-1} \left( -\hat{Z}_k \right)
# $$
# 
# This transformation enforces the anti-symmetry of the fermionic states and the Hamiltonian can now be expressed in terms of the quantum gates $\hat{X}$, $\hat{Y}$ and $\hat{Z}$. Expanding the Hamiltonian in terms of these operators, and making use of suitable identities for the Pauli operators, we eventually get
# 
# 
# $$
# H = \sum_{j,\sigma} -J(a^\dagger_{j,s}a_{j+1,s} + a^\dagger_{j+1,s}a_{j,s}) + Un_{j,\downarrow}n_{j,\uparrow} = \sum_{j,s} \frac{J}{2}(X_{j,s}X_{j+1,s} + Y_{j,s}Y_{j+1,\sigma}) + \frac{U}{4}(1- Z_{j,\uparrow} - Z_{j,\downarrow} + Z_{j,\uparrow}Z_{j,\downarrow})
# $$
# 

# 
# 
