import streamlit as st
import pandas as pd
from prophet import Prophet
from utils import load_data, categorize_expenses, prepare_prophet_data
import plotly.graph_objs as go


def show_forecast():
    st.title("🔮 Expense Forecasting")
    st.markdown(
        "Upload your transaction data to generate a **30-day expense forecast** using AI (Prophet)."
    )

    uploaded_file = st.file_uploader("📁 Upload CSV file", type="csv", key="forecast_file")

    if uploaded_file:
        with st.spinner("Processing your data..."):
            # Step 1: Load & clean
            df = load_data(uploaded_file)
            df = categorize_expenses(df)
            prophet_df = prepare_prophet_data(df)

            # Step 2: Forecast
            try:
                model = Prophet()
                model.fit(prophet_df)
                future = model.make_future_dataframe(periods=30)
                forecast = model.predict(future)

                # Step 3: Plot
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=prophet_df['ds'], y=prophet_df['y'],
                                         mode='lines+markers', name='Actual Spend'))
                fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'],
                                         mode='lines', name='Forecasted Spend'))

                fig.update_layout(title="📊 30-Day Expense Forecast",
                                  xaxis_title="Date", yaxis_title="Spend Amount",
                                  template="plotly_white")

                st.success("Forecast generated!")
                st.plotly_chart(fig, use_container_width=True)

                # Optional: Show forecasted data table
                st.subheader("🔍 Forecast Data (Next 30 Days)")
                forecast_filtered = forecast[['ds', 'yhat']].tail(30)
                forecast_filtered.columns = ['Date', 'Predicted Spend']
                st.dataframe(forecast_filtered)

            except Exception as e:
                st.error(f"❌ Forecasting failed: {e}")
    else:
        st.info("Upload your `.csv` file with transaction history to begin.")

          
