import os
from typing import Dict, Union

from ticdat import PanDatFactory, TicDatFactory


def read_data(input_data_loc: str, schema: Union[PanDatFactory, TicDatFactory]):
    """
    Reads data from files and populates an instance of the corresponding schema.

    Parameters
    ----------
    input_data_loc: str
        Path-like string to the input data. It can be a directory containing CSV files, a xls/xlsx file, or a json
        file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat.
    
    Returns
    -------
    PanDat
        a PanDat object populated with the tables available in the input_data_loc.
    """
    print(f'Reading data from: {input_data_loc}')
    
    if not isinstance(input_data_loc, str):
        raise TypeError(f"input_data_loc should be a string, not {type(input_data_loc)}")
    if not isinstance(schema, (TicDatFactory, PanDatFactory)):
        raise TypeError(f"schema should be a TicDatFactory or PanDatFactory, not {type(schema)}")
    if not os.path.exists(input_data_loc):
        raise ValueError(f"bad input_data_loc path: '{input_data_loc}'")
    
    if str(input_data_loc).endswith(".xlsx") or str(input_data_loc).endswith(".xls"):
        dat = schema.xls.create_pan_dat(input_data_loc)
    elif str(input_data_loc).endswith("json"):
        dat = schema.json.create_pan_dat(input_data_loc)
    else:  # read from cvs files
        if not os.path.isdir(input_data_loc):
            raise ValueError(f"input_data_loc should be a directory, if not .xlsx, .xls, or .json:\n{input_data_loc}")
        dat = schema.csv.create_pan_dat(input_data_loc)
    
    return dat


def write_data(sln, output_data_loc: str, schema: Union[PanDatFactory, TicDatFactory]) -> None:
    """
    Writes data to the specified location.

    Parameters
    ----------
    sln: PanDat
        A PanDat object populated with the data to be written to file/files.
    output_data_loc: str
        Path-like string to save the sln to. It can be a directory (to save the data as CSV files), a xls/xlsx file,
        or a json file.
    schema: PanDatFactory
        An instance of the PanDatFactory class of ticdat compatible with sln.
    
    Returns
    -------
    None
    """
    print(f'Writing data back to: {output_data_loc}')
    
    if not isinstance(output_data_loc, str):
        raise TypeError(f"input_data_loc should be a string, not {type(output_data_loc)}")
    if not isinstance(schema, (TicDatFactory, PanDatFactory)):
        raise TypeError(f"schema should be a TicDatFactory or PanDatFactory, not {type(schema)}")
    if not os.path.exists(output_data_loc):
        raise ValueError(f"bad output_data_loc path: '{output_data_loc}'")
    
    if output_data_loc.endswith(".xlsx") or output_data_loc.endswith("xls"):
        schema.xls.write_file(sln, output_data_loc)
    elif output_data_loc.endswith(".json"):
        schema.json.write_file_pd(sln, output_data_loc, orient='split')
    else:  # write to csv files
        if not os.path.isdir(output_data_loc):
            raise ValueError(
                f"output_data_loc should be a directory, if not .xlsx, .xls, or .json:\n{output_data_loc}"
            )
        schema.csv.write_directory(sln, output_data_loc)
    
    return None


def print_failures(schema: Union[PanDatFactory, TicDatFactory], failures: Dict) -> None:
    """Prints out a sample of the data failure encountered."""
    if isinstance(schema, PanDatFactory):
        for table_name, table in failures.items():
            print(table_name)
            print(table.head().to_string())
    elif isinstance(schema, TicDatFactory):
        for table_name, table in failures.items():
            print(table_name)
            print({key: table[key] for key in list(table)[:5]})
    else:
        raise ValueError('bad schema')


def check_data(dat, schema: Union[PanDatFactory, TicDatFactory]) -> None:
    """
    Runs data integrity checks and prints out some sample failures to facilitate debugging.

    :param dat: A PanDat or TicDat object.
    :param schema: The schema that `dat` belongs to.
    :return: None
    """
    print('Running data integrity check...')
    assert isinstance(schema, (TicDatFactory, PanDatFactory))
    if isinstance(schema, TicDatFactory):
        if not schema.good_tic_dat_object(dat):
            raise AssertionError("Not a good TicDat object")
    else:
        if not schema.good_pan_dat_object(dat):
            raise AssertionError("Not a good PanDat object")
    foreign_key_failures = schema.find_foreign_key_failures(dat)
    if foreign_key_failures:
        print_failures(schema, foreign_key_failures)
        raise AssertionError(f"Foreign key failures found in {len(foreign_key_failures)} table(s)/field(s).")
    data_type_failures = schema.find_data_type_failures(dat)
    if data_type_failures:
        print_failures(schema, data_type_failures)
        raise AssertionError(f"Data type failures found in {len(data_type_failures)} table(s)/field(s).")
    data_row_failures = schema.find_data_row_failures(dat)
    if data_row_failures:
        print_failures(schema, data_row_failures)
        raise AssertionError(f"Data row failures found in {len(data_row_failures)} table(s)/field(s).")
    duplicates = schema.find_duplicates(dat)
    if duplicates:
        print_failures(schema, duplicates)
        raise AssertionError(f"Duplicates found in {len(duplicates)} table(s)/field(s).")
    print('Data is good!')
