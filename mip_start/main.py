from mwcommons.ticdat_utils import check_data, set_data_types, set_parameters_datatypes

from mip_start.output_data import create_output_tables
from mip_start.input_data import get_optimization_data
from mip_start.model import optimize
from mip_start.schemas import input_schema


def solve(dat):
    """
    Main solve engine.

    Parameters
    ----------
    dat
        Input data, according to input schema.

    Returns
    -------
    sln
        Output data, according to output schema.
    """

    # Set data types for input data
    dat = set_data_types(dat=dat, schema=input_schema)
    
    # Check input data, according to input schema definition
    check_data(dat, input_schema)

    # Set data types for parameters
    params = input_schema.create_full_parameters_dict(dat)
    params = set_parameters_datatypes(params=params, schema=input_schema)

    # Get optimization data
    model_data = get_optimization_data(dat, params)

    # Build optimization model
    model_sol = optimize(model_data, params)

    # Populate output tables
    sln = create_output_tables(dat, model_data, model_sol)
    
    return sln
