# Northwest Quantum Nexus 2023 Hackathon

The Washington State University team's submission to the NQN Hackathon.

[Read the documentation here.](https://edsq.github.io/nqn-hackathon-2023)


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

## Develoment notes
- Put all notebooks to be committed in the repository in the `notebooks/` directory
    - A `jupytext` generated markdown pair file will automatically be generated in `md_notebooks/` - only commit this markdown file, not the `.ipynb` file!
- If you pull new notebooks from the remote repository, you'll need to run `jupytext --sync md_notebooks/*` again to generate the `*.ipynb` file
- Try not to add new dependencies without careful consideration
- Autoformat python files and jupyter notebooks using the `black` command (e.g. `black notebooks/hello_world.ipynb`)
- If `black` would make changes to a file staged for commit, `pre-commit` will block the commit
    - If this happens, you can simply re `git add` the files `black` changed and re-commit
    - Best practice is probably to inspect the changes `black` made with a `git diff` first, however
