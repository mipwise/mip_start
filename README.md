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