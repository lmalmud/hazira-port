'''
compute_savings_hazira.py
Write compute savings hazira.py: 
calculate differential Opex vs. 
baseline for each scenario; 
summarize savings by subprocess and total.
'''

import pandas as pd
from pathlib import Path

NUM_QUAY = 6
NUM_YARD = 14

CONFIG = {
    "unit_rates" : Path("../baseline_cost_model_inputs/unit_costs_hazira.xlsx"),
    "baseline_xlsx" : Path("../baseline_cost_model_inputs/Cost_Model_Hazira.xlsx"),
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

def load_metrics_xlsx(path: Path) -> pd.Series:
    '''
    Read the data that we care about for computing prices
    into one dataframe.
    Parameters
    path (Path): path of the simulation spreadsheet
    Returns
    pd.Series: updated annual simulation values
    '''

    # Compute the total number of service hours for this simulation
    vessels = pd.read_excel(path, sheet_name="vessel_turnaround_haizra")
    vessels["service_time"] = pd.to_timedelta(vessels["service_time"])
    vessels["service_time"] = vessels["service_time"].dt.total_seconds() / 3600
    total_service_hours = vessels["service_time"].sum()

    cranes = pd.read_excel(path, sheet_name="crane_uptime_hazira")
    cranes["duration"] = pd.to_timedelta(cranes["duration"])
    cranes["duration"] = cranes["duration"].dt.total_seconds() / 3600

    # Separate the quay cranes from the yard cranes
    quay = cranes[cranes["resource_name"].str.contains("Quay")]
    yard = cranes[cranes["resource_name"].str.contains("Yard")]

    # Calculate the total number of hours of operation by subtracting
    # the number of downtime from the total possible number of working hours
    total_quay_hours = (NUM_QUAY*365*24) - quay["duration"].sum()
    total_yard_hours = (NUM_YARD*365*24) - yard["duration"].sum()

    gate = pd.read_excel(path, sheet_name="gate_entries_hazira")
    trucks_processed = gate["num_processed"].sum()

    data = {
        "vessel_service_hr" : total_service_hours,
        "quay_crane" : total_quay_hours,
        "yard_crane" : total_yard_hours,
        "truck_entry" : trucks_processed
    }

    # Does not return dataframe, but rather one dimensional array
    return pd.Series(data)

UNIT_RATES = load_unit_rates(CONFIG["unit_rates"])
savings_frames = []
kpi_frames = []
totals_frames = []

# .name on a Path object gets the actual path
# Iterate over each path that matches the format
for xlsx_path in CONFIG["scenario_glob"].parent.glob(CONFIG["scenario_glob"].name):
    # xlsx_path is something like Adjusted_Metrics_SC_aggressive.xlsx

    all_metrics = load_metrics_xlsx(xlsx_path)

    # Not every metric has a cost associated with it, like vessel turnaround
    costed_metrics = all_metrics[all_metrics.index.isin(UNIT_RATES.index)]
    uncosted_metrics = all_metrics[~all_metrics.index.isin(UNIT_RATES.index)]

    # Extract from spreadsheet the baseline annual costs
    scenario_costs = costed_metrics * UNIT_RATES.loc[costed_metrics.index]

    # Will have the volume consumed for every metric (including ones that were not improved in each scenario)
    baseline_metrics = pd.read_excel(CONFIG["baseline_xlsx"], sheet_name="Annual-Metrics").set_index("metric")["volume"]

    # Compute the baselien cost by multiplying by unit rate
    # Note that a new Sheet in the Workbook was created because we had not previously computed annual volumes
    baseline_costs = baseline_metrics[costed_metrics.index] * UNIT_RATES.loc[costed_metrics.index]

    delta_costs = baseline_costs - scenario_costs
    
    # 1. savings_by_subprocess
    savings_df = pd.DataFrame({
        "subprocess"      : costed_metrics.index,
        "baseline_qty"    : baseline_metrics[costed_metrics.index], # We only want the baseline metrics that are costed
        "baseline_cost"   : baseline_costs[costed_metrics.index],
        "scenario_qty"    : costed_metrics.values,
        "scenario_cost"   : scenario_costs.values,
        "savings_delta"   : delta_costs[costed_metrics.index].values,
        "savings_percent" : delta_costs[costed_metrics.index].values / baseline_costs[costed_metrics.index].values
    })


    # 2. kpi_changes (KPI = key performance indicator)
    kpi_df = pd.DataFrame({
        "metric"          : all_metrics.index,
        "baseline_value"  : baseline_metrics[all_metrics.index].values,
        "scenario_value"  : all_metrics.values,
        "change"          : all_metrics.values - baseline_metrics[all_metrics.index].values
    })

    ## 3) totals
    totals_df = pd.DataFrame([{
        "baseline_total_cost" : baseline_costs.sum(),
        "scenario_total_cost" : scenario_costs.sum(),
        "savings_delta"       : delta_costs.sum(),
        "savings_percent"     : delta_costs.sum() / baseline_costs.sum(),
    }])

    # Get simulation name
    profile = xlsx_path.stem.split("_")[-1] # example: 'agressive'

    # Tag each result with corresponding simulation
    savings_df["scenario"] = profile
    kpi_df["scenario"]     = profile
    totals_df["scenario"]  = profile

    # Add to list of all simulation dataframes
    savings_frames.append(savings_df)
    kpi_frames.append(kpi_df)
    totals_frames.append(totals_df)


# --- one big table per type ---------------
all_savings = pd.concat(savings_frames, ignore_index=True)   # scenario in a column
all_kpi     = pd.concat(kpi_frames,     ignore_index=True)
all_totals  = pd.concat(totals_frames,  ignore_index=True)

# --- write once ---------------------------
with pd.ExcelWriter(CONFIG["output_xlsx"], engine="xlsxwriter") as xlw:
    all_savings.to_excel(xlw, sheet_name="Savings_by_subprocess", index=False)
    all_kpi.to_excel(    xlw, sheet_name="KPI_changes",            index=False)
    all_totals.to_excel( xlw, sheet_name="Totals",                index=False)
