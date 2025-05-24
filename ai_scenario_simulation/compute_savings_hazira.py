'''
compute_savings_hazira.py
Write compute savings hazira.py: 
calculate differential Opex vs. 
baseline for each scenario; 
summarize savings by subprocess and total.
'''

import pandas as pd

NUM_QUAY = 6
NUM_YARD = 14
unit_costs = pd.read_excel('../baseline_cost_model_inputs/unit_costs_hazira.xlsx', 'unit_costs')
base = pd.read_excel('../simulation_tasks/hazira_monthly_metrics.xlsx', 'Sheet1')

# TODO: calculate the baseline costs and the new costs for each simulation