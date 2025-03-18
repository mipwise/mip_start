"""
Module to read input data and create the optimization parameters.
"""
from typing import Any


def get_optimization_data(dat, params) -> dict[str, Any]:
    """
    Read input data and prepare optimization parameters.
    
    Parameters
    ----------
    dat
        Input data, according to input schema.
    params : dict[str, Any]
        Dictionary with parameters as {param_name: value}.
    
    Returns
    -------
    data_in
        Dictionary with optimization parameters as {param_name: value} according to the formulation.
    """
    ...
