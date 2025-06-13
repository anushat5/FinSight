import streamlit as st
from dashboard import show_dashboard
from forecast import show_forecast
from assistant import show_ai_assistant

st.set_page_config(page_title="FinSight Pro 💰", layout="wide")

st.sidebar.title("📂 Navigation")
page = st.sidebar.radio("Go to", ["Dashboard", "Forecasting", "AI Assistant"])

st.title("💰 FinSight Pro")
st.write("Advanced AI-Powered Financial Analysis & Forecasting Dashboard")

if page == "Dashboard":
    show_dashboard()
elif page == "Forecasting":
    show_forecast()
elif page == "AI Assistant":
    show_ai_assistant()
