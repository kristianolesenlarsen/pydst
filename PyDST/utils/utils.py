import pandas as pd

# These are small utility functions the end user might find useful.


def common_columns(df1, df2):
    """ Returns a list of the columns which are present in both dataframes.

    Args:
        df1: a pandas dataframe
        df2: a pandas dataframe
    Returns:
        list
    """
    if not isinstance(df1, pd.DataFrame) and isinstance(df2, pd.DataFrame):
        raise TypeError('Both input must be dataframes')

    return list(set(df1.columns) & set(df2.columns))
