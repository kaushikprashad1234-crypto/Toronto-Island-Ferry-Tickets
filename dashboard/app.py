import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# ---------------------------------------------------
# Page Configuration
# ---------------------------------------------------

st.set_page_config(
    page_title="Ferry Capacity Utilization Analytics",
    page_icon="⛴️",
    layout="wide"
)

st.title("⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics")
st.markdown("Toronto Government Parks, Forestry & Recreation")

# ---------------------------------------------------
# Load Data
# ---------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv(
        "E:\\power bi\\Toronto Island Ferry Tickets\\data\\Processed_Ferry_Data.csv",
        parse_dates=["Timestamp"]
    )
    return df

df = load_data()

# ---------------------------------------------------
# Sidebar Filters
# ---------------------------------------------------

st.sidebar.header("Filters")

years = sorted(df["Year"].unique())

selected_year = st.sidebar.multiselect(
    "Select Year",
    years,
    default=years
)

seasons = sorted(df["Season"].unique())

selected_season = st.sidebar.multiselect(
    "Season",
    seasons,
    default=seasons
)

time_band = sorted(df["Time_Band"].unique())

selected_band = st.sidebar.multiselect(
    "Time Band",
    time_band,
    default=time_band
)

filtered = df[
    (df["Year"].isin(selected_year)) &
    (df["Season"].isin(selected_season)) &
    (df["Time_Band"].isin(selected_band))
]

# ---------------------------------------------------
# KPI Cards
# ---------------------------------------------------

activity = filtered["Total_Activity_Load"]

cur = filtered["Capacity_Utilization_Ratio"].mean()

oli = filtered["Operational_Load_Index"].mean()

cpi = filtered["Congestion_Pressure_Index"].mean()

idle = filtered["Idle_Capacity"].mean()*100

peak = filtered["Peak_Interval"].mean()*100

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric(
    "Capacity Utilization",
    f"{cur:.2f}"
)

c2.metric(
    "Operational Load",
    f"{oli:.2f}"
)

c3.metric(
    "Congestion Index",
    f"{cpi:.2f}"
)

c4.metric(
    "Idle Capacity %",
    f"{idle:.1f}%"
)

c5.metric(
    "Peak Interval %",
    f"{peak:.1f}%"
)

st.divider()

# ---------------------------------------------------
# Timeline
# ---------------------------------------------------

st.subheader("Activity Timeline")

fig = px.line(
    filtered,
    x="Timestamp",
    y="Total_Activity_Load"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Hourly Trend
# ---------------------------------------------------

hourly = filtered.groupby("Hour")[
    "Total_Activity_Load"
].mean().reset_index()

fig = px.line(
    hourly,
    x="Hour",
    y="Total_Activity_Load",
    markers=True
)

st.subheader("Hourly Utilization")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Monthly Activity
# ---------------------------------------------------

monthly = filtered.groupby("Month_Name")[
    "Total_Activity_Load"
].mean().reset_index()

order = [
    "January","February","March",
    "April","May","June",
    "July","August","September",
    "October","November","December"
]

monthly["Month_Name"] = pd.Categorical(
    monthly["Month_Name"],
    order
)

monthly = monthly.sort_values("Month_Name")

fig = px.bar(
    monthly,
    x="Month_Name",
    y="Total_Activity_Load"
)

st.subheader("Monthly Activity")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Season Comparison
# ---------------------------------------------------

season = filtered.groupby("Season")[
    "Total_Activity_Load"
].mean().reset_index()

fig = px.bar(
    season,
    x="Season",
    y="Total_Activity_Load",
    color="Season"
)

st.subheader("Season Comparison")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Weekend Comparison
# ---------------------------------------------------

week = filtered.groupby("Weekend")[
    "Total_Activity_Load"
].mean().reset_index()

week["Weekend"] = week["Weekend"].map({
    False:"Weekday",
    True:"Weekend"
})

fig = px.pie(
    week,
    names="Weekend",
    values="Total_Activity_Load"
)

st.subheader("Weekend vs Weekday")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Congestion Scatter
# ---------------------------------------------------

fig = px.scatter(
    filtered,
    x="Operational_Load_Index",
    y="Congestion_Pressure_Index",
    color="Season"
)

st.subheader("Congestion Analysis")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Peak Intervals
# ---------------------------------------------------

peak_df = filtered[
    filtered["Peak_Interval"]==1
]

st.subheader("Peak Intervals")

st.dataframe(
    peak_df[
        [
            "Timestamp",
            "Sales_Count",
            "Redemption_Count",
            "Congestion_Pressure_Index"
        ]
    ]
)

# ---------------------------------------------------
# Idle Capacity
# ---------------------------------------------------

idle_df = filtered[
    filtered["Idle_Capacity"]==1
]

st.subheader("Idle Capacity")

st.dataframe(
    idle_df[
        [
            "Timestamp",
            "Sales_Count",
            "Redemption_Count",
            "Total_Activity_Load"
        ]
    ]
)

# ---------------------------------------------------
# Correlation Heatmap
# ---------------------------------------------------

corr = filtered[
[
"Sales_Count",
"Redemption_Count",
"Total_Activity_Load",
"Operational_Load_Index",
"Capacity_Utilization_Ratio",
"Congestion_Pressure_Index"
]
].corr()

fig = go.Figure(
    data=go.Heatmap(
        z=corr.values,
        x=corr.columns,
        y=corr.columns
    )
)

st.subheader("Correlation Heatmap")

st.plotly_chart(
    fig,
    use_container_width=True
)

# ---------------------------------------------------
# Raw Dataset
# ---------------------------------------------------

st.subheader("Processed Dataset")

st.dataframe(filtered)

# ---------------------------------------------------
# Download Button
# ---------------------------------------------------

csv = filtered.to_csv(index=False)

st.download_button(
    "Download Filtered Data",
    csv,
    "Filtered_Ferry_Data.csv",
    "text/csv"
)

# ---------------------------------------------------
# Footer
# ---------------------------------------------------

st.success("Dashboard Loaded Successfully")