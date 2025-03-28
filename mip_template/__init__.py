__version__ = "0.1.0"
from mip_template.action_report_builder import report_builder_solve
from mip_template.action_update_food_cost import update_food_cost_solve
from mip_template.constants import Portions
from mip_template.create_output_data import create_output_tables
from mip_template.load_model_data import get_optimization_data
from mip_template.main import solve
from mip_template.model import optimize
from mip_template.schemas import input_schema, output_schema


# Configured deployment on Mip Hub, see https://github.com/mipwise/mip-go/tree/main/6_deploy/4_configured_deployment
actions_config = {
    'Update Food Cost': {
        'schema': 'input',
        'engine': update_food_cost_solve,
        'tooltip': "Update the food cost by the factor inputted in the 'Food Cost Multiplier' parameter"
    },
    'Report Builder': {
        'schema': 'output',
        'engine': report_builder_solve,
        'tooltip': "Read the output from the main engine and populate a chart of food-nutrient contributions"
    }
}

parameters_config = {
    'hidden': [],
    'categories': {'Solver': ['Time Limit', 'Mip Gap']},
    'order': [],
    'tooltips': {
        'Food Cost Multiplier': "Factor by which to multiply the 'Per Unit Cost' column in 'foods' input table",
        'Time Limit': "Maximum time (in seconds) to run the optimization",
        'Mip Gap': "Relative MIP gap tolerance for mixed-integer linear programs",
    }
}

input_tables_config = {
    'hidden_tables': [],
    'categories': {},
    'order': ['parameters', 'foods', 'nutrients', 'foods_nutrients'],
    'tables_display_names': {},
    'columns_display_names': {},
    'hidden_columns': {}
}

output_tables_config = {
    'hidden_tables': [],
    'categories': {},
    'order': ['buy', 'nutrition'],
    'tables_display_names': {},
    'columns_display_names': {},
    'hidden_columns': {}
}
