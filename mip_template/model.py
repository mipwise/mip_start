"""
Implementation of model. The model could be a MIP model, metaheuristic model, etc.
"""
from typing import Any
import pyscipopt as scip
from pyscipopt import quicksum as qs


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
    # Instantiate the model
    mdl = scip.Model("diet_problem")
    # Retrieve model data
    I, J = data_in['I'], data_in['J']
    nl, nu, nq = data_in['nl'], data_in['nu'], data_in['nq']
    c = data_in['c']
    # Create variables
    x = {}
    for i in I:
        x[i] = mdl.addVar(vtype='C', name=i)

    # Add constraints
    for j in J:
        mdl.addCons(qs(nq[i, j] * x[i] for i in I) >= nl[j], name=f'nl_{j}')
        mdl.addCons(qs(nq[i, j] * x[i] for i in I) <= nu[j], name=f'nu_{j}')

    # Set objective
    mdl.setObjective(qs(c[i] * x[i] for i in I))

    # Set solver parameters
    if params['Time Limit']:
        mdl.setRealParam('limits/time', params['Time Limit'])
    mdl.setRealParam('limits/gap', params['Mip Gap'])

    # Optimize and retrieve the solution
    mdl.optimize()
    status = mdl.getStatus()
    if status == 'optimal':
        x_sol = [(key, mdl.getVal(var)) for key, var in x.items()]
    else:
        x_sol = None
        print(f'Model is not optimal. Status: {status}')

    return x_sol
