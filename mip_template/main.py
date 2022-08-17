from mip_template import output_schema
from mip_template import input_schema


def solve(dat):
    """Sample solve engine."""
    params = input_schema.create_full_parameters_dict(dat)
    sample_input_table_df = dat.sample_input_table.copy()
    if params['Sample Two Values Parameter'] == 'Value 1':
        sample_output_table_df = sample_input_table_df[['Primary Key One', 'Data Field One']]
    elif params['Sample Two Values Parameter'] == 'Value 2':
        sample_output_table_df = sample_input_table_df[['Primary Key Two', 'Data Field Two']]
    else:
        raise ValueError(f"bad value for 'Sample Two Values Parameter': {params['Sample Two Values Parameter']}")
    sample_output_table_df.rename(
        columns={'Primary Key One': 'Primary Key', 'Data Field One': 'Data Field'}, inplace=True)
    sln = output_schema.PanDat()
    sln.sample_output_table = sample_output_table_df
    return sln
