"""
Defines the input and output schemas of the problem.
For more details on how to implement and configure data schemas see:
https://github.com/mipwise/mip-go/tree/main/5_develop/4_data_schema
"""
from mwcommons.ticdat_types import non_negative_float, text
from ticdat import PanDatFactory

from mip_template.constants import Portions


# region INPUT SCHEMA
input_schema = PanDatFactory(
    # syntax: table_name=[['Primary Key One', 'Primary Key Two'], ['Data Field One', 'Data Field Two']]
    parameters=[['Name'], ['Value']],  # this is a special table for parameters, don't change it!
    foods=[['Food ID'], ['Food Name', 'Per Unit Cost']],
    nutrients=[['Nutrient ID'], ['Nutrient Name', 'Min Intake', 'Max Intake']],
    foods_nutrients=[['Food ID', 'Nutrient ID'], ['Quantity']],
)
# endregion

# region USER PARAMETERS
input_schema.add_parameter('Food Cost Multiplier', default_value=1.5, **non_negative_float())
input_schema.add_parameter('Time Limit', default_value=None, nullable=True, **non_negative_float())
input_schema.add_parameter('Mip Gap', default_value=0.001, **non_negative_float(max=1.0, inclusive_max=False))
# endregion

# region OUTPUT SCHEMA
output_schema = PanDatFactory(
    buy=[['Food ID'], ['Food Name', 'Quantity']],
    nutrition=[['Nutrient ID'], ['Nutrient Name', 'Quantity']],
)
# endregion

# region DATA TYPES AND PREDICATES - INPUT SCHEMA

# region foods
table = 'foods'
input_schema.set_data_type(table=table, field='Food ID', **text())
input_schema.set_data_type(table=table, field='Food Name', **text())
input_schema.set_data_type(table=table, field='Per Unit Cost', **non_negative_float())
input_schema.set_default_value(table=table, field='Per Unit Cost', default_value=1.00)
# endregion

# region nutrients
table = 'nutrients'
input_schema.set_data_type(table=table, field='Nutrient ID', **text())
input_schema.set_data_type(table=table, field='Nutrient Name', **text())
input_schema.set_data_type(table=table, field='Min Intake', **non_negative_float())
input_schema.set_data_type(table=table, field='Max Intake', **non_negative_float())
input_schema.add_data_row_predicate(table=table, predicate_name='Min Intake <= Max Intake',
                                    predicate=lambda row: row['Min Intake'] <= row['Max Intake'])
# endregion

# region foods_nutrients
table = 'foods_nutrients'
for field in ['Food ID', 'Nutrient ID']:
    input_schema.set_data_type(table=table, field=field, **text())
input_schema.set_data_type(table=table, field='Quantity', **non_negative_float())
input_schema.add_foreign_key(native_table=table, foreign_table='foods', mappings=[('Food ID', 'Food ID')])
input_schema.add_foreign_key(native_table=table, foreign_table='nutrients', mappings=[('Nutrient ID', 'Nutrient ID')])
# endregion

# endregion

# region DATA TYPES AND PREDICATES - OUTPUT SCHEMA

# region buy
table = 'buy'
output_schema.set_data_type(table=table, field='Food ID', **text())
output_schema.set_data_type(table=table, field='Food Name', **text())
output_schema.set_data_type(table=table, field='Quantity', **non_negative_float())
# endregion

# region nutrition
table = 'nutrition'
output_schema.set_data_type(table=table, field='Nutrient ID', **text())
output_schema.set_data_type(table=table, field='Nutrient Name', **text())
output_schema.set_data_type(table=table, field='Quantity', **non_negative_float())
output_schema.set_data_type(table=table, field='Min Intake', **non_negative_float())
output_schema.set_data_type(table=table, field='Max Intake', **non_negative_float())
# endregion

# endregion
