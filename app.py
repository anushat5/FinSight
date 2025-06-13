import streamlit as st
from utils import load_data, categorize_expenses
from dashboard import show_dashboard
from forecast import show_forecast
from assistant import show_ai_assistant

# ------------------------------------------------ #
#  Page config
# ------------------------------------------------ #
st.set_page_config(
    page_title="FinSight Pro",
    page_icon="💰",
    layout="wide",
)

st.title("💰 FinSight Pro – Personal Finance Studio")

# ------------------------------------------------ #
#  1 – File upload (sidebar, single source of truth)
# ------------------------------------------------ #
with st.sidebar:
    st.header("📂 Upload Data")
    uploaded = st.file_uploader("CSV with Date, Description, Amount", type="csv")

    if uploaded:
        df = load_data(uploaded)
        df = categorize_expenses(df)
        st.success(f"Loaded {len(df)} transactions")
        # Persist between tabs
        st.session_state["data"] = df
    elif "data" not in st.session_state:
        st.info("Please upload a CSV to begin")

# ------------------------------------------------ #
#  2 – Main content (tabs)
# ------------------------------------------------ #
if "data" in st.session_state:
    df = st.session_state["data"]

    tab1, tab2, tab3 = st.tabs(["📊 Dashboard", "🔮 Forecast", "💬 AI Assistant"])

    with tab1:                      # Dashboard
        show_dashboard(df)

    with tab2:                      # Forecast
        show_forecast(df)

    with tab3:                      # AI Assistant
        show_ai_assistant(df)
else:
    st.stop()  # nothing to show until a file is uploaded

