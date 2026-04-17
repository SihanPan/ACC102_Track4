import streamlit as st
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# 页面设置
st.set_page_config(page_title="Stock Analysis Tool", layout="wide")
st.title("ACC102 Track4: Interactive Stock Analysis Tool")
st.subheader("Student: [Your Name] | ID: [Your ID]")

# 用户输入
ticker = st.text_input("Input Stock Ticker (e.g., AAPL, MSFT)", "AAPL")
start = st.date_input("Start Date", pd.to_datetime("2023-01-01"))
end = st.date_input("End Date", pd.to_datetime("2026-01-01"))

# 下载数据
data = yf.download(ticker, start=start, end=end)

if not data.empty:
    st.success("Data loaded successfully!")

    # 数据清洗
    data = data.dropna()
    data["Daily Return"] = data["Close"].pct_change()

    # 展示数据
    st.subheader("Data Preview")
    st.dataframe(data.tail(10))

    # 描述统计
    st.subheader("Descriptive Statistics")
    st.write(data[["Close", "Volume", "Daily Return"]].describe())

    # 画图1：股价走势
    st.subheader("Close Price Trend")
    fig1, ax1 = plt.subplots(figsize=(12, 4))
    ax1.plot(data.index, data["Close"], label="Close Price")
    ax1.set_title(f"{ticker} Price Trend")
    ax1.legend()
    st.pyplot(fig1)

    # 画图2：收益率分布
    st.subheader("Daily Return Distribution")
    fig2, ax2 = plt.subplots(figsize=(10, 3))
    ax2.hist(data["Daily Return"].dropna(), bins=50)
    ax2.set_title("Daily Return")
    st.pyplot(fig2)

    # 结论
    st.subheader("Key Insights")
    st.write(f"Latest Close Price: ${data['Close'].iloc[-1]:.2f}")
    st.write(f"Average Daily Return: {data['Daily Return'].mean():.4f}")
    st.write(f"Volatility (Std): {data['Daily Return'].std():.4f}")

else:
    st.warning("No data, please check ticker or date.")