"""
Defines the input and output schemas of the problem.
For more details on how to implement and configure data schemas see:
https://github.com/mipwise/mip-go/tree/main/5_develop/4_data_schema
"""

from ticdat import PanDatFactory


# region Aliases for datatypes in ticdat
# Remark: use only aliases that match perfectly your needs, otherwise set datatype explicitly
float_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": -float("inf"),
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

non_negative_float = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": 0,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

positive_float = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": False,
    "min": 0,
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

integer_number = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": -float("inf"),
    "inclusive_min": False,
    "max": float("inf"),
    "inclusive_max": False,
}

non_negative_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 0,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

positive_integer = {
    "number_allowed": True,
    "strings_allowed": (),
    "must_be_int": True,
    "min": 1,
    "inclusive_min": True,
    "max": float("inf"),
    "inclusive_max": False,
}

text = {"strings_allowed": "*", "number_allowed": False}
# endregion

# region INPUT SCHEMA
input_schema = PanDatFactory(
    parameters=[['Name'], ['Value']],  # Do not change the column names of the parameters table!
    sample_input_table=[['Primary Key One', 'Primary Key Two'], ['Data Field One', 'Data Field Two']])
# endregion

# region USER PARAMETERS
input_schema.add_parameter('Sample Text Parameter', default_value='Any Text', number_allowed=False, strings_allowed='*')
input_schema.add_parameter('Sample Two Values Parameter', default_value='Value 1', number_allowed=False,
                           strings_allowed=['Value 1', 'Value 2'])
input_schema.add_parameter('Sample Float Parameter', default_value=1.5, number_allowed=True, strings_allowed=(),
                           must_be_int=False, min=0, inclusive_min=True, max=10, inclusive_max=True)
input_schema.add_parameter('Sample Date Parameter', default_value='11/21/2022', datetime=True)
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    sample_output_table=[['Primary Key'], ['Data Field']])
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA
# region sample_input_table
table = 'sample_input_table'
input_schema.set_data_type(table=table, field='Primary Key One', number_allowed=False, strings_allowed='*')
input_schema.set_data_type(table=table, field='Primary Key Two', number_allowed=False, strings_allowed='*')
input_schema.set_data_type(table=table, field='Data Field One', number_allowed=False,
                           strings_allowed=('Option 1', 'Option 2'))
input_schema.set_data_type(table=table, field='Data Field Two', number_allowed=True, strings_allowed=())
# endregion
# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA
# region sample_output_table
table = 'sample_output_table'
output_schema.set_data_type(table=table, field='Primary Key', number_allowed=False, strings_allowed='*')
output_schema.set_data_type(table=table, field='Data Field', number_allowed=False, strings_allowed='*')
# endregion
# endregion

