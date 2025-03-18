from mwcommons.ticdat_utils import set_data_types, set_parameters_datatypes

from mip_template.create_output_data import create_output_tables
from mip_template.load_model_data import get_optimization_data
from mip_template.model import optimize
from mip_template.schemas import input_schema


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
    dat = set_data_types(dat=dat, schema=input_schema)
    params = input_schema.create_full_parameters_dict(dat)
    params = set_parameters_datatypes(params=params, schema=input_schema)
    data_in = get_optimization_data(dat=dat, params=params)
    data_out = optimize(data_in=data_in, params=params)
    sln = create_output_tables(dat=dat, data_in=data_in, data_out=data_out)
    
    return sln
