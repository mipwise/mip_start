from mip_template.schemas import input_schema


def update_food_cost_solve(dat):
    """Scale food cost by 'Food Cost Multiplier' input parameter"""
    params = input_schema.create_full_parameters_dict(dat)
    _dat = input_schema.copy_pan_dat(dat)
    foods = _dat.foods.copy()
    
    foods['Per Unit Cost'] = params['Food Cost Multiplier'] * foods['Per Unit Cost']
    foods = foods.round({'Per Unit Cost': 2})
    _dat.foods = foods
    
    return _dat
