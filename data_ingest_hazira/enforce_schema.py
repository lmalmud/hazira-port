'''
enforce_schema.py
Function to run check on all a csv file to ensure
that necessary columns are present.
'''
import pandas as pd

def enforce_schema(file, name, SCHEMA):
    '''
    Parameters
    file: name of .csv file
    name: desired output pickle name
    SCHEMA: dictionary with columns and dtypes
    Returns
    dataframe and exports it to .pkl
    '''
    df = pd.read_csv(file)

    # Any columns that are supposed to be in the dataframe that are not
    missing = set(SCHEMA['columns']) - set(df.columns)
    if missing:
        raise RuntimeError(f'{file} missing columns {missing}')

    # Set the columns to be their given types
    df = df[SCHEMA['columns']].astype(SCHEMA['dtypes'])

    df.to_pickle(f'{name}.pkl')

    return df