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
- [ ] References in [setup.cfg](setup.cfg).
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
- `pyproject.toml` and `setup.cfg` are used to build the distribution files 
  of the package (more information [here](https://github.com/mipwise/mip-go/blob/main/6_deploy/1_distribution_package/README.md)).

## Setting Up and Using `uv`

`uv` is a tool for managing your Python project, including dependencies. The goal here is to help you create a local virtual environment using `uv` and understand the most common commands.

**TL;DR**: basic `uv` setup:
- after cloning the repository (and everytime `pyproject.toml` is modified, e.g. after a `git pull`), simply run `uv sync`
- to manage dependencies, either modify `pyproject.toml` manually (but not `uv.lock`!) and run `uv sync` afterwards, or use `uv add <package>` and `uv remove <package>`

**Note**: all the basic `uv` commands (`sync`, `add`, `remove`) will create a virtual environment `.venv` with default arguments (i.e. as `uv venv` would) if it doesn't exist yet. If environment variables were set, they will be used. Also, those commands also regenerate `uv.lock` accordingly.

**Note**: you don't need to activate the virtual environment on the terminal to run `uv` commands. For example, `uv add <package>` installs `<package>` on `uv`'s venv (e.g. `.venv`) regardless of its activation. However, you do need to activate it if you intend to run scripts from the terminal. Similarly, you need to select `uv`'s venv as the python interpreter for your IDE if you use one (e.g. VS Code or Pycharm).

### **1. Installing `uv`**

Follow the [official guide](https://docs.astral.sh/uv/getting-started/installation/) for installation. For example, in Linux/macOS one can run

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

while in Windows one can use

```bash
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### **2. Set Up the Virtual Environment**

**Note**: `uv sync`, `uv add <package>`, and `uv remove <package>` already create a virtual environment `.venv` (as `uv venv` does) if it doesn't exist yet. So, you only need to call `uv venv` if you want to specify arguments on how to create it.

To manually create a virtual environment with `uv`, navigate to the project's root folder and run:
```bash
uv venv --python 3.11
```
By default, `uv` will create a virtual environment in a directory named `.venv` (under the current working directory) using the specified python version (to be installed by `uv` if not yet available in the system).

If you activate `.venv` on a terminal (`source .venv/bin/activate` on Linux/macOS or `.venv\Scripts\activate` on Windows), it'll be displayed as the name of the project's root folder (e.g. `mip_template`) instead of the virtual environment folder name. You can customize that through

```bash
uv venv --python 3.11 --prompt my_preferred_display_name
```

**Note**: a good reason to use `uv` to create the virtual environment instead of `pip` is that `uv` already adds the project's root folder to the virtual environment python path. This means any python's `import` statement relative to the root of the project works nicely regardless of the IDE you're using, even from the command line.

If you want to customize the virtual environment path/name, please refer to [Customizing the Virtual Environment Path](#customizing-the-virtual-environment-path).

### **3. Common `uv` Commands**

#### Sync Dependencies

To ensure your virtual environment matches the lock file:

```bash
uv sync
```

Use this after pulling changes or updating `pyproject.toml`.

It updates the dependencies installed in the virtual environment to match exactly the ones in the lock file `uv.lock` (created from `pyproject.toml`). This means installing dependencies from `uv.lock` that are currently missing in the virtual environment, and also removing packages from the virtual environment that are not listed in `uv.lock`.

`uv sync` supports syncing specific groups of dependencies as explained in [Add Dependencies](#add-dependencies) section (e.g. `uv sync --no-dev`).

By default, `uv sync` only considers the `dependencies` table under `pyproject.toml` and `dependency-groups.dev` as actual dependencies. Other groups of dependencies from `pyproject.toml` must be specified explicitly:
- `uv sync --extra <optional_group>`: for groups of **optional** dependencies under `project.optional-dependencies` (`project.optional-dependencies.<optional_group>` in this case)
- `uv sync --group <my_group>`: for groups under `dependency-groups` (`dependency-groups.<my_group>` in this case)

Other options include `--extra <EXTRA>`, `--all-extras`, `--no-extra <EXTRA>`, `--no-dev`, `--only-dev`, `--group <GROUP>`, `--no-group <GROUP>`, `--only-group <GROUP>`, `--all-groups`. See `uv sync --help` for more details on those arguments.

#### **Add Dependencies**
To add a new dependency to the project:
```bash
uv add <package>
```

`uv` will install the most recent version of `<package>` in the virtual environment (as `pip install <package>` would do). `uv`  will also add `<package>` dependency to `pyproject.toml` (under `dependencies` table) and update `uv.lock` accordingly.

`uv` also handles version specification according to [PEP 508](https://peps.python.org/pep-0508/) (e.g. `uv add <package>==1.0.0`).

You can add dependencies under specific groups to `pyproject.toml`:
- `uv add <package> --dev` adds `<package>` to the development dependency group (i.e. under `dependency-groups.dev`)
- `uv add <package> --optional <optional_group>` adds `<package>` to the optional dependency group `<optional_group>` (i.e. under `project.optional-dependencies.<optional_group>`)
- `uv add <package> --group <specific_group>` adds `<package>` to the specified group `<specific_group>` (i.e. under `dependency-groups.<specific_group>`)

#### **Remove Dependencies**
To remove a dependency:
```bash
uv remove <package>
```

This uninstalls `<package>` (and its dependencies, unless needed for other dependencies) from the virtual environment, and also remove it from `pyproject.toml` and the lock file `uv.lock`.

By default `uv remove <package>` only removes dependencies from `dependencies` table. Use:
- `uv remove --group <my_group> <package>` to remove dependencies under `dependency-groups.<my_group>`, including development dependencies (i.e. `<my_group>=dev`)
- `uv remove --optional <optional_group> <package>` to remove optional dependencies under `project.optional-dependencies.<optional_group>`

**Note**: here's one advantage of using `uv remove <package>` instead of `pip uninstall <package>`: assume `pandas` is a dependency of your project, but not `numpy` explicitly, that is, you never need to import anything from `numpy` itself and `numpy` is not listed in `pyproject.toml`. Both `uv add pandas` and `pip install pandas` install both `pandas` and `numpy` since `numpy` is a dependency of `pandas`. However, `pip uninstall pandas` doesn't remove `numpy` since `pip` doesn't know that `numpy` is not a dependency (it doesn't fully interact with `.toml` files), whereas `uv remove pandas` also removes `numpy` because `uv` does know that `numpy` is not a dependency by reading `pyproject.toml`.

#### **Lock Dependencies**
To regenerate the lock file based on the current `pyproject.toml`:
```bash
uv lock
```
This ensures all dependencies are frozen to specific versions.

`uv lock` is already called under the hood by `uv add`, `uv remove` and `uv sync` so usually you don't need to call it explicitly.

#### Tree of Dependencies
`uv tree` displays the tree of dependencies. By default, it includes dependencies from `pyproject.toml`'s `dependencies` table, but also development (from `dependency-groups.dev`) and optional (under `project.optional-dependencies`) ones.

Development dependencies can be omitted through `uv tree --no-dev` or can be displayed alone through `uv tree --only-dev`.

Optional dependencies cannot be omitted. Dependencies from other groups can be configured through:
- `--group <my_group>` to include `<my_group>`
- `--no-group <my_group>` to exclude `<my_group>`
- `--only-group <my_group>` to only include `<my_group>`
- `--all-groups` to include all groups

**Note**: it seems `pip freeze` or `pip list` commands don't correctly return the packages installed in the virtual environment set up by `uv`. Instead, you can use `uv pip freeze` or `uv pip list`.

For example, by running `uv add pandas` (that also installs `numpy`, one of `pandas`'s dependencies) and then `uv remove pandas`, `uv` correctly installs and uninstalls `numpy`, however `pip freeze`/`pip list` still returns `numpy` as one of the installed packages. By running `python -c "import numpy"` you can confirm that `numpy` is indeed not installed (unless it's also a dependency in `pyproject.toml`).

#### **Build the Package**
To build the package,
```bash
uv build
```
It creates distribution files under `dist/`.

#### **Publish the Package**
To publish the package to PyPI:
```bash
uv publish
```
This requires a valid PyPI account and API token. Ensure the `pyproject.toml` is properly configured.

<font color="red"> **TODO**: validate this. Description generated by chatgpt </font>

### Customizing the Virtual Environment Path

If you want to use a different name for the virtual environment (e.g., `my_venv`), or to place it somewhere else instead of under the project's root directory, you need to set the environment variable
```plaintext
UV_PROJECT_ENVIRONMENT=path/to/my/venv
```

At first, this can be done through the terminal by setting an environment variable, like

```bash
export UV_PROJECT_ENVIRONMENT=path/to/my/venv
```

on Linux/macOS, or through

```powershell
$env:UV_PROJECT_ENVIRONMENT = "path/to/my/venv"
```
on Windows. However, this would require you to set that variable everytime you start a terminal/IDE session, which is annoying.

Instead, you can create a `.env` file in the project root with the following content:
```plaintext
UV_PROJECT_ENVIRONMENT="path/to/my/venv"
```

and configure your IDE to load `.env` everytime you open a new session.

For VS Code users, you can install the [sync-env](https://marketplace.visualstudio.com/items?itemName=dongido.sync-env) extension to automatically load variables from environment files (default=`.env`).

<font color="red"> **TODO**: add instructions for Pycharm </font>

Finally, if you're using git for version control, ensure `.env` is not tracked by adding it to `.gitignore`:
```plaintext
.env
```

### Environment Variables

Besides `UV_PROJECT_ENVIRONMENT` as explained [here](#customizing-the-virtual-environment-path), another useful environment variable to add to `.env` is
```plaintext
UV_PYTHON=3.11
```
to specify the python version for `uv` to use. By setting `UV_PYTHON`, you don't need to specify the `--python` argument for `uv venv`.
