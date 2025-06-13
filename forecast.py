import streamlit as st
import pandas as pd
from prophet import Prophet
from utils import load_data, categorize_expenses

def show_forecast():
    st.subheader("📈 Spending Forecast")

    uploaded_file = st.file_uploader("Upload transaction data", type="csv", key="forecast_upload")
    if uploaded_file:
        df = load_data(uploaded_file)
        df = categorize_expenses(df)
        df = df[df['Category'] != 'Income']
        df['Date'] = pd.to_datetime(df['Date'])

        df_grouped = df.groupby('Date')['Amount'].sum().reset_index()
        df_grouped.columns = ['ds', 'y']
        df_grouped['y'] = -df_grouped['y']  # negative because expenses

        m = Prophet()
        m.fit(df_grouped)
        future = m.make_future_dataframe(periods=30)
        forecast = m.predict(future)

        st.line_chart(forecast[['ds', 'yhat']].set_index('ds'))
    else:
        st.info("Upload your data to forecast future spending.")
