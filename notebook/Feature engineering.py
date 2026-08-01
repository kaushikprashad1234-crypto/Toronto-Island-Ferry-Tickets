# ============================================================
# PART 4 : FEATURE ENGINEERING
# Ferry Capacity Utilization & Operational Efficiency Analytics
# ============================================================

import pandas as pd
import numpy as np

# ------------------------------------------------------------
# Load Processed Dataset
# ------------------------------------------------------------
df = pd.read_csv("E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv")

# Remove leading/trailing spaces from column names
df.columns = df.columns.str.strip()

# Print all column names
print("\nColumns in dataset:")
print(df.columns.tolist())

df["Timestamp"] = pd.to_datetime(df["Timestamp"])
print("\nDataset Loaded Successfully")
print(df.head())

# ------------------------------------------------------------
# Basic Time Features
# ------------------------------------------------------------

df["Year"] = df["Timestamp"].dt.year
df["Month"] = df["Timestamp"].dt.month
df["Month_Name"] = df["Timestamp"].dt.month_name()

df["Day"] = df["Timestamp"].dt.day
df["Week"] = df["Timestamp"].dt.isocalendar().week.astype(int)

df["Day_Name"] = df["Timestamp"].dt.day_name()
df["Hour"] = df["Timestamp"].dt.hour
df["Minute"] = df["Timestamp"].dt.minute

# ------------------------------------------------------------
# Weekend Indicator
# ------------------------------------------------------------

df["Is_Weekend"] = df["Day_Name"].isin(
    ["Saturday", "Sunday"]
).astype(int)

# ------------------------------------------------------------
# Season Classification
# ------------------------------------------------------------

def season(month):

    if month in [12, 1, 2]:
        return "Winter"

    elif month in [3, 4, 5]:
        return "Spring"

    elif month in [6, 7, 8]:
        return "Summer"

    else:
        return "Autumn"

df["Season"] = df["Month"].apply(season)

# ------------------------------------------------------------
# Time Band
# ------------------------------------------------------------

def time_band(hour):

    if 5 <= hour < 12:
        return "Morning"

    elif 12 <= hour < 17:
        return "Afternoon"

    elif 17 <= hour < 21:
        return "Evening"

    else:
        return "Night"

df["Time_Band"] = df["Hour"].apply(time_band)

# ------------------------------------------------------------
# Total Activity Load
# ------------------------------------------------------------

df["Total_Activity"] = (
    df["Sales_Count"] +
    df["Redemption_Count"]
)

# ------------------------------------------------------------
# Redemption Pressure Ratio
# ------------------------------------------------------------

df["Redemption_Pressure"] = (
    df["Redemption_Count"] /
    (df["Sales_Count"] + 1)
)

# ------------------------------------------------------------
# Capacity Utilization Ratio
# ------------------------------------------------------------

max_activity = df["Total_Activity"].max()

df["Capacity_Utilization"] = (
    df["Total_Activity"] /
    max_activity
)

# ------------------------------------------------------------
# Operational Load Index (Normalized)
# ------------------------------------------------------------

min_load = df["Total_Activity"].min()
max_load = df["Total_Activity"].max()

df["Operational_Load_Index"] = (
    (df["Total_Activity"] - min_load) /
    (max_load - min_load)
)

# ------------------------------------------------------------
# Congestion Pressure Index
# ------------------------------------------------------------

df["Congestion_Pressure_Index"] = (
    df["Operational_Load_Index"] *
    df["Redemption_Pressure"]
)

# ------------------------------------------------------------
# Idle Capacity Indicator
# ------------------------------------------------------------

threshold = df["Total_Activity"].quantile(0.25)

df["Idle_Capacity"] = np.where(
    df["Total_Activity"] <= threshold,
    1,
    0
)

# ------------------------------------------------------------
# Peak Interval Indicator
# ------------------------------------------------------------

peak_threshold = df["Total_Activity"].quantile(0.90)

df["Peak_Interval"] = np.where(
    df["Total_Activity"] >= peak_threshold,
    1,
    0
)

# ------------------------------------------------------------
# Rolling Average Activity
# ------------------------------------------------------------

df = df.sort_values("Timestamp")

df["Rolling_Activity"] = (
    df["Total_Activity"]
      .rolling(window=4, min_periods=1)
      .mean()
)

# ------------------------------------------------------------
# Activity Growth Rate
# ------------------------------------------------------------

df["Activity_Growth"] = (
    df["Total_Activity"]
      .pct_change()
      .fillna(0)
)

# ------------------------------------------------------------
# Lag Features
# ------------------------------------------------------------

df["Previous_Activity"] = (
    df["Total_Activity"]
      .shift(1)
      .fillna(0)
)

df["Next_Activity"] = (
    df["Total_Activity"]
      .shift(-1)
      .fillna(0)
)

# ------------------------------------------------------------
# Difference Feature
# ------------------------------------------------------------

df["Activity_Difference"] = (
    df["Sales_Count"] -
    df["Redemption_Count"]
)

# ------------------------------------------------------------
# Efficiency Score
# ------------------------------------------------------------

df["Efficiency_Score"] = (
    df["Capacity_Utilization"] *
    (1 - df["Idle_Capacity"])
)

# ------------------------------------------------------------
# Operational Variability
# ------------------------------------------------------------

df["Operational_Variability"] = (
    df["Total_Activity"]
      .rolling(window=8, min_periods=1)
      .std()
      .fillna(0)
)

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------

print("\nFeature Engineering Completed")

print("\nNew Columns")

new_cols = [
    "Year",
    "Month",
    "Month_Name",
    "Day",
    "Week",
    "Day_Name",
    "Hour",
    "Minute",
    "Season",
    "Time_Band",
    "Is_Weekend",
    "Total_Activity",
    "Redemption_Pressure",
    "Capacity_Utilization",
    "Operational_Load_Index",
    "Congestion_Pressure_Index",
    "Idle_Capacity",
    "Peak_Interval",
    "Rolling_Activity",
    "Activity_Growth",
    "Previous_Activity",
    "Next_Activity",
    "Activity_Difference",
    "Efficiency_Score",
    "Operational_Variability"
]

print(df[new_cols].head())

# ------------------------------------------------------------
# Save Dataset
# ------------------------------------------------------------

df.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Feature_Engineered_Ferry_Data.csv",
    index=False
)

print("\nFeature Engineered Dataset Saved Successfully")

print(df.shape)

print("=" * 70)
print("FEATURE ENGINEERING COMPLETED")
print("=" * 70)