# Northwest Quantum Nexus 2023 Hackathon

The Washington State University team's submission to the NQN Hackathon.


## Installation

0. Install [poetry](https://python-poetry.org), best done via [pipx](https://pypa.github.io/pipx/)
```
pipx install poetry
```

1. Create and activate a conda environment for the project:
```
conda create --name nqn-2023 python=3.9
conda activate nqn-2023
```
If you have python 3.9+ available already at the system (e.g. through [pyenv](https://github.com/pyenv/pyenv)), you can avoid using conda, and let PDM handle the environment management.

2. Install the package:
```
poetry install
```

3. Install the pre-commit hooks:
```
poetry run pre-commit install
```
