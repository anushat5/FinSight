import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, categorize_expenses

def show_dashboard():
    uploaded_file = st.file_uploader("Upload CSV", type="csv")
    if uploaded_file:
        df = load_data(uploaded_file)
        df = categorize_expenses(df)

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
        fig = px.pie(chart_data, values='Amount', names='Category')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Please upload your transaction CSV.")
