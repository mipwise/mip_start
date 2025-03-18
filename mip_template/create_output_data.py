"""
Module to read the outputs from the model and create output data.
"""
from typing import Any


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
    ...
