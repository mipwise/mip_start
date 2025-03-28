from ticdat import standard_main

from mip_start.main import solve
from mip_start.schemas import input_schema, output_schema


# When run from the command line, will read/write json/xls/csv/db/sql/mdb files.
# For example, the next command will read from a model stored in input.xlsx and write the solution to output.xlsx.
#   python -m mip_template -i input.xlsx -o solution.xlsx -e errors.xlsx
# "-e <errors_file_or_dir>" argument is optional; if used ticdat will check for errors (according to the input schema
# definition) and store in a xlsx/xls file as separate tabs, or into a directory as separate csv files.
if __name__ == "__main__":
    standard_main(input_schema, output_schema, solve)
