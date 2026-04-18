import pandas as pd
import plotly.express as px
import streamlit as st


df = pd.read_csv("transactions.csv")
df["Date"] = pd.to_datetime(df["Date"])
df = df.sort_values("Date")


st.title("Personal Spending Tracker")


categories = ["All"] + list(df["Category"].unique())
selected_cat = st.sidebar.selectbox("Filter by Category", categories)
date_range = st.sidebar.date_input("Date Range", [df["Date"].min(), df["Date"].max()])

filtered = df.copy()
if selected_cat != "All":
    filtered = filtered[filtered["Category"] == selected_cat]
filtered = filtered[
    (filtered["Date"] >= pd.to_datetime(date_range[0])) &
    (filtered["Date"] <= pd.to_datetime(date_range[1]))
]

col1, col2, col3 = st.columns(3)
col1.metric("Total Spent", f"${filtered['Amount'].sum():,.2f}")
col2.metric("Transactions", len(filtered))
col3.metric("Avg per Transaction", f"${filtered['Amount'].mean():,.2f}")

st.subheader("Spending by Category")
fig1 = px.bar(filtered.groupby("Category")["Amount"].sum().reset_index(),
              x="Category", y="Amount", color="Category")
st.plotly_chart(fig1)

st.subheader("Spending Over Time")
fig2 = px.line(filtered.groupby("Date")["Amount"].sum().reset_index(),
               x="Date", y="Amount")
st.plotly_chart(fig2)

st.subheader("Category Breakdown")
fig3 = px.pie(filtered, values="Amount", names="Category")
st.plotly_chart(fig3)

st.subheader("All Transactions")
st.dataframe(filtered)