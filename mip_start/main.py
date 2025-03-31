from mip_start.input_data import get_optimization_data
from mip_start.model import optimize
from mip_start.output_data import create_output_tables


def solve(dat):
    # Get optimization data
    model_data = get_optimization_data(dat)

    # Build optimization model
    model_sol = optimize(model_data)

    # Populate output tables
    sln = create_output_tables(dat, model_data, model_sol)

    return sln
