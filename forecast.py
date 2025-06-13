import streamlit as st
import pandas as pd
from prophet import Prophet
from utils import load_data, categorize_expenses
import plotly.graph_objs as go

def show_forecast():
    st.subheader("📈 Spending Forecast")

    uploaded_file = st.file_uploader("Upload transaction data", type="csv", key="forecast_upload")
    if uploaded_file:
        df = load_data(uploaded_file)
        df = categorize_expenses(df)
        df = df[df['Category'] != 'Income']
        df['Date'] = pd.to_datetime(df['Date'])

        # Group by date
        df_grouped = df.groupby('Date')['Amount'].sum().reset_index()
        df_grouped.columns = ['ds', 'y']
        df_grouped['y'] = -df_grouped['y']  # Prophet expects positive numbers

        try:
            m = Prophet()
            m.fit(df_grouped)
            future = m.make_future_dataframe(periods=30)
            forecast = m.predict(future)

            # Plot forecast with Plotly
            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_grouped['ds'], y=df_grouped['y'], name='Actual Spend'))
            fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], name='Forecast Spend'))
            st.plotly_chart(fig, use_container_width=True)
        except Exception as e:
            st.error(f"Error in forecasting: {e}")
    else:
        st.info("Upload your data to forecast future spending.")

        
