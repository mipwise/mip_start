"""
Module to read input data and create the optimization parameters.
"""
from typing import Any

import pandas as pd



def get_optimization_data(dat) -> dict[str, Any]:
    """
    Read input data and prepare optimization parameters.
    
    Parameters
    ----------
    dat : dict[str, pd.DataFrame]
        Input data, according to input schema. Dictionary {table_name: pandas.DataFrame}.
    
    Returns
    -------
    data_in
        Dictionary with optimization parameters as {param_name: value} according to the formulation, and possibly some
        additional ones for coding purposes.
    """
    model_data = dict()  # initialize empty dict to store data for model
    model_data['I'] = set(dat['foods']['Food ID'])
    model_data['J'] = set(dat['nutrients']['Nutrient ID'])
    model_data['nl'] = dict(zip(dat['nutrients']['Nutrient ID'], dat['nutrients']['Min Intake']))
    model_data['nu'] = dict(zip(dat['nutrients']['Nutrient ID'], dat['nutrients']['Max Intake']))
    model_data['nq'] = dict(zip(zip(dat['foods_nutrients']['Food ID'], dat['foods_nutrients']['Nutrient ID']),
                                dat['foods_nutrients']['Quantity']))
    model_data['c'] = dict(zip(dat['foods']['Food ID'], dat['foods']['Per Unit Cost']))

    return model_data
