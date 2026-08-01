# ==========================================================
# PART 4 : KPI ANALYTICS
# Ferry Capacity Utilization & Operational Efficiency
# ==========================================================

import pandas as pd
import numpy as np

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv",
    parse_dates=["Timestamp"]
)

print("="*60)
print("KPI ANALYTICS")
print("="*60)

# ----------------------------------------------------------
# Capacity Utilization Ratio (CUR)
# ----------------------------------------------------------

df["Capacity_Utilization_Ratio"] = (
    df["Redemption_Count"] /
    (df["Sales_Count"] + 1)
)

# ----------------------------------------------------------
# Operational Load Index (OLI)
# ----------------------------------------------------------

activity = (
    df["Sales_Count"] +
    df["Redemption_Count"]
)

df["Operational_Load_Index"] = (
    activity - activity.min()
) / (
    activity.max() - activity.min()
)

# ----------------------------------------------------------
# Congestion Pressure Index (CPI)
# ----------------------------------------------------------

df["Congestion_Pressure_Index"] = (
    0.6 * df["Operational_Load_Index"] +
    0.4 * df["Capacity_Utilization_Ratio"]
)

# ----------------------------------------------------------
# Idle Capacity Indicator
# ----------------------------------------------------------

idle_threshold = activity.quantile(0.25)

df["Idle_Capacity"] = (
    activity <= idle_threshold
).astype(int)

# ----------------------------------------------------------
# Peak Interval Indicator
# ----------------------------------------------------------

peak_threshold = activity.quantile(0.90)

df["Peak_Interval"] = (
    activity >= peak_threshold
).astype(int)

# ----------------------------------------------------------
# Peak Strain Duration
# ----------------------------------------------------------

df["Peak_Group"] = (
    df["Peak_Interval"] !=
    df["Peak_Interval"].shift()
).cumsum()

peak_duration = (
    df[df["Peak_Interval"] == 1]
    .groupby("Peak_Group")
    .size()
)

max_peak_duration = (
    peak_duration.max()
    if len(peak_duration) > 0
    else 0
)

# ----------------------------------------------------------
# Operational Variability Score
# ----------------------------------------------------------

ovs = (
    activity.std() /
    activity.mean()
)

# ----------------------------------------------------------
# Redemption Efficiency
# ----------------------------------------------------------

df["Redemption_Efficiency"] = (
    df["Redemption_Count"] /
    (activity + 1)
)

# ----------------------------------------------------------
# Hourly KPI
# ----------------------------------------------------------

hourly = (
    df.groupby("Hour")
    .agg(
        Average_Load=("Operational_Load_Index","mean"),
        Average_CPI=("Congestion_Pressure_Index","mean"),
        Idle_Rate=("Idle_Capacity","mean"),
        Peak_Rate=("Peak_Interval","mean"),
        Avg_Sales=("Sales_Count","mean"),
        Avg_Redemption=("Redemption_Count","mean")
    )
    .reset_index()
)

# ----------------------------------------------------------
# Daily KPI
# ----------------------------------------------------------

daily = (
    df.groupby(df["Timestamp"].dt.date)
    .agg(
        Total_Sales=("Sales_Count","sum"),
        Total_Redemption=("Redemption_Count","sum"),
        Average_CPI=("Congestion_Pressure_Index","mean"),
        Average_OLI=("Operational_Load_Index","mean")
    )
    .reset_index()
)

# ----------------------------------------------------------
# Monthly KPI
# ----------------------------------------------------------

monthly = (
    df.groupby("Month_Name")
    .agg(
        Average_Load=("Operational_Load_Index","mean"),
        Average_CPI=("Congestion_Pressure_Index","mean"),
        Idle_Rate=("Idle_Capacity","mean"),
        Peak_Rate=("Peak_Interval","mean")
    )
)

month_order = [
    "January","February","March","April",
    "May","June","July","August",
    "September","October","November","December"
]

monthly = monthly.reindex(month_order)

# ----------------------------------------------------------
# Seasonal KPI
# ----------------------------------------------------------

seasonal = (
    df.groupby("Season")
    .agg(
        Avg_Load=("Operational_Load_Index","mean"),
        Avg_CPI=("Congestion_Pressure_Index","mean"),
        Avg_CUR=("Capacity_Utilization_Ratio","mean"),
        Idle_Rate=("Idle_Capacity","mean")
    )
)

# ----------------------------------------------------------
# Weekend KPI
# ----------------------------------------------------------

weekend = (
    df.groupby("Weekend")
    .agg(
        Avg_Load=("Operational_Load_Index","mean"),
        Avg_CPI=("Congestion_Pressure_Index","mean"),
        Avg_CUR=("Capacity_Utilization_Ratio","mean")
    )
)

# ----------------------------------------------------------
# Overall KPI Dashboard
# ----------------------------------------------------------

dashboard = pd.DataFrame({

    "KPI":[
        "Average Capacity Utilization Ratio",
        "Average Operational Load Index",
        "Average Congestion Pressure Index",
        "Idle Capacity Percentage",
        "Peak Interval Percentage",
        "Peak Strain Duration",
        "Operational Variability Score",
        "Average Sales",
        "Average Redemption",
        "Average Total Activity"
    ],

    "Value":[

        round(df["Capacity_Utilization_Ratio"].mean(),3),

        round(df["Operational_Load_Index"].mean(),3),

        round(df["Congestion_Pressure_Index"].mean(),3),

        round(df["Idle_Capacity"].mean()*100,2),

        round(df["Peak_Interval"].mean()*100,2),

        max_peak_duration,

        round(ovs,3),

        round(df["Sales_Count"].mean(),2),

        round(df["Redemption_Count"].mean(),2),

        round(activity.mean(),2)
    ]

})

print("\nOverall KPI Dashboard")
print(dashboard)

# ----------------------------------------------------------
# Operational Status
# ----------------------------------------------------------

def classify(cpi):

    if cpi >= 0.80:
        return "Critical"

    elif cpi >= 0.60:
        return "High"

    elif cpi >= 0.40:
        return "Moderate"

    else:
        return "Low"

df["Operational_Status"] = (
    df["Congestion_Pressure_Index"]
    .apply(classify)
)

status_summary = (
    df["Operational_Status"]
    .value_counts()
)

print("\nOperational Status")
print(status_summary)

# ----------------------------------------------------------
# Save Outputs
# ----------------------------------------------------------

dashboard.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\KPI_Dashboard.csv",
    index=False
)

hourly.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Hourly_KPI.csv",
    index=False
)

daily.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Daily_KPI.csv",
    index=False
)

monthly.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Monthly_KPI.csv"
)

seasonal.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Seasonal_KPI.csv"
)

weekend.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Weekend_KPI.csv"
)

df.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Operational_KPI_Data.csv",
    index=False
)

print("\nFiles Saved Successfully")

print("KPI_Dashboard.csv")
print("Hourly_KPI.csv")
print("Daily_KPI.csv")
print("Monthly_KPI.csv")
print("Seasonal_KPI.csv")
print("Weekend_KPI.csv")
print("Operational_KPI_Data.csv")

print("\nKPI ANALYTICS COMPLETED SUCCESSFULLY")