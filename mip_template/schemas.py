"""
Defines the input and output schemas of the problem.
For more details on how to implement and configure data schemas see:
https://github.com/mipwise/mip-go/tree/main/5_develop/4_data_schema
"""
from mwcommons.ticdat_types import float_number, non_negative_float, non_negative_integer, text
from ticdat import PanDatFactory

from mip_template.constants import SampleConstants


# TODO: replace by diet problem schema
# TODO: add TimeLimit and MipGap as ticdat parameters
# region INPUT SCHEMA
input_schema = PanDatFactory(
    parameters=[['Name'], ['Value']],  # Do not change the column names of the parameters table!
    sample_input_table=[['Primary Key One', 'Primary Key Two'], ['Data Field One', 'Data Field Two']],
)
# endregion

# region USER PARAMETERS
input_schema.add_parameter('Sample Text Parameter', default_value='Any Text', **text())
input_schema.add_parameter('Sample Two Values Parameter', default_value=SampleConstants.FIRST_VALUE,
                           **text(strings_allowed=tuple(SampleConstants)))
input_schema.add_parameter('Sample Float Parameter', default_value=1.5,
                           **non_negative_float(max=10, inclusive_max=True))
input_schema.add_parameter('Sample Int Parameter', default_value=1,
                           **non_negative_integer(max=10, inclusive_max=True))
input_schema.add_parameter('Sample Date Parameter', default_value='11/21/2022', datetime=True)
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    sample_output_table=[['Primary Key'], ['Data Field']],
)
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA
# region sample_input_table
table = 'sample_input_table'
input_schema.set_data_type(table=table, field='Primary Key One', **text())
input_schema.set_data_type(table=table, field='Primary Key Two', **text())
input_schema.set_data_type(table=table, field='Data Field One', **text(strings_allowed=('Option 1', 'Option 2')))
input_schema.set_data_type(table=table, field='Data Field Two', **float_number())
# endregion
# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA
# region sample_output_table
table = 'sample_output_table'
output_schema.set_data_type(table=table, field='Primary Key', **text())
output_schema.set_data_type(table=table, field='Data Field', **text())
# endregion
# endregion
