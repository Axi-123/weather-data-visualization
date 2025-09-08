import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

st.title("Weather Data Visualization")

# Sample data
dates = pd.date_range(start='2021-01-01', end='2021-12-31')
temperature = np.random.randint(20,35,len(dates))
df = pd.DataFrame({"Date": dates, "Temperature": temperature})

# Plot
st.subheader("Temperature Trend")
st.line_chart(df.set_index('Date'))
