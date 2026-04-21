import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

import sys
sys.modules['distutils.version'] = __import__('packaging.version')

import pandas_datareader as pdr

st.title("AAPL Stock Analysis Tool")
st.subheader("Data Source: Stooq (Real US Stock Data)")

ticker = "AAPL"
start_date = "2024-01-01"
end_date = "2025-01-01"

try:
    data = pdr.get_data_stooq(ticker, start=start_date, end=end_date)
    data = data.sort_index()
    st.success("✅ Real data loaded successfully")
except:
    dates = pd.date_range(start="2024-01-01", periods=100, freq="D")
    data = pd.DataFrame({
        "Close": [150 + i*0.5 for i in range(100)],
        "Volume": [1000000]*100
    }, index=dates)
    st.info("ℹ️ Using demo data")

data = data.dropna()
data["Daily Return"] = data["Close"].pct_change().fillna(0)

st.subheader("Latest Data")
st.dataframe(data.tail(10))

st.subheader("Descriptive Statistics")
st.write(data[["Close", "Volume", "Daily Return"]].describe())

st.subheader("Close Price Trend")
fig1, ax1 = plt.subplots(figsize=(10, 3))
ax1.plot(data.index, data["Close"], label="Close Price")
ax1.set_title(f"{ticker} Close Price")
ax1.legend()
ax1.grid(alpha=0.3)
st.pyplot(fig1)

st.subheader("Daily Return Distribution")
fig2, ax2 = plt.subplots(figsize=(10, 3))
ax2.hist(data["Daily Return"], bins=50, alpha=0.7)
ax2.set_title("Daily Return")
ax2.grid(alpha=0.3)
st.pyplot(fig2)

st.subheader("Key Metrics")
st.write(f"Latest Close Price: ${data['Close'].iloc[-1]:.2f}")
st.write(f"Average Daily Return: {data['Daily Return'].mean():.4f}")
st.write(f"Volatility: {data['Daily Return'].std():.4f}")
