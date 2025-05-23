'''
ingest_berth_occupancy_hazira.py

'''

import glob
import pandas as pd

SCHEMA = {
    'columns' : ['time', 'MP1', 'MP2', 'MP3', 'MP4', 'CT1', 'CT2'],
    'dtypes' : {'time' : 'datetime64[ns]',
                'MP1' : 'float64',
                'MP2' : 'float64',
                'MP3' : 'float64',
                'MP4' : 'float64',
                'CT1' : 'float64',
                'CT2' : 'float64'}
}


file = '../simulation_tasks/berth_occupancy_hazira.csv'
df = pd.read_csv(file)

# Any columns that are supposed to be in the dataframe that are not
missing = set(SCHEMA['columns']) - set(df.columns)
if missing:
    raise RuntimeError(f'{file} missing columns {missing}')

# Set the columns to be their given types
df = df[SCHEMA['columns']].astype(SCHEMA['dtypes'])

pd.to_pickle('./data_ingest_hazira', 'berth_occupancy_hazira.pkl')