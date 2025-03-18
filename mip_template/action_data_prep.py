from mip_template.schemas import input_schema


# TODO: replace by update_food_cost() function
def data_prep_solve(dat):
    """Sample input action."""
    params = input_schema.create_full_parameters_dict(dat)
    sample_input_table_df = dat.sample_input_table.copy()
    sample_input_table_df['Data Field Two'] = params['Sample Float Parameter'] * sample_input_table_df['Data Field Two']
    dat.sample_input_table = sample_input_table_df
    return dat


