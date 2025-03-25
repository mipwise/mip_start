__version__ = "0.1.0"
from mip_template.schemas import input_schema, output_schema
from mip_template.action_update_food_cost import update_food_cost_solve

from mip_template.load_model_data import get_optimization_data
from mip_template.model import optimize
from mip_template.create_output_data import create_output_tables

from mip_template.main import solve
from mip_template.action_report_builder import report_builder_solve


# For a configured deployment on Mip Hub see:
# https://github.com/mipwise/mip-go/tree/main/6_deploy/4_configured_deployment
