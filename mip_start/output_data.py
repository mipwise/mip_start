"""
Module to read the outputs from the model and create output data.
"""
import pandas as pd


def create_output_tables(dat, data_in, data_out):
    """
    Receives input and optimization data to create output tables.
    
    Parameters
    ----------
    dat: dict[str, pd.DataFrame]
        Input data, dict {table_name: pandas.DataFrame}
    data_in: dict[str, Any]
        Input data to the optimization model data, in the form {param_name: value}.
    data_out: dict[str, Any]
        Output data from the optimization model.
    
    Returns
    -------
    dict[str, pd.DataFrame]
        Output data, dict {table_name: pandas.DataFrame}
    """
    # Instantiate output
    sln = {}

    # Read optimal values from the model
    x_sol = data_out['vars'].get('x', {})

    # Populate the kpis table
    kpis_df = pd.DataFrame(data=list(data_out['kpis'].items()), columns=['Name', 'Value'])
    sln['kpis'] = kpis_df
    
    # Populate the buy table
    x_df = pd.DataFrame(data=list(x_sol.items()), columns=['Food ID', 'Quantity'])
    buy_df = x_df.merge(dat['foods'][['Food ID', 'Food Name']], on='Food ID', how='left')
    buy_df = buy_df.astype({'Food ID': str, 'Food Name': str, 'Quantity': 'Float64'})
    buy_df = buy_df.sort_values(by='Food ID', ascending=True, ignore_index=True)
    sln['buy'] = buy_df.round({'Quantity': 2})

    # Populate the nutrition table
    foods_nutrients_df = dat['foods_nutrients'][['Food ID', 'Nutrient ID', 'Quantity']]
    foods_nutrients_df = foods_nutrients_df.rename(columns={'Quantity': 'Quantity per Food'})
    # merge buy and foods nutrients to get total nutrients of the diet
    nutrition_df = buy_df.merge(foods_nutrients_df, on='Food ID', how='left')
    nutrition_df['Quantity'] = nutrition_df['Quantity'] * nutrition_df['Quantity per Food']
    nutrition_df = nutrition_df[['Nutrient ID', 'Quantity']].groupby('Nutrient ID').agg('sum').reset_index()
    # merge nutrition with nutrients to get additional columns
    nutrients_df = dat['nutrients'][['Nutrient ID', 'Nutrient Name', 'Min Intake', 'Max Intake']]
    nutrition_df = nutrition_df.merge(nutrients_df, on='Nutrient ID', how='left')
    nutrition_df = nutrition_df.astype({'Nutrient ID': str, 'Nutrient Name': str, 'Quantity': 'Float64',
                                        'Min Intake': 'Float64', 'Max Intake': 'Float64'})
    nutrition_df = nutrition_df.sort_values(by='Nutrient ID', ascending=True, ignore_index=True)
    sln['nutrition'] = nutrition_df.round({'Quantity': 2})
    
    return sln
