from pathlib import Path

import pandas as pd

import mip_start


cwd = Path(__file__).parent.resolve()

input_data_loc = f"{cwd}/data/testing_data.xlsx"
output_data_loc = f"{cwd}/data/output.xlsx"

# Read input data
dat = pd.read_excel(input_data_loc, sheet_name=None)

# Solve the optimization problem
sln = mip_start.solve(dat)

# Write output data
with pd.ExcelWriter(output_data_loc) as writer:
    for table_name, df in sln.items():
        df.to_excel(writer, sheet_name=table_name, index=False)
