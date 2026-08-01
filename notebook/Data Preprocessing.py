# ============================================================
# Ferry Capacity Utilization & Operational Efficiency Analytics
# ============================================================

# Import Libraries
import pandas as pd
import numpy as np

# ------------------------------------------------------------
# 1. Load Dataset
# ------------------------------------------------------------

file_path = "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Toronto Island Ferry Tickets.csv"

df = pd.read_csv(file_path)

print("=" * 60)
print("Dataset Loaded Successfully")
print("=" * 60)

print(df.head())

# ------------------------------------------------------------
# 2. Dataset Overview
# ------------------------------------------------------------

print("\nShape:", df.shape)

print("\nColumns")
print(df.columns)

print("\nData Types")
print(df.dtypes)

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

# ------------------------------------------------------------
# 3. Convert Timestamp
# ------------------------------------------------------------

df["Timestamp"] = pd.to_datetime(df["Timestamp"])

# Sort dataset

df = df.sort_values("Timestamp").reset_index(drop=True)

# ------------------------------------------------------------
# 4. Rename Columns (optional)
# ------------------------------------------------------------

df.columns = [
    "ID",
    "Timestamp",
    "Sales_Count",
    "Redemption_Count"
]

# ------------------------------------------------------------
# 5. Remove Negative Values
# ------------------------------------------------------------

df = df[
    (df["Sales_Count"] >= 0) &
    (df["Redemption_Count"] >= 0)
]

# ------------------------------------------------------------
# 6. Time Features
# ------------------------------------------------------------

df["Year"] = df["Timestamp"].dt.year
df["Month"] = df["Timestamp"].dt.month
df["Month_Name"] = df["Timestamp"].dt.month_name()

df["Day"] = df["Timestamp"].dt.day

df["Hour"] = df["Timestamp"].dt.hour

df["Minute"] = df["Timestamp"].dt.minute

df["Weekday"] = df["Timestamp"].dt.day_name()

df["Week_Number"] = df["Timestamp"].dt.isocalendar().week

df["Quarter"] = df["Timestamp"].dt.quarter

# Weekend Indicator

df["Weekend"] = df["Weekday"].isin(
    ["Saturday", "Sunday"]
)

# ------------------------------------------------------------
# 7. Season Classification
# ------------------------------------------------------------

def season(month):

    if month in [12,1,2]:
        return "Winter"

    elif month in [3,4,5]:
        return "Spring"

    elif month in [6,7,8]:
        return "Summer"

    else:
        return "Fall"

df["Season"] = df["Month"].apply(season)

# ------------------------------------------------------------
# 8. Time Band
# ------------------------------------------------------------

def time_band(hour):

    if 5 <= hour < 12:
        return "Morning"

    elif 12 <= hour < 17:
        return "Afternoon"

    elif 17 <= hour < 22:
        return "Evening"

    else:
        return "Night"

df["Time_Band"] = df["Hour"].apply(time_band)

# ------------------------------------------------------------
# 9. Feature Engineering
# ------------------------------------------------------------

# Total Activity Load

df["Total_Activity_Load"] = (
    df["Sales_Count"] +
    df["Redemption_Count"]
)

# Redemption Pressure Ratio

df["Redemption_Pressure_Ratio"] = (
    df["Redemption_Count"] /
    (df["Sales_Count"] + 1)
)

# Operational Load Index

df["Operational_Load_Index"] = (
    (
        df["Total_Activity_Load"] -
        df["Total_Activity_Load"].min()
    )
    /
    (
        df["Total_Activity_Load"].max() -
        df["Total_Activity_Load"].min()
    )
)

# Capacity Utilization Ratio

df["Capacity_Utilization_Ratio"] = (
    df["Redemption_Count"] /
    (df["Sales_Count"] + 1)
)

# Congestion Pressure Index

df["Congestion_Pressure_Index"] = (
    0.6 * df["Operational_Load_Index"]
    +
    0.4 * df["Capacity_Utilization_Ratio"]
)

# Rolling Mean

df["Rolling_Load"] = (
    df["Total_Activity_Load"]
    .rolling(window=4, min_periods=1)
    .mean()
)

# Rolling Standard Deviation

df["Rolling_STD"] = (
    df["Total_Activity_Load"]
    .rolling(window=4, min_periods=1)
    .std()
)

# Idle Capacity Indicator

threshold = (
    df["Total_Activity_Load"]
    .quantile(0.25)
)

df["Idle_Capacity"] = np.where(
    df["Total_Activity_Load"] <= threshold,
    1,
    0
)

# Peak Indicator

peak_threshold = (
    df["Total_Activity_Load"]
    .quantile(0.90)
)

df["Peak_Interval"] = np.where(
    df["Total_Activity_Load"] >= peak_threshold,
    1,
    0
)

# ------------------------------------------------------------
# 10. Aggregate Hourly
# ------------------------------------------------------------

hourly_df = (
    df
    .set_index("Timestamp")
    .resample("h")
    .agg({
        "Sales_Count":"sum",
        "Redemption_Count":"sum",
        "Total_Activity_Load":"sum",
        "Operational_Load_Index":"mean",
        "Capacity_Utilization_Ratio":"mean",
        "Congestion_Pressure_Index":"mean"
    })
    .reset_index()
)

# ------------------------------------------------------------
# 11. Aggregate Daily
# ------------------------------------------------------------

daily_df = (
    df
    .set_index("Timestamp")
    .resample("D")
    .agg({
        "Sales_Count":"sum",
        "Redemption_Count":"sum",
        "Total_Activity_Load":"sum",
        "Operational_Load_Index":"mean",
        "Capacity_Utilization_Ratio":"mean",
        "Congestion_Pressure_Index":"mean"
    })
    .reset_index()
)

# ------------------------------------------------------------
# 12. Missing Interval Check
# ------------------------------------------------------------

full_range = pd.date_range(
    start=df["Timestamp"].min(),
    end=df["Timestamp"].max(),
    freq="15min"
)

missing_intervals = (
    len(full_range)
    -
    len(df["Timestamp"].unique())
)

print("\nMissing 15-Minute Intervals:", missing_intervals)

# ------------------------------------------------------------
# 13. Summary Statistics
# ------------------------------------------------------------

print("\nSummary Statistics")

print(df.describe())

# ------------------------------------------------------------
# 14. Save Processed Data
# ------------------------------------------------------------

df.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv",
    index=False
)

hourly_df.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Hourly_Ferry_Data.csv",
    index=False
)

daily_df.to_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Daily_Ferry_Data.csv",
    index=False
)

print("\nFiles Saved Successfully")

print("Processed_Ferry_Data.csv")
print("Hourly_Ferry_Data.csv")
print("Daily_Ferry_Data.csv")

print("\nProject preprocessing completed successfully.")