# ⛴️ Ferry Capacity Utilization & Operational Efficiency Analytics System

## 📌 Project Overview

The **Ferry Capacity Utilization & Operational Efficiency Analytics System** is an end-to-end data analytics project developed to evaluate the operational performance of the **Toronto Island Ferry System** using historical ticket sales and redemption data.

The project transforms raw operational records into actionable insights through data preprocessing, exploratory data analysis (EDA), statistical analysis, feature engineering, interactive visualization, and business intelligence dashboards. It enables transportation authorities to monitor capacity utilization, identify congestion-prone periods, detect idle-capacity windows, and support evidence-based operational planning.

---

# 🎯 Problem Statement

The Toronto Island Ferry operates under fixed vessel capacities, staffing constraints, and significant seasonal demand fluctuations. Although historical ticket sales and redemption data are available, there is no structured analytical framework to:

* Measure ferry capacity utilization.
* Detect congestion-prone operating periods.
* Identify underutilized service intervals.
* Evaluate operational efficiency across seasons.
* Support data-driven scheduling and resource allocation.

This project addresses these challenges by developing a comprehensive operational analytics system.

---

# 🎯 Objectives

## Primary Objectives

* Quantify ferry capacity utilization.
* Measure operational efficiency using ticket activity.
* Identify congestion and idle-capacity periods.
* Develop operational Key Performance Indicators (KPIs).

## Secondary Objectives

* Analyze seasonal utilization patterns.
* Compare weekday and weekend operations.
* Support strategic planning and resource optimization.
* Build an interactive Streamlit dashboard.

---

# 📂 Dataset Information

**Organization:** Toronto Government Parks, Forestry & Recreation

**Time Period:** 2015–2025

**Granularity:** 15-minute intervals

### Dataset Columns

| Column             | Description                      |
| ------------------ | -------------------------------- |
| `_id`              | Unique record identifier         |
| `Timestamp`        | 15-minute interval timestamp     |
| `Sales Count`      | Tickets sold during the interval |
| `Redemption Count` | Tickets redeemed during boarding |

---

# 🛠️ Technology Stack

| Technology       | Purpose               |
| ---------------- | --------------------- |
| Python           | Programming language  |
| Pandas           | Data preprocessing    |
| NumPy            | Numerical computation |
| Matplotlib       | Data visualization    |
| Plotly           | Interactive charts    |
| SciPy            | Statistical analysis  |
| Streamlit        | Dashboard development |
| Jupyter Notebook | Data analysis         |
| GitHub           | Version control       |

---

# 📊 Project Workflow

```
Raw Dataset
      │
      ▼
Data Cleaning
      │
      ▼
Feature Engineering
      │
      ▼
Exploratory Data Analysis
      │
      ▼
Statistical Analysis
      │
      ▼
Operational KPIs
      │
      ▼
Interactive Dashboard
      │
      ▼
Business Insights
```

---

# ⚙️ Feature Engineering

The following operational features were created:

* Total Activity Load
* Redemption Pressure Ratio
* Capacity Utilization Ratio (CUR)
* Operational Load Index (OLI)
* Congestion Pressure Index (CPI)
* Idle Capacity Indicator
* Peak Interval Indicator
* Rolling Average Activity
* Seasonal Classification
* Weekend Indicator
* Time Band Classification

---

# 📈 Key Performance Indicators (KPIs)

The dashboard calculates the following KPIs:

* Capacity Utilization Ratio
* Operational Load Index
* Congestion Pressure Index
* Idle Capacity Percentage
* Peak Strain Duration
* Operational Variability Score
* Redemption Efficiency

---

# 📊 Exploratory Data Analysis

The project includes comprehensive EDA covering:

* Dataset overview
* Missing-value analysis
* Descriptive statistics
* Distribution analysis
* Time-series visualization
* Hourly activity analysis
* Daily trends
* Monthly trends
* Seasonal comparison
* Weekday vs. Weekend comparison
* Correlation heatmap
* Outlier detection
* Rolling average trends

---

# 📉 Statistical Analysis

The following statistical techniques were applied:

* Descriptive Statistics
* Pearson Correlation
* Spearman Correlation
* Shapiro–Wilk Normality Test
* Independent Sample t-Test
* One-Way ANOVA
* Confidence Interval Estimation
* Z-Score Analysis
* IQR Outlier Detection

---

# 📊 Dashboard Features

The Streamlit dashboard includes:

* KPI Summary Cards
* Capacity Utilization Timeline
* Hourly Utilization Analysis
* Seasonal Comparison
* Monthly Activity Analysis
* Weekend vs. Weekday Analysis
* Congestion Scatter Plot
* Correlation Heatmap
* Peak Interval Detection
* Idle Capacity Analysis
* Interactive Filters
* Downloadable Reports

---

# 📁 Project Structure

```
Ferry-Capacity-Analytics/
│
├── data/
│   ├── Ferry_Data.csv
│   └── Processed_Ferry_Data.csv
│
├── notebooks/
│   ├── Part1_Data_Preprocessing.ipynb
│   ├── Part2_EDA.ipynb
│   ├── Part3_Statistical_Analysis.ipynb
│   ├── Part4_Feature_Engineering.ipynb
│   └── Part5_KPI_Analysis.ipynb
│
├── dashboard/
│   └── app.py
│
├── report/
│   ├── Research_Paper.pdf
│   ├── Executive_Summary.pdf
│  
│
├── requirements.txt
├── README.md
└── LICENSE
```

---

# 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/Ferry-Capacity-Analytics.git

cd Ferry-Capacity-Analytics
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the Streamlit application:

```bash
streamlit run app.py
```

---

# 📊 Dashboard Preview

The dashboard provides:

* Operational KPI cards
* Interactive filters
* Time-series visualizations
* Seasonal comparisons
* Congestion monitoring
* Idle-capacity detection
* Downloadable filtered datasets

---

# 💡 Key Business Insights

The analysis identified several operational findings:

* Passenger demand follows predictable hourly and seasonal patterns.
* Summer operations experience the highest utilization levels.
* Congestion occurs during recurring operating windows.
* Off-peak periods exhibit significant idle capacity.
* Historical ticket activity is an effective indicator of operational demand.
* Data-driven scheduling can improve service efficiency and passenger experience.

---

# 📌 Recommendations

Based on the analysis:

* Adopt demand-responsive ferry scheduling.
* Develop season-specific operational plans.
* Monitor KPIs continuously.
* Optimize staffing based on utilization patterns.
* Reduce unnecessary service during low-demand periods.
* Expand analytics with predictive forecasting and real-time monitoring.

---

# 📚 Deliverables

* ✅ Data preprocessing pipeline
* ✅ Feature engineering
* ✅ Exploratory Data Analysis (EDA)
* ✅ Statistical analysis
* ✅ Operational KPI framework
* ✅ Streamlit dashboard
* ✅ Research paper
* ✅ Executive summary
* ✅ GitHub documentation

---

# 🔮 Future Enhancements

Potential improvements include:

* Machine learning demand forecasting
* Real-time dashboard integration
* Weather-based operational optimization
* GIS route visualization
* Predictive congestion alerts
* Vessel occupancy estimation
* Fuel consumption analytics
* AI-assisted scheduling recommendations

---

# 👨‍💻 Author

**Kaushik Prasad**

Data Analytics Project

Toronto Government Parks, Forestry & Recreation (Case Study)

---

# 📄 License

This project is developed for **educational, research, and portfolio purposes**. The analytical framework and source code may be adapted for learning and non-commercial use with appropriate attribution.

---

## ⭐ Acknowledgements

This project demonstrates how operational analytics can transform historical transportation data into actionable insights for public sector decision-making. By integrating data engineering, statistical analysis, visualization, and interactive dashboards, it provides a scalable framework for improving ferry capacity utilization, operational efficiency, and long-term transportation planning.
