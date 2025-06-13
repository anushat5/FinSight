import streamlit as st
from dashboard import show_dashboard
from forecast import show_forecast
from utils import load_data, categorize_expenses

st.set_page_config(page_title="FinSight - Personal Finance App", layout="wide")
st.title("💰 FinSight – Personal Finance Tracker")

uploaded_file = st.sidebar.file_uploader("📁 Upload your transaction CSV", type="csv")

if uploaded_file and "data" not in st.session_state:
    df = load_data(uploaded_file)
    df = categorize_expenses(df)
    st.session_state["data"] = df

if "data" in st.session_state:
    df = st.session_state["data"]

    tab = st.sidebar.radio("📊 Select View", ["Dashboard", "Forecast"])

    if tab == "Dashboard":
        show_dashboard(df)
    elif tab == "Forecast":
        show_forecast(df)
else:
    st.warning("⚠️ Please upload a CSV file to get started.")
