import unittest
from math import isclose
from pathlib import Path

from mwcommons import ticdat_utils as utils

import mip_start


cwd = Path(__file__).parent.resolve()

class TestMipMe(unittest.TestCase):

    @classmethod
    def setUpClass(cls) -> None:
        dat = utils.read_data(f'{cwd}/data/testing_data.xlsx', mip_start.input_schema)
        cls.params = mip_start.input_schema.create_full_parameters_dict(dat)
        cls.dat = dat

    def test_1_action_data_ingestion(self):
        utils.check_data(self.dat, mip_start.input_schema)

    def test_2_action_data_prep(self):
        new_dat = mip_start.update_food_cost_solve(self.dat)
        
        old_df = self.dat.foods.copy()
        new_df = new_dat.foods.copy()

        comparison_df = new_df[['Food ID', 'Per Unit Cost']].merge(
            old_df[['Food ID', 'Per Unit Cost']],
            on='Food ID',
            how='outer',
            suffixes=(' New', ' Old')
        )

        # ensure old and new Food ID values match
        missing_entries = comparison_df['Per Unit Cost Old'].isna() | comparison_df['Per Unit Cost New'].isna()
        self.assertFalse(missing_entries.any(), "Update food cost action should not change Food IDs")

        # ensure new cost is (Food Cost Multiplier) * old cost
        comparison_df['Diff'] = abs(
            comparison_df['Per Unit Cost New']
            - self.params['Food Cost Multiplier'] * comparison_df['Per Unit Cost Old']
        )
        close_enough = (comparison_df['Diff'] < 1e-2)
        self.assertTrue(close_enough.all(), "Update food cost check 2")

    def test_3_main_solve(self):
        sln = mip_start.solve(self.dat)
        kpis_df = sln.kpis.copy()
        self.assertTrue("Total Cost" in kpis_df['Name'].values, "'Total Cost' should be a kpi")
        total_cost = kpis_df.loc[kpis_df['Name'] == 'Total Cost', 'Value'].iloc[0]
        self.assertTrue(isclose(total_cost, 11.92, abs_tol=1e-2), "'Total Cost' should be 11.92")

    def test_4_action_report_builder(self):
        sln = mip_start.solve(self.dat)
        sln = mip_start.report_builder_solve(self.dat, sln, f'{cwd}/app/output')


if __name__ == '__main__':
    unittest.main()
