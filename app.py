import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Delhi Climate Visualization", layout="wide")

st.title("🌦️ Delhi Climate Data Visualization")
st.write("Analyze and smooth Delhi climate data using Moving Averages and Exponential Smoothing")

# --- Upload CSV ---
uploaded_file = st.file_uploader("Upload DailyDelhiClimateTrain.csv", type="csv")
if uploaded_file is not None:
    try:
        # Try reading with default comma separator
        df = pd.read_csv(uploaded_file)
    except pd.errors.ParserError:
        # If comma fails, try tab-separated
        df = pd.read_csv(uploaded_file, sep='\t', engine='python')
    
    # Preview dataset
    st.subheader("Dataset Preview")
    st.dataframe(df.head())

    # --- Convert date column ---
    if 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        df.set_index('date', inplace=True)
    else:
        st.error("No 'date' column found in CSV!")
        st.stop()

    # --- Select parameter ---
    if 'meantemp' not in df.columns:
        st.error("No 'meantemp' column found in CSV!")
        st.stop()

    option = 'meantemp'

    # --- Raw Temperature Plot ---
    st.subheader("Raw Temperature Data")
    st.line_chart(df[option])

    # --- Moving Averages ---
    st.subheader("Moving Average Smoothing")
    df['MA_7'] = df[option].rolling(window=7).mean()
    df['MA_30'] = df[option].rolling(window=30).mean()

    fig1, ax1 = plt.subplots(figsize=(10,5))
    ax1.plot(df.index, df[option], label="Raw Temperature", alpha=0.5)
    ax1.plot(df.index, df['MA_7'], label="7-day Moving Avg", color='orange')
    ax1.plot(df.index, df['MA_30'], label="30-day Moving Avg", color='red')
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Temperature (°C)")
    ax1.set_title("Moving Average Smoothing")
    ax1.legend()
    st.pyplot(fig1)

    # --- Exponential Smoothing ---
    st.subheader("Exponential Smoothing")
    df['Exp_Smooth'] = df[option].ewm(span=20, adjust=False).mean()

    fig2, ax2 = plt.subplots(figsize=(10,5))
    ax2.plot(df.index, df[option], label="Raw Temperature", alpha=0.5)
    ax2.plot(df.index, df['Exp_Smooth'], label="Exponential Smoothing", color='green')
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Temperature (°C)")
    ax2.set_title("Exponential Smoothing of Temperature")
    ax2.legend()
    st.pyplot(fig2)

    # --- Seasonal Trends (Monthly Average) ---
    st.subheader("Seasonal Trend (Monthly Average)")
    df['Month'] = df.index.month
    monthly_avg = df.groupby('Month')[option].mean()

    fig3, ax3 = plt.subplots(figsize=(8,5))
    ax3.plot(monthly_avg.index, monthly_avg.values, marker='o', color='purple')
    ax3.set_xlabel("Month")
    ax3.set_ylabel("Average Temperature (°C)")
    ax3.set_title("Seasonal Temperature Trend in Delhi")
    st.pyplot(fig3)

else:
    st.info("Please upload the DailyDelhiClimateTrain.csv file to visualize data.")
