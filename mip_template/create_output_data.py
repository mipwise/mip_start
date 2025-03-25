"""
Module to read the outputs from the model and create output data.
"""
from typing import Any

import pandas as pd

from mip_template.schemas import output_schema


def create_output_tables(dat, data_in: dict[str, Any], data_out: dict[str, Any]):
    """
    Receives input and optimization data to create output tables.
    
    Parameters
    ----------
    dat
        Input data, according to input schema.
    data_in
        Input data to the optimization model data, in the form {param_name: value}.
    data_out
        Output data from the optimization model, in the form {var_name: optimal_values}.
    """
    # Instantiate output schema object
    sln = output_schema.PanDat()

    # Populate the buy table
    x_df = pd.DataFrame(data=[(key, value) for key, value in data_out.items()], columns=['Food ID', 'Quantity'])
    buy_df = x_df.merge(dat.foods[['Food ID', 'Food Name']], on='Food ID', how='left')
    buy_df = buy_df.round({'Quantity': 2})
    buy_df = buy_df.astype({'Food ID': str, 'Food Name': str, 'Quantity': 'Float64'})
    sln.buy = buy_df

    # Populate the nutrition table
    foods_nutrients_df = dat.foods_nutrients[['Food ID', 'Nutrient ID', 'Quantity']]
    foods_nutrients_df = foods_nutrients_df.rename(columns={'Quantity': 'Quantity per Food'})
    # merge buy and foods nutrients to get total nutrients of the diet
    nutrition_df = buy_df.merge(foods_nutrients_df, on='Food ID', how='left')
    nutrition_df['Quantity'] = nutrition_df['Quantity'] * nutrition_df['Quantity per Food']
    nutrition_df = nutrition_df[['Nutrient ID', 'Quantity']].groupby('Nutrient ID').agg('sum').reset_index()
    # merge nutrition with nutrients to get additional columns
    nutrients_df = dat.nutrients[['Nutrient ID', 'Nutrient Name', 'Min Intake', 'Max Intake']]
    nutrition_df = nutrition_df.merge(nutrients_df, on='Nutrient ID', how='left')
    nutrition_df = nutrition_df.round({'Quantity': 2})
    nutrition_df = nutrition_df.astype({'Nutrient ID': str, 'Nutrient Name': str, 'Quantity': 'Float64',
                                        'Min Intake': 'Float64', 'Max Intake': 'Float64'})
    sln.nutrition = nutrition_df
    
    return sln