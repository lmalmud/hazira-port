'''
compute_savings_hazira.py
Write compute savings hazira.py: 
calculate differential Opex vs. 
baseline for each scenario; 
summarize savings by subprocess and total.
'''

import pandas as pd
from pathlib import Path

CONFIG = {
    "unit_rates" : Path("../baseline_cost_model_inputs/unit_costs_hazira.xlsx"),
    "baseline_xlsx" : Path("../simulation_tasks/hazira_monthly_metrics.xlsx"),
    "output_xlsx" : Path("Cost_Savings_Summary.xlsx"),
    "scenario_glob" : Path("Adjusted_Metrics_SC_*.xlsx") # Will match any pattern of adjusted metrics
}

def load_unit_rates(path: Path) -> pd.Series:
    '''
    Returns a dataframe, indexed by resource, with appropriate unit rates.
    Parameters
    path (Path): path to Excel spreadsheet containing unit rates
    '''
    df = pd.read_excel(path, sheet_name="unit_costs")
    df = df.set_index("metric")["unit_rate"] # metric is each resource: quay_crane, yard_crane, etc.
    return df

def annualize_metrics(df: pd.DataFrame) -> pd.Series:
    '''
    Sum columns that are numeric; assume one column per metric.
    '''
    numeric = df.select_dtypes("number")
    return numeric.sum()

print(load_unit_rates(CONFIG["unit_rates"]))