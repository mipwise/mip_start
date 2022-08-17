import mip_template
import unittest
import utils
import os


class TestLocalExecution(unittest.TestCase):
    """
    Class for convenient local execution of solve engines.

    The methods of this class mimic the execution flow that a user typically experience on Mip Hub.
    """

    def test_1_action_data_ingestion(self):
        dat = utils.read_data(os.path.join('testing_data', 'testing_data.json'), mip_template.input_schema)
        utils.check_data(dat, mip_template.input_schema)
        utils.write_data(dat, 'inputs', mip_template.input_schema)

    def test_2_action_data_prep(self):
        dat = utils.read_data('inputs', mip_template.input_schema)
        dat = mip_template.action_data_prep.data_prep_solve(dat)
        utils.write_data(dat, 'inputs', mip_template.input_schema)

    def test_3_main_solve(self):
        dat = utils.read_data('inputs', mip_template.input_schema)
        sln = mip_template.solve(dat)
        utils.write_data(sln, 'outputs', mip_template.output_schema)

    def test_4_action_report_builder(self):
        dat = utils.read_data('inputs', mip_template.input_schema)
        sln = utils.read_data('outputs', mip_template.output_schema)
        sln = mip_template.action_report_builder.report_builder_solve(dat, sln)
        utils.write_data(sln, 'outputs', mip_template.output_schema)


if __name__ == '__main__':
    unittest.main()
