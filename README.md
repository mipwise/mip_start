# Mip Start
This is a template repository for building python packages for data pipelines.

Use this template as a starting point for new projects. You only need to 
rename `mip_start` with the name of your project in a few places:
- [ ] References in this README file.
- [ ] The name of the [root](../mip_start), [package](mip_start), and
  [testing](test_mip_start) directories (in Pycharm, do a right-click and 
  then  `Refactor > Rename...` or just `SHIFT + F6`).
- [ ] The name of [unit testing script](test_mip_start/test_mip_start_pkg.py). Be careful to not name it the same as its parent folder!
- [ ] References in [pyproject.toml](pyproject.toml).
- [ ] Exceptions in [.gitignore](.gitignore).

Make sure to keep the word "test_" when renaming the testing directory 
and the unit testing scripts.

## Repository guide
- [docs](docs): Hosts documentation (in addition to readme files and docstrings)
  of the project.
- [mip_start](mip_start): Contains the Python package that solves the 
  problem.
  It contains scripts that define the input and the output data schemas, the 
  solution engine, data manipulations, and other auxiliary modules.
- [test_mip_start](test_mip_start): Hosts testing suits and testing data 
  sets used for testing the solution throughout the development process.
- `pyproject.toml` is used to build the distribution files 
  of the package (more information [here](https://github.com/mipwise/mip-go/blob/main/6_deploy/1_distribution_package/README.md)).

## Project setup

1. Clone the repository on your machine and navigate to its folder (same level of this readme)
2. Create a python virtual environment, e.g. `pythonX.Y -m venv <venv_name>`  
    - Make sure to use a python version `X.Y` compatible with [pyproject.toml](pyproject.toml)'s `requires-python`
    - Replace `<venv_name>` by a name for your virtual environment (e.g. `.venv`)
3. Activate the virtual environment
    - Linux/macOS: `source <venv_name>/bin/activate`
    - Windows (cmd): `<venv_name>\Scripts\activate` or `.\<venv_name>\Scripts\activate`
    - If necessary, call `deactivate` (Linux/macOS/Windows) to deactivate an already activated virtual environment
4. Install dependencies: `pip install -r requirements.txt`

### Path-handling

For the scripts on this project to run properly, the python interpreter must be able to locate modules/packages in the root folder of this repository (the parent folder of this readme file). This ensures that all import statements across the project work well.

If you're using Pycharm, you can disregard this section because it will handle that for you under the hood.

Otherwise, you need to manually add the project's root folder to the interpreter's path. **With your virtual environment activated, and from the project's root folder**, run:  
- Linux/macOS:  
`pwd > "$(python -c 'import site; print(site.getsitepackages()[0])')/path_to_root.pth"`
- Windows (cmd):  
    1. `python -c "import site; print(site.getsitepackages())"`. This will output some paths on the console; copy the first path that contains `site-packages` (without quotes);
    2. `cd > "<path>\path_to_root.pth"` (make sure to use double quotes). Replace `<path>` by what you copied from step 1.

This will locate the appropriate site-packages directory under your virtual environment, and create a file `path_to_root.pth` with one line that points to the root folder. This ensures that any module/package on this repository can be found (i.e. imported) starting from the project's root folder.

To make sure it worked, you can run `python -c "import sys; print(sys.path)"` and confirm that the path to the root folder of your project shows up among the output.
