__version__ = "0.1.0"
from mip_template.schemas import input_schema, output_schema
from mip_template.action_data_prep import data_prep_solve
from mip_template.main import solve
from mip_template.action_report_builder import report_builder_solve

# For a configured deployment on Mip Hub see:
# https://github.com/mipwise/mip-go/tree/main/6_deploy/4_configured_deployment

