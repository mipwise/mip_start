"""
Implementation of model. The model could be a MIP model, metaheuristic model, etc.
"""
import pandas as pd
import pyscipopt as scip
from pyscipopt import quicksum as qs


def optimize(data_in):
    """
    Create the optimization model.
    
    Parameters
    ----------
    data_in: dict[str, Any]
        Dictionary with optimization input parameters as {param_name: value} according to the formulation.
    
    Returns
    -------
    data_out: dict[str, Any]
        The model data after optimizing, including status and variables' values.
    """
    # Initialize output data
    opt_sol = {}
    
    # Instantiate the model
    mdl = scip.Model("diet_problem")
    
    # Retrieve model data
    I, J = data_in['I'], data_in['J']
    nl, nu, nq = data_in['nl'], data_in['nu'], data_in['nq']
    c = data_in['c']
    
    # Create variables
    x = {}
    for i in I:
        # vtypes allowed: "C", "I", "B", "M"
        x[i] = mdl.addVar(vtype="C", name=f'x_{i}')

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
    mdl.setParam('limits/time', 300)  # in seconds
    mdl.setParam('limits/gap', 0.001)  # 0.1% optimality gap

    # Optimize and retrieve the solution
    mdl.optimize()
    status = mdl.getStatus()
    print(f'Model status: {status}')
    opt_sol['status'] = status
    
    opt_sol['vars'], opt_sol['kpis'] = {}, {}
    if mdl.getNSols() >= 1:  # if there's at least one feasible solution...
        x_sol = {key: mdl.getVal(var) for key, var in x.items()}
        opt_sol['vars']['x'] = x_sol
        
        final_obj = mdl.getObjVal()
        print(f'Final objective: {final_obj}')
        opt_sol['kpis']['Total Cost'] = round(final_obj, 2)
    
    return opt_sol
