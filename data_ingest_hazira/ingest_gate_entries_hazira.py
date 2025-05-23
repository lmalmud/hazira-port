'''
ingest_gate_entries_hazira.py
Enforces schema for gate_entries_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['time', 'arrivals', 'num_processed', 'queue_length'],
    'dtypes' : {'time' : 'datetime64[ns]',
                'arrivals' : 'int64',
                'num_processed' : 'int64',
                'queue_length' : 'int64'}
}

file = '../simulation_tasks/gate_entries_hazira.csv'
enforce_schema(file, 'gate_entries_hazira', SCHEMA)