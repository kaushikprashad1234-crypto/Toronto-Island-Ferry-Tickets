# ==========================================================
# PART 3 : STATISTICAL ANALYSIS
# Ferry Capacity Utilization & Operational Efficiency
# ==========================================================

# Import Libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from scipy import stats
from scipy.stats import ttest_ind
from scipy.stats import f_oneway
from scipy.stats import pearsonr
from scipy.stats import spearmanr
from scipy.stats import shapiro
from scipy.stats import levene

# ----------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------

df = pd.read_csv(
    "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv",
    parse_dates=["Timestamp"]
)

print("="*60)
print("STATISTICAL ANALYSIS")
print("="*60)

# ----------------------------------------------------------
# Descriptive Statistics
# ----------------------------------------------------------

print("\nDescriptive Statistics")

print(df[
    [
        "Sales_Count",
        "Redemption_Count",
        "Total_Activity_Load",
        "Operational_Load_Index",
        "Congestion_Pressure_Index"
    ]
].describe())

# ----------------------------------------------------------
# Correlation Analysis
# ----------------------------------------------------------

print("\nCorrelation Matrix")

corr = df[
    [
        "Sales_Count",
        "Redemption_Count",
        "Total_Activity_Load",
        "Operational_Load_Index",
        "Capacity_Utilization_Ratio",
        "Congestion_Pressure_Index"
    ]
].corr()

print(corr)

# Pearson Correlation

r, p = pearsonr(
    df["Sales_Count"],
    df["Redemption_Count"]
)

print("\nPearson Correlation")
print("Coefficient :", round(r,4))
print("P-value :", p)

# Spearman Correlation

r2, p2 = spearmanr(
    df["Sales_Count"],
    df["Redemption_Count"]
)

print("\nSpearman Correlation")
print("Coefficient :", round(r2,4))
print("P-value :", p2)

# ----------------------------------------------------------
# Normality Test
# ----------------------------------------------------------

print("\nShapiro-Wilk Normality Test")

sample = df["Total_Activity_Load"].sample(
    min(5000, len(df)),
    random_state=42
)

stat, p = shapiro(sample)

print("Statistic :", stat)
print("P-value :", p)

if p > 0.05:
    print("Normally Distributed")
else:
    print("Not Normally Distributed")

# ----------------------------------------------------------
# Variance Homogeneity
# ----------------------------------------------------------

weekday = df[df["Weekend"] == False]["Total_Activity_Load"]
weekend = df[df["Weekend"] == True]["Total_Activity_Load"]

stat, p = levene(
    weekday,
    weekend
)

print("\nLevene Test")
print("Statistic :", stat)
print("P-value :", p)

# ----------------------------------------------------------
# Independent T-Test
# Weekday vs Weekend
# ----------------------------------------------------------

t, p = ttest_ind(
    weekday,
    weekend,
    equal_var=False
)

print("\nIndependent T-Test")

print("T Statistic :", t)
print("P-value :", p)

if p < 0.05:
    print("Significant Difference")
else:
    print("No Significant Difference")

# ----------------------------------------------------------
# ANOVA
# Seasonal Activity
# ----------------------------------------------------------

winter = df[df["Season"]=="Winter"]["Total_Activity_Load"]

spring = df[df["Season"]=="Spring"]["Total_Activity_Load"]

summer = df[df["Season"]=="Summer"]["Total_Activity_Load"]

fall = df[df["Season"]=="Fall"]["Total_Activity_Load"]

F,p = f_oneway(
    winter,
    spring,
    summer,
    fall
)

print("\nANOVA")

print("F Statistic :",F)
print("P-value :",p)

if p<0.05:
    print("Seasonal Difference Exists")
else:
    print("No Seasonal Difference")

# ----------------------------------------------------------
# Confidence Interval
# ----------------------------------------------------------

mean = df["Total_Activity_Load"].mean()

std = df["Total_Activity_Load"].std()

n = len(df)

margin = (
    1.96 *
    (std / np.sqrt(n))
)

lower = mean - margin
upper = mean + margin

print("\n95% Confidence Interval")

print(lower, upper)

# ----------------------------------------------------------
# Z Score Outliers
# ----------------------------------------------------------

z = np.abs(
    stats.zscore(
        df["Total_Activity_Load"]
    )
)

outliers = df[z > 3]

print("\nOutliers :", len(outliers))

# ----------------------------------------------------------
# IQR Outliers
# ----------------------------------------------------------

Q1 = df["Total_Activity_Load"].quantile(0.25)

Q3 = df["Total_Activity_Load"].quantile(0.75)

IQR = Q3-Q1

lower = Q1 - 1.5*IQR

upper = Q3 + 1.5*IQR

iqr_outliers = df[
    (df["Total_Activity_Load"]<lower) |
    (df["Total_Activity_Load"]>upper)
]

print("IQR Outliers :",len(iqr_outliers))

# ----------------------------------------------------------
# Monthly Trend
# ----------------------------------------------------------

monthly = df.groupby("Month")[
    "Total_Activity_Load"
].mean()

print("\nMonthly Average")

print(monthly)

# ----------------------------------------------------------
# Hourly Trend
# ----------------------------------------------------------

hourly = df.groupby("Hour")[
    "Total_Activity_Load"
].mean()

print("\nHourly Average")

print(hourly)

# ----------------------------------------------------------
# Weekday Trend
# ----------------------------------------------------------

weekday_avg = df.groupby(
    "Weekday"
)["Total_Activity_Load"].mean()

print("\nWeekday Average")

print(weekday_avg)

# ----------------------------------------------------------
# Peak Interval Statistics
# ----------------------------------------------------------

peak = df[df["Peak_Interval"]==1]

print("\nPeak Statistics")

print(peak[
    [
        "Sales_Count",
        "Redemption_Count",
        "Total_Activity_Load"
    ]
].describe())

# ----------------------------------------------------------
# Idle Capacity Statistics
# ----------------------------------------------------------

idle = df[df["Idle_Capacity"]==1]

print("\nIdle Statistics")

print(idle[
    [
        "Sales_Count",
        "Redemption_Count",
        "Total_Activity_Load"
    ]
].describe())

# ----------------------------------------------------------
# Linear Trend Analysis
# ----------------------------------------------------------

df["Time_Index"] = np.arange(len(df))

slope, intercept = np.polyfit(
    df["Time_Index"],
    df["Total_Activity_Load"],
    1
)

print("\nLinear Trend")

print("Slope :", slope)

if slope > 0:
    print("Increasing Operational Activity")
elif slope < 0:
    print("Decreasing Operational Activity")
else:
    print("No Trend")

# ----------------------------------------------------------
# Rolling Mean
# ----------------------------------------------------------

df["Rolling30"] = (
    df["Total_Activity_Load"]
    .rolling(30)
    .mean()
)

plt.figure(figsize=(15,5))

plt.plot(
    df["Timestamp"],
    df["Rolling30"]
)

plt.title("30-Interval Rolling Mean")

plt.xlabel("Time")

plt.ylabel("Activity")

plt.grid(True)

plt.show()

# ----------------------------------------------------------
# Summary Report
# ----------------------------------------------------------

print("\n==============================")
print("STATISTICAL SUMMARY")
print("==============================")

print("Average Activity:",
      round(df["Total_Activity_Load"].mean(),2))

print("Median Activity:",
      round(df["Total_Activity_Load"].median(),2))

print("Std Dev:",
      round(df["Total_Activity_Load"].std(),2))

print("Maximum Activity:",
      df["Total_Activity_Load"].max())

print("Minimum Activity:",
      df["Total_Activity_Load"].min())

print("Peak Interval %:",
      round(df["Peak_Interval"].mean()*100,2))

print("Idle Capacity %:",
      round(df["Idle_Capacity"].mean()*100,2))

print("Correlation Sales vs Redemption:",
      round(corr.loc["Sales_Count","Redemption_Count"],3))

print("\nSTATISTICAL ANALYSIS COMPLETED")