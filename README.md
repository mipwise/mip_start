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
