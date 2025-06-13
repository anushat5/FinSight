import streamlit as st
from dashboard import show_dashboard
from forecast import show_forecast
from assistant import show_ai_assistant
from utils import load_data, categorize_expenses

st.set_page_config(page_title="FinSight - Personal Finance AI", layout="wide")
st.title("💰 FinSight – AI Financial Analysis")

# CSV Upload only once
uploaded_file = st.sidebar.file_uploader("📁 Upload your transaction CSV", type="csv")

# Store in session state to persist across tabs
if uploaded_file and "data" not in st.session_state:
    df = load_data(uploaded_file)
    df = categorize_expenses(df)
    st.session_state["data"] = df

# Check if data exists
if "data" in st.session_state:
    df = st.session_state["data"]

    tab = st.sidebar.radio("📊 Select View", ["Dashboard", "Forecast", "AI Assistant"])

    if tab == "Dashboard":
        show_dashboard(df)
    elif tab == "Forecast":
        show_forecast(df)
    elif tab == "AI Assistant":
        show_ai_assistant(df)
else:
    st.warning("⚠️ Please upload a CSV file to get started.")
