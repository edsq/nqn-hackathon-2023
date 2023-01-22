# Northwest Quantum Nexus 2023 Hackathon

The Washington State University team's submission to the NQN Hackathon.


## Development Installation

0. Clone the repository and `cd` into the project:
```
cd nqn-hackathon-2023
```

1. Create and activate the conda environment for the project:
```
conda env create -f environment.yml
conda activate nqn-2023
```
If you have [poetry](https://python-poetry.org) and python 3.9+ available already at the system level (e.g. through [pyenv](https://github.com/pyenv/pyenv)), you can avoid using conda, and let poetry handle the environment management.

2. Install the package:
```
poetry install
```

3. Install the pre-commit hooks:
```
pre-commit install
```

4. Generate the notebooks from synced markdown files using `jupytext`:
```
jupytext --sync md_notebooks/*
```
