# ==========================================================
# PART 2 : EXPLORATORY DATA ANALYSIS (EDA)
# Ferry Capacity Utilization & Operational Efficiency
# ==========================================================

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ----------------------------------------------------------
# Load Processed Dataset
# ----------------------------------------------------------

df = pd.read_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv",
    parse_dates=["Timestamp"]
)

print("="*60)
print("EDA STARTED")
print("="*60)

# ----------------------------------------------------------
# Dataset Information
# ----------------------------------------------------------

print("\nDataset Shape")
print(df.shape)

print("\nDataset Info")
print(df.info())

print("\nSummary Statistics")
print(df.describe())

print("\nMissing Values")
print(df.isnull().sum())

print("\nDuplicate Rows")
print(df.duplicated().sum())

# ----------------------------------------------------------
# Correlation Matrix
# ----------------------------------------------------------

numeric = df.select_dtypes(include=np.number)

corr = numeric.corr()

plt.figure(figsize=(10,8))
plt.imshow(corr, cmap="coolwarm")
plt.colorbar()

plt.xticks(range(len(corr.columns)),
           corr.columns,
           rotation=90)

plt.yticks(range(len(corr.columns)),
           corr.columns)

plt.title("Correlation Matrix")

plt.tight_layout()
plt.show()

# ----------------------------------------------------------
# Sales Distribution
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Sales_Count"],
    bins=40
)

plt.title("Sales Count Distribution")
plt.xlabel("Sales Count")
plt.ylabel("Frequency")

plt.show()

# ----------------------------------------------------------
# Redemption Distribution
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Redemption_Count"],
    bins=40
)

plt.title("Redemption Count Distribution")
plt.xlabel("Redemption Count")
plt.ylabel("Frequency")

plt.show()

# ----------------------------------------------------------
# Total Activity Distribution
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

plt.hist(
    df["Total_Activity_Load"],
    bins=40
)

plt.title("Total Activity Load")
plt.xlabel("Activity")

plt.show()

# ----------------------------------------------------------
# Time Series
# ----------------------------------------------------------

plt.figure(figsize=(15,5))

plt.plot(
    df["Timestamp"],
    df["Total_Activity_Load"]
)

plt.title("15-Minute Activity Timeline")

plt.xlabel("Date")
plt.ylabel("Activity")

plt.show()

# ----------------------------------------------------------
# Daily Activity
# ----------------------------------------------------------

daily = df.groupby(
    df["Timestamp"].dt.date
)["Total_Activity_Load"].sum()

plt.figure(figsize=(15,5))

plt.plot(
    daily.index,
    daily.values
)

plt.title("Daily Activity")

plt.show()

# ----------------------------------------------------------
# Monthly Activity
# ----------------------------------------------------------

monthly = df.groupby("Month")[
    "Total_Activity_Load"
].mean()

plt.figure(figsize=(8,5))

plt.bar(
    monthly.index.astype(str),
    monthly.values
)

plt.title("Average Monthly Activity")

plt.xlabel("Month")
plt.ylabel("Average Activity")

plt.show()

# ----------------------------------------------------------
# Yearly Trend
# ----------------------------------------------------------

yearly = df.groupby("Year")[
    "Total_Activity_Load"
].mean()

plt.figure(figsize=(8,5))

plt.plot(
    yearly.index,
    yearly.values,
    marker="o"
)

plt.title("Yearly Average Activity")

plt.show()

# ----------------------------------------------------------
# Hourly Pattern
# ----------------------------------------------------------

hourly = df.groupby("Hour")[
    "Total_Activity_Load"
].mean()

plt.figure(figsize=(10,5))

plt.plot(
    hourly.index,
    hourly.values,
    marker="o"
)

plt.title("Average Hourly Activity")

plt.xlabel("Hour")

plt.show()

# ----------------------------------------------------------
# Weekday Comparison
# ----------------------------------------------------------

weekday = df.groupby("Weekday")[
    "Total_Activity_Load"
].mean()

order = [
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
]

weekday = weekday.reindex(order)

plt.figure(figsize=(10,5))

plt.bar(
    weekday.index,
    weekday.values
)

plt.xticks(rotation=45)

plt.title("Weekday Activity")

plt.show()

# ----------------------------------------------------------
# Weekend vs Weekday
# ----------------------------------------------------------

weekend = df.groupby("Weekend")[
    "Total_Activity_Load"
].mean()

plt.figure(figsize=(5,5))

plt.bar(
    ["Weekday","Weekend"],
    weekend.values
)

plt.title("Weekend vs Weekday")

plt.show()

# ----------------------------------------------------------
# Seasonal Activity
# ----------------------------------------------------------

season = df.groupby("Season")[
    "Total_Activity_Load"
].mean()

season = season.reindex(
    ["Winter","Spring","Summer","Fall"]
)

plt.figure(figsize=(8,5))

plt.bar(
    season.index,
    season.values
)

plt.title("Seasonal Activity")

plt.show()

# ----------------------------------------------------------
# Time Band
# ----------------------------------------------------------

band = df.groupby("Time_Band")[
    "Total_Activity_Load"
].mean()

band = band.reindex(
    ["Morning","Afternoon","Evening","Night"]
)

plt.figure(figsize=(8,5))

plt.bar(
    band.index,
    band.values
)

plt.title("Activity by Time Band")

plt.show()

# ----------------------------------------------------------
# Boxplot
# ----------------------------------------------------------

plt.figure(figsize=(8,5))

plt.boxplot(
    df["Total_Activity_Load"],
    vert=True
)

plt.title("Boxplot - Total Activity")

plt.show()

# ----------------------------------------------------------
# Operational Load Index
# ----------------------------------------------------------

plt.figure(figsize=(12,5))

plt.plot(
    df["Timestamp"],
    df["Operational_Load_Index"]
)

plt.title("Operational Load Index")

plt.show()

# ----------------------------------------------------------
# Congestion Pressure Index
# ----------------------------------------------------------

plt.figure(figsize=(12,5))

plt.plot(
    df["Timestamp"],
    df["Congestion_Pressure_Index"]
)

plt.title("Congestion Pressure Index")

plt.show()

# ----------------------------------------------------------
# Idle Capacity Percentage
# ----------------------------------------------------------

idle = (
    df["Idle_Capacity"].value_counts(normalize=True)
    *100
)

plt.figure(figsize=(5,5))

plt.pie(
    idle.values,
    labels=["Active","Idle"],
    autopct="%.1f%%"
)

plt.title("Idle Capacity Percentage")

plt.show()

# ----------------------------------------------------------
# Peak Interval Percentage
# ----------------------------------------------------------

peak = (
    df["Peak_Interval"].value_counts(normalize=True)
    *100
)

plt.figure(figsize=(5,5))

plt.pie(
    peak.values,
    labels=["Normal","Peak"],
    autopct="%.1f%%"
)

plt.title("Peak Interval Percentage")

plt.show()

# ----------------------------------------------------------
# Rolling Load
# ----------------------------------------------------------

plt.figure(figsize=(15,5))

plt.plot(
    df["Timestamp"],
    df["Rolling_Load"]
)

plt.title("Rolling Average Activity")

plt.show()

# ----------------------------------------------------------
# Top 20 Congested Intervals
# ----------------------------------------------------------

top = df.nlargest(
    20,
    "Congestion_Pressure_Index"
)

plt.figure(figsize=(12,5))

plt.bar(
    range(len(top)),
    top["Congestion_Pressure_Index"]
)

plt.title("Top 20 Congested Intervals")

plt.show()

# ----------------------------------------------------------
# Lowest Activity Intervals
# ----------------------------------------------------------

low = df.nsmallest(
    20,
    "Total_Activity_Load"
)

plt.figure(figsize=(12,5))

plt.bar(
    range(len(low)),
    low["Total_Activity_Load"]
)

plt.title("Lowest Activity Intervals")

plt.show()

# ----------------------------------------------------------
# KPI Summary
# ----------------------------------------------------------

print("\n================ KPI SUMMARY ================")

print("Average Sales :",
      round(df["Sales_Count"].mean(),2))

print("Average Redemption :",
      round(df["Redemption_Count"].mean(),2))

print("Average Activity :",
      round(df["Total_Activity_Load"].mean(),2))

print("Average Operational Load Index :",
      round(df["Operational_Load_Index"].mean(),3))

print("Average Congestion Pressure :",
      round(df["Congestion_Pressure_Index"].mean(),3))

print("Idle Capacity % :",
      round(df["Idle_Capacity"].mean()*100,2))

print("Peak Interval % :",
      round(df["Peak_Interval"].mean()*100,2))

print("\nEDA COMPLETED SUCCESSFULLY")