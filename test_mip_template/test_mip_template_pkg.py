import unittest
from math import isclose
from pathlib import Path

from mwcommons import ticdat_utils as utils

import mip_template


cwd = Path(__file__).parent.resolve()

class TestMipMe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        dat = utils.read_data(f'{cwd}/data/testing_data/testing_data.json', mip_template.input_schema)
        cls.params = mip_template.input_schema.create_full_parameters_dict(dat)
        cls.dat = dat

    def test_1_action_data_ingestion(self):
        utils.check_data(self.dat, mip_template.input_schema)

    def test_2_action_data_prep(self):
        old_sum = self.dat.sample_input_table['Data Field Two'].sum()
        dat = mip_template.data_prep_solve(self.dat)
        new_sum = dat.sample_input_table['Data Field Two'].sum()
        close_enough = isclose(new_sum, self.params['Sample Float Parameter'] * old_sum, rel_tol=1e-2)
        self.assertTrue(close_enough, "Data prep check")

    def test_3_main_solve(self):
        sln = mip_template.solve(self.dat)
        self.assertSetEqual(set(sln.sample_output_table['Data Field']), {'Option 1', 'Option 2'}, 'Main solve check')

    def test_4_action_report_builder(self):
        sln = mip_template.solve(self.dat)
        sln = mip_template.report_builder_solve(self.dat, sln, f'{cwd}/test_mip_template/app/output')
        self.assertSetEqual(set(sln.sample_output_table['Data Field']), {'Option 1.0', 'Option 2.0'}, "Report check")


if __name__ == '__main__':
    unittest.main()
