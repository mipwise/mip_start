"""
Implementation of model. The model could be a MIP model, metaheuristic model, etc.
"""
from typing import Any


def optimize(data_in: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    """
    Create the optimization model.
    
    Parameters
    ----------
    dat
        Input data, according to input schema.
    params : dict[str, Any]
        Dictionary with parameters as {param_name: value}.
    
    Returns
    -------
    data_out
        The model data after optimizing, in the form {var_name: optimal_values}.
    """
    ...
