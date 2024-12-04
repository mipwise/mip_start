import unittest
from pathlib import Path

from mip_utils import ticdat_utils as utils

import mip_template


cwd = Path(__file__).parent.resolve()

class TestLocalExecution(unittest.TestCase):
    """
    THIS IS NOT UNIT TESTING! Unit testing are implemented in other scripts.

    This class only serves the purpose of conveniently (with one click) executing solve engines locally during
    development.

    In addition, the methods in this class mimic the execution flow that a user typically experience on a Mip Hub app.
    """

    def test_1_action_data_ingestion(self):
        dat = utils.read_data(f'{cwd}/data/testing_data/testing_data.json', mip_template.input_schema)
        utils.check_data(dat, mip_template.input_schema)
        utils.write_data(dat, f'{cwd}/data/inputs', mip_template.input_schema)

    def test_2_action_data_prep(self):
        dat = utils.read_data(f'{cwd}/data/inputs', mip_template.input_schema)
        dat = mip_template.data_prep_solve(dat)
        utils.write_data(dat, f'{cwd}/data/inputs', mip_template.input_schema)

    def test_3_main_solve(self):
        dat = utils.read_data(f'{cwd}/data/inputs', mip_template.input_schema)
        sln = mip_template.solve(dat)
        utils.write_data(sln, f'{cwd}/data/outputs', mip_template.output_schema)

    def test_4_action_report_builder(self):
        dat = utils.read_data(f'{cwd}/data/inputs', mip_template.input_schema)
        sln = utils.read_data(f'{cwd}/data/outputs', mip_template.output_schema)
        sln = mip_template.report_builder_solve(dat, sln)
        utils.write_data(sln, f'{cwd}/data/outputs', mip_template.output_schema)


if __name__ == '__main__':
    unittest.main()
