# Mip Template
This is a template repository that follows the standards of the 
[Mip Go](https://www.mipwise.com/mip-go) program. 

Use this template as a starting point for new projects. You only need to 
rename `mip_template` with the name of your project in a few places:
- [ ] References in this README file.
- [ ] The name of the [root](../mip_template), [package](mip_template), and
  [testing](test_mip_template) directories (in Pycharm, do a right-click and 
  then  `Refactor > Rename...` or just `SHIFT + F6`).
- [ ] The name of [unit testing script](test_mip_template/test_mip_template.py).
- [ ] References in [pyproject.toml](pyproject.toml).
- [ ] Exceptions in [.gitignore](.gitignore).

Make sure to keep the word "test_" when renaming the testing directory 
and the unit testing scripts.

## Repository guide
- [docs](docs): Hosts documentation (in addition to readme files and docstrings)
  of the project.
- [mip_template](mip_template): Contains the Python package that solves the 
  problem.
  It contains scripts that define the input and the output data schemas, the 
  solution engine, and other auxiliary modules.
- [test_mip_template](test_mip_template): Hosts testing suits and testing data 
  sets used for testing the solution throughout the development process.
- `pyproject.toml` is used to build the distribution files 
  of the package (more information [here](https://github.com/mipwise/mip-go/blob/main/6_deploy/1_distribution_package/README.md)).

## Setting Up and Using `uv`

`uv` is a tool for managing the dependencies of your Python project. The goal here is to help you create a local virtual environment using `uv` and understand the most common commands.

### Installing `uv`
Install `uv` on your system following the [instructions](https://docs.astral.sh/uv/getting-started/installation/)

### Adding/removing dependencies
After cloning the repository and everytime `pyproject.toml` is modified (e.g. after a `git pull`), simply run
```bash
uv sync
```

First, `uv sync` creates a virtual environment `.venv` if it doesn't exist yet. Then, it updates the dependencies installed in `.venv` to match exactly those in the lock file `uv.lock` (created from `pyproject.toml`). This means installing dependencies from `uv.lock` that are currently missing in `.venv`, and also removing packages from `.venv` that are not listed in `uv.lock`.

### Adding/removing dependencies

To add/remove dependencies from your project/virtual environment, call
```bash
uv add <package>
```

or 

```bash
uv remove <package>
```

`uv` will install/uninstall `<package>` in/from `.venv` (as `pip` would do). However, `uv`  will also add/remove the `<package>` dependency to/from `pyproject.toml` (under `dependencies` table) and update `uv.lock` accordingly, which is very handy.

Alternatively, you can modify dependencies manually in `pyproject.toml` and call `uv sync`.

**Note**: you don't need to activate the virtual environment on the terminal to run `uv` commands. For example, `uv add <package>` installs `<package>` `.venv` regardless of its activation. However, you do need to activate it if you intend to run scripts from the terminal, use`source .venv/bin/activate` on Linux/macOS, or `.venv\Scripts\activate` on Windows. Similarly, you need to select `.venv` as the python interpreter for your IDE if you use one (e.g. VS Code or Pycharm).
