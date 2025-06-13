import streamlit as st
import pandas as pd
import plotly.express as px

def show_forecast(df):
    st.subheader("🔮 Expense Forecast")

    # Ensure Date column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Filter out income for forecasting expenses only
    df = df[df['Category'] != 'Income']

    if df.empty:
        st.info("Not enough expense data to forecast.")
        return

    # Aggregate monthly expenses
    df['Month'] = df['Date'].dt.to_period('M').astype(str)
    monthly_expense = df.groupby('Month')['Amount'].sum().reset_index()
    monthly_expense['Month'] = pd.to_datetime(monthly_expense['Month'])

    # Simple Linear Forecast
    monthly_expense = monthly_expense.sort_values('Month')
    monthly_expense['Forecast'] = monthly_expense['Amount'].rolling(window=3, min_periods=1).mean()

    # Plot
    fig = px.line(monthly_expense, x='Month', y=['Amount', 'Forecast'],
                  labels={'value': '₹', 'variable': 'Type'},
                  title='Monthly Expense & Forecast')
    st.plotly_chart(fig, use_container_width=True)

    st.caption("⚠️ Forecast is based on a rolling average of the past 3 months. For better accuracy, integrate ML models later.")
