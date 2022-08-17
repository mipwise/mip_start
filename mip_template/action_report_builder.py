
def report_builder_solve(dat, sln):
    """Sample output action."""
    sample_input_table_df = dat.sample_input_table.copy()
    sample_output_table_df = sln.sample_output_table.copy()
    sample_output_table_df['Data Field'] = sample_input_table_df['Data Field One'] + '.0'
    sln.sample_output_table = sample_output_table_df
    return sln
