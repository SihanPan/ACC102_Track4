import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sys
try:
    from distutils.version import LooseVersion
except ImportError:
    from packaging.version import Version as LooseVersion
    sys.modules['distutils.version'] = sys.modules['packaging.version']
    setattr(sys.modules['distutils.version'], 'LooseVersion', LooseVersion)

import pandas_datareader as pdr

st.set_page_config(page_title="Stock Analysis Tool", layout="wide")
st.title("ACC102 Track4: Interactive Stock Analysis Tool")
st.subheader("Student: Sihan Pan | ID: 2471700")

ticker = st.text_input("Input Stock Ticker (e.g., AAPL, MSFT)", "AAPL")
start = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end = st.date_input("End Date", pd.to_datetime("2026-01-01"))

data = pdr.get_data_stooq(ticker, start=start, end=end)
data = data.sort_index()
st.success("Real US stock data loaded successfully (Stooq)")

data = data.dropna()
data["Daily Return"] = data["Close"].pct_change().fillna(0)

st.subheader("Data Preview")
st.dataframe(data.tail(10))

st.subheader("Descriptive Statistics")
st.write(data[["Close", "Volume", "Daily Return"]].describe())

st.subheader("Close Price Trend")
fig1, ax1 = plt.subplots(figsize=(12, 4))
ax1.plot(data.index, data["Close"], label="Close Price")
ax1.set_title(f"{ticker} Price Trend")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

st.subheader("Daily Return Distribution")
fig2, ax2 = plt.subplots(figsize=(10, 3))
ax2.hist(data["Daily Return"].dropna(), bins=50, alpha=0.7)
ax2.set_title("Daily Return Distribution")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

st.subheader("Key Insights")
st.write(f"Latest Close Price: ${data['Close'].iloc[-1]:.2f}")
st.write(f"Average Daily Return: {data['Daily Return'].mean():.4f}")
st.write(f"Volatility (Std): {data['Daily Return'].std():.4f}")
