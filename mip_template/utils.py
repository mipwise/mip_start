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


if __name__ == "__main__":
    import doctest
    doctest.testmod()
