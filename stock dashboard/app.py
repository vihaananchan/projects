import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import yfinance as yf

st.title("Market Dashboard")

ticker = st.sidebar.text_input("Stock Ticker", value="AAPL").upper()
start_date = st.sidebar.date_input("Start Date", value=pd.to_datetime("2023-01-01"))
end_date = st.sidebar.date_input("End Date", value=pd.to_datetime("today"))

data = yf.download(ticker, start=start_date, end=end_date)

if data.empty:
    st.error("No data found. Check the ticker symbol.")
else:
    data = data[["Close"]].copy()
    data.columns = ["Close"]
    data.index = pd.to_datetime(data.index)

    data["Daily Return"] = data["Close"].pct_change()
    data["Cumulative Return"] = (1 + data["Daily Return"]).cumprod() - 1
    data["Volatility"] = data["Daily Return"].rolling(window=21).std() * (252 ** 0.5)
    data["Peak"] = data["Close"].cummax()
    data["Drawdown"] = (data["Close"] - data["Peak"]) / data["Peak"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Return", f"{data['Cumulative Return'].iloc[-1]*100:.2f}%")
    col2.metric("Max Drawdown", f"{data['Drawdown'].min()*100:.2f}%")
    col3.metric("Current Volatility", f"{data['Volatility'].iloc[-1]*100:.2f}%")

    st.subheader(f"{ticker} Price")
    fig1 = px.line(data, x=data.index, y="Close")
    st.plotly_chart(fig1)

    st.subheader("Cumulative Return")
    fig2 = px.line(data, x=data.index, y="Cumulative Return")
    st.plotly_chart(fig2)

    st.subheader("Rolling Volatility (Annualised)")
    fig3 = px.line(data, x=data.index, y="Volatility")
    st.plotly_chart(fig3)

    st.subheader("Drawdown")
    fig4 = px.area(data, x=data.index, y="Drawdown")
    st.plotly_chart(fig4)

    st.subheader("Raw Data")
    st.dataframe(data)