'''
ingest_container_moves_hazira.py
Enforces schema for container_moves_hazira.csv
'''

from enforce_schema import enforce_schema
import pandas as pd

SCHEMA = {
    'columns' : ['container_arrival', 'call_id', 'teu_handled', 'resource_assigned', 'move_start', 'move_end'],
    'dtypes' : {'container_arrival' : 'datetime64[ns]',
                'call_id' : 'int64',
                'teu_handled' : 'int64',
                'resource_assigned' : 'string',
                'move_start' : 'datetime64[ns]',
                'move_end' : 'datetime64[ns]'}
}

file = '../simulation_tasks/container_moves_hazira.csv'
enforce_schema(file, 'container_moves_hazira', SCHEMA)