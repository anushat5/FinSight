import streamlit as st
import plotly.express as px
import pandas as pd

def show_dashboard(df):
    st.subheader("🔎 Summary")
    income = df[df['Category'] == 'Income']['Amount'].sum()
    expense = df[df['Category'] != 'Income']['Amount'].sum()
    savings = income - expense

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Income", f"₹{income:,.0f}")
    col2.metric("Total Expenses", f"₹{expense:,.0f}")
    col3.metric("Net Savings", f"₹{savings:,.0f}")

    st.subheader("📊 Expenses by Category")
    chart_data = df[df['Category'] != 'Income'].groupby('Category')['Amount'].sum().reset_index()
    if not chart_data.empty:
        fig = px.pie(chart_data, values='Amount', names='Category', title="Spending Breakdown")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No expenses to show yet.")
