from typing import Any, Dict

import numpy as np
import pandas as pd
from ticdat import PanDatFactory

from mip_template.constants import BadInputDataError


def set_input_parameter(schema, dat, name: str, value: Any):
    assert isinstance(schema, PanDatFactory)
    assert isinstance(dat, schema.PanDat)
    assert isinstance(name, str)

    if name not in schema.parameters:
        raise ValueError(f"Parameter {repr(name)} not found in schema.")

    params_df: pd.DataFrame = dat.parameters.copy()
    _dat = schema.copy_pan_dat(dat)
    
    if name in params_df["Name"].values:
        print(f"Overwriting parameter {repr(name)} with new value {repr(value)}")
        params_df.loc[params_df["Name"] == name, "Value"] = value
    else:
        print(f"Adding new parameter {repr(name)} with value {repr(value)}")
        new_row = pd.DataFrame({"Name": [name], "Value": [value]})
        params_df = pd.concat([params_df, new_row], ignore_index=True, axis=0)
    
    _dat.parameters = params_df
    
    return _dat


def set_multiple_input_parameters(schema, dat, parameters: Dict[str, Any]):
    _dat = schema.copy_pan_dat(dat)
    
    for param_name, param_value in parameters.items():
        _dat = set_input_parameter(schema, _dat, param_name, param_value)

    return _dat


def set_data_types(dat, schema: PanDatFactory):
    """
    Return a copy of the input dat with the data types set according to the schema.
    
    Remember that ticdat doesn't enforce datatypes, it's meant only to check/validate the input data matches the
    specified types.
    """
    dat_ = schema.copy_pan_dat(pan_dat=dat)

    # get data_types dict from input_schema: {}
    data_types = schema.schema(include_ancillary_info=True)['data_types']

    # iterate over the data_types to get a dict with the data dtypes for each column, for each DataFrame
    for table_name in data_types.keys():
        table_df = getattr(dat_, table_name)
        table_df = table_df.reset_index(drop=True)
        fields = data_types[table_name].keys()
        for field in fields:
            field_data_type = data_types[table_name][field]._asdict()
            if field_data_type['datetime']:
                table_df[field] = pd.to_datetime(table_df[field])
            
            elif field_data_type['strings_allowed']:
                # if strings_allowed, the field is supposed to be str. However, simply setting astype(str) could
                # silently convert NaN values to 'nan' instead of '' (empty string). Similarly, original integer values
                # may have been understood as float an converted from 10 to 10.0 (if there was NaN values for instance,
                # pandas cast to float), so directly converting to str would lead to '10.0' instead of '10'.
                # We'll handle these cases carefully.
                table_df[field] = _set_series_type_to_str(table_df[field])
            
            elif field_data_type['number_allowed']:
                table_df[field] = table_df[field].astype(float)
                if field_data_type['must_be_int']:
                    int_field = table_df[field].astype(int)
                    # ensure we don't accidently round values in a silent bug
                    if not np.array_equal(int_field, table_df[field]):
                        raise BadInputDataError(
                            f"The column {table_name}.{field} must be int, but it contains non-integer values that " \
                            f"would be rounded by .astype(int) and therefore the type conversion is not clear."
                        )
                    table_df[field] = int_field
                    
        setattr(dat_, table_name, table_df)

    return dat_


def _set_series_type_to_str(series: pd.Series) -> pd.Series:
    """
    Converts a pandas series to str, converting NaN to '', decimals like '123.0' or 123.0 to '123', and keeping
    everything else unchanged.

    Parameters
    ----------
    series : pandas.series
        Series whose values are to be converted to str. It may contain decimals, so if we simply convert to str
        directly, we'll have strings like '123.0' but what we actually want is '123'.

    Returns
    -------
    pandas.series
        The output series with values converted to str and decimals removed, if any. NaN values are converted to the
        empty string ''. All the other values (non-numeric, not-null) are simply passed to .astype('str').
    """
    # try to convert to numeric first, to get entries that are numeric. Non-numeric entries will be NaN (coerce)
    to_numeric = pd.to_numeric(series, errors='coerce')
    
    # get indices
    numeric_indices = ~to_numeric.isna()
    nan_indices = series.isna()
    remaining_indices = (~numeric_indices) & (~nan_indices)
    
    # get entries
    numeric_entries = series.loc[numeric_indices]
    nan_entries = series.loc[nan_indices]
    remaining_entries = series.loc[remaining_indices]
    
    # convert entries
    # numeric: float -> int (e.g. 123.0 -> 123) -> str
    # NaN entries: simply fill with ''
    # everything else: simply convert to str
    numeric_entries = numeric_entries.astype('float').astype('int').astype('str')
    nan_entries = nan_entries.fillna('')
    remaining_entries = remaining_entries.astype('str')

    # put everything together keeping the original order
    output = pd.concat([numeric_entries, nan_entries, remaining_entries]).sort_index()

    return output


def is_null(value) -> bool:
    """
    Check if 'value' is None, NaN, empty string, or empty collections.

    The reason to create this function instead of simply relying on the built-in bool() is because
    1.  bool(float('nan')) returns True, suggesting it's not null, but we want it to be null;
    2.  bool(0) returns False, suggesting it's null, but we want it to be not null.    

    Parameters
    ----------
    value : Any
        Value to be checked.

    Returns
    -------
    bool
        True if the value is None, NaN, empty string, or empty collections, False otherwise.
    
    Examples:
    >>> is_null(None)
    True
    >>> is_null(float('nan'))
    True
    >>> is_null(np.nan)
    True
    >>> is_null("")
    True
    >>> is_null([])
    True
    >>> is_null({})
    True
    >>> is_null(set())
    True
    >>> is_null(0)
    False
    >>> is_null("non-empty")
    False
    >>> is_null("nan")
    False
    >>> is_null([1, 2, 3])
    False
    >>> is_null([np.nan])
    False
    """
    if isinstance(value, (int, float)):
        return np.isnan(value)

    return not bool(value)


def check_field_inclusion(dat, native_table: dict, foreign_table: dict, reverse: bool = False) -> None:
    """
    Ensure a foreign key relation from native_table to foreign_table structures.

    Parameters
    ----------
    dat
        A PanDat object that holds the native and foreign tables as attributes.
    native_table : dict
        A dictionary with the following keys:
            name : str
                The name of the native table.
            field : str
                The field in the native table to be checked against a foreign table's field.
            field_subset : str or None, default=None
                The field in the native table to be used to filter its rows when checking inclusion. See 'subset'.
                Set it to None if no filter is supposed to be applied, that is, all rows of the native table are to
                be checked at 'field' column.
            subset : set or None, default=None
                A set of values for filtering the native table by where 'field_subset' is in 'subset' before checking
                the inclusion. Set it to None if no filter is supposed to be applied.
            entry: str
                The name of the entry in the native table to be reported in the error message.
    foreign_table : dict
        A dictionary with the following keys:
            name : str
                The name of the foreign table.
            field : str
                The field in the foreign table that holds the reference values for the native table's field.
            field_subset : str or None, default=None
                The field in the foreign table to be used to filter its rows when checking inclusion. See 'subset'.
                Set it to None if no filter is supposed to be applied, that is, all rows of the foreign table hold
                reference values (at 'field' column) for the native table's 'field' column.
            subset : set or None, default=None
                A set of values for filtering the foreign table by where 'field_subset' is in 'subset' before checking
                the inclusion. Set it to None if no filter is supposed to be applied.
            entry: str
                The name of the entry in the foreign table to be reported in the error message.
    reverse : bool, default=False
        Whether to check the reverse inclusion as well. Defaults to False, that is, only the unidirectional inclusion
        from the native table to the foreign table is checked. Set it to True to check the equality.

    Raises
    ------
    BadInputDataError
        If the foreign key relation from the native table to the foreign table fails, that is, the field in the native
        table (possibly filtered) contains some value(s) not present in the foreign table's field (possibly filtered).
        If reverse is True, then this exception is raised in case the equality fails (instead of the unidirectional
        inclusion).
    """
    # ensure mandatory dictionaries' keys are present
    mandatory_keys = ['name', 'field', 'entry']
    missing_keys = []  # list of tuples (dictionary, missing_key) to report
    for dictionary, dict_name in [(native_table, 'native_table'), (foreign_table, 'foreign_table')]:
        for key in mandatory_keys:
            if key not in dictionary:
                missing_keys.append((dict_name, key))
        # ensure field_subset and subset are both present or both absent
        if ('field_subset' in dictionary) != ('subset' in dictionary):
            raise ValueError(
                f"If 'field_subset' is set, 'subset' must be set as well, and vice-versa. {dict_name}:\n{dictionary}"
            )
    if missing_keys:
        raise ValueError(
            f"{mandatory_keys} are mandatory keys for the dictionaries native_table and foreign_table. The following "
            f"are pairs of (dictionary, missing_key):\n{missing_keys}"
        )
    
    native_table_df = getattr(dat, native_table['name'])
    foreign_table_df = getattr(dat, foreign_table['name'])
    
    # create standard function to get the indices
    def _get_indices_to_compare(table_dict: dict, table_df: pd.DataFrame) -> set:
        assert bool(table_dict.get('field_subset', False)) == bool(table_dict.get('subset', False)), (
            f"If 'field_subset' is set, 'subset' must be set as well, and vice-versa.\n{table_dict}"
        )
        
        if table_dict.get('field_subset'):
            return set(table_df.loc[
                table_df[table_dict['field_subset']].isin(table_dict['subset']), table_dict['field']
            ])
        
        return set(table_df[table_dict['field']])
    
    # get sets of values to compare
    native_table_entries: set = _get_indices_to_compare(native_table, native_table_df)
    foreign_table_entries: set = _get_indices_to_compare(foreign_table, foreign_table_df)
    
    # create function to standardize the error message
    def _error_message(native_table: dict, foreign_table: dict, df_to_report: pd.DataFrame) -> str:
        base_text = (
            f"The following {native_table['entry']} show up in {native_table['name']}.{native_table['field']}, "
            f"but they don't appear in {foreign_table['name']}.{foreign_table['field']}"
        )
        
        if 'field_subset' in foreign_table:
            base_text += (
                f" (where {foreign_table['name']}.{foreign_table['field_subset']} is in {foreign_table['subset']})"
            )

        return base_text + f":\n{df_to_report.to_string(index=False)}"
    
    # compare inclusion of values from the native table into the foreign ones
    missing_entries = native_table_entries.difference(foreign_table_entries)
    if missing_entries:
        # there are entries in the native table that are not in the foreign table
        df_to_report = native_table_df[native_table_df[native_table['field']].isin(missing_entries)]
        raise BadInputDataError(_error_message(native_table, foreign_table, df_to_report))
    
    # check reverse inclusion if requested
    if reverse:
        missing_entries_reverse = foreign_table_entries.difference(native_table_entries)
        if missing_entries_reverse:
            # there are entries in the foreign table that are not in the native table
            df_to_report = foreign_table_df[foreign_table_df[foreign_table['field']].isin(missing_entries_reverse)]
            raise BadInputDataError(_error_message(foreign_table, native_table, df_to_report))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
