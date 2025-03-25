"""
Implementation of model. The model could be a MIP model, metaheuristic model, etc.
"""
from typing import Any

import pandas as pd
import pyscipopt as scip
from pyscipopt import quicksum as qs


def optimize(data_in: dict[str, Any], params: dict[str, Any]) -> dict[str, Any]:
    """
    Create the optimization model.
    
    Parameters
    ----------
    data_in: dict[str, Any]
        Dictionary with optimization input parameters as {param_name: value} according to the formulation.
    params : dict[str, Any]
        Dictionary with parameters as {param_name: value} from input data.
    
    Returns
    -------
    data_out
        The model data after optimizing, including status and variables' values.
    """
    # Initialize output data
    opt_sol = {}
    
    # Instantiate the model
    mdl = scip.Model("diet_problem")
    
    # Retrieve model data
    I, J = data_in['I'], data_in['J']
    nl, nu, nq = data_in['nl'], data_in['nu'], data_in['nq']
    c, vtypes = data_in['c'], data_in['vtypes']
    
    # Create variables
    x = {}
    for i in I:
        # vtype is either "I" (integer) or "C" (continuous), depending on the input foods.Portion values
        x[i] = mdl.addVar(vtype=vtypes[i], name=f'x_{i}')

    # Add constraints
    for j in J:
        # C1
        mdl.addCons(qs(nq[i, j] * x[i] for i in I) >= nl[j], name=f'C1_{j}')
        
        # C2
        if pd.notnull(nu[j]):
            mdl.addCons(qs(nq[i, j] * x[i] for i in I) <= nu[j], name=f'C2_{j}')

    # Set objective
    mdl.setObjective(qs(c[i] * x[i] for i in I), sense='minimize')

    # Set solver parameters
    if params['Time Limit'] is not None:
        mdl.setParam('limits/time', params['Time Limit'])
    mdl.setParam('limits/gap', params['Mip Gap'])

    # Optimize and retrieve the solution
    mdl.optimize()
    status = mdl.getStatus()
    print(f'Model status: {status}')
    opt_sol['status'] = status
    
    opt_sol['vars'] = {}
    if mdl.getNSols() >= 1:  # if there's at least one feasible solution...
        x_sol = {key: mdl.getVal(var) for key, var in x.items()}
        opt_sol['vars']['x'] = x_sol
        
        final_obj = mdl.getObjVal()
        print(f'Final objective: {final_obj}')
        opt_sol['obj_val'] = final_obj
    
    return opt_sol
