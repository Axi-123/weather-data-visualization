import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import IsolationForest

st.title("🌦️ Weather Data Visualization Dashboard")

# --- Generate Sample Dataset ---
dates = pd.date_range(start='2021-01-01', end='2021-12-31')
np.random.seed(0)
df = pd.DataFrame({
    "Date": dates,
    "Min Temp": np.random.randint(15,25,len(dates)),
    "Max Temp": np.random.randint(20,35,len(dates)),
    "Humidity": np.random.randint(40,90,len(dates)),
    "Rainfall": np.random.randint(0,20,len(dates)),
    "Wind Speed": np.random.randint(5,20,len(dates))
})

# --- Sidebar Controls ---
st.sidebar.header("Filters")
show_temp = st.sidebar.checkbox("Show Temperature Trend", True)
show_rainfall = st.sidebar.checkbox("Show Rainfall Distribution", True)
show_humidity = st.sidebar.checkbox("Show Humidity Boxplot", False)
show_correlation = st.sidebar.checkbox("Show Correlation Heatmap", False)
show_anomalies = st.sidebar.checkbox("Show Anomaly Detection", False)

# --- Temperature Trend ---
if show_temp:
    st.subheader("🌡️ Temperature Trend")
    st.line_chart(df.set_index("Date")[["Min Temp","Max Temp"]])

# --- Rainfall Distribution ---
if show_rainfall:
    st.subheader("🌧️ Rainfall Distribution")
    fig, ax = plt.subplots()
    sns.histplot(df["Rainfall"], bins=30, kde=True, ax=ax)
    st.pyplot(fig)

# --- Humidity Boxplot ---
if show_humidity:
    st.subheader("💧 Humidity Boxplot")
    fig2, ax2 = plt.subplots()
    sns.boxplot(y=df["Humidity"], ax=ax2)
    st.pyplot(fig2)

# --- Correlation Heatmap ---
if show_correlation:
    st.subheader("📊 Correlation Between Variables")
    corr = df[["Min Temp","Max Temp","Humidity","Rainfall","Wind Speed"]].corr()
    fig3, ax3 = plt.subplots()
    sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax3)
    st.pyplot(fig3)

# --- Anomaly Detection ---
if show_anomalies:
    st.subheader("⚠️ Unusual Weather Days (Anomalies)")
    iso = IsolationForest(contamination=0.02)
    df["Anomaly"] = iso.fit_predict(df[["Max Temp","Min Temp","Humidity","Rainfall"]])
    anomalies = df[df["Anomaly"]==-1]
    st.dataframe(anomalies[["Date","Max Temp","Min Temp","Humidity","Rainfall"]])
