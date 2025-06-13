import streamlit as st
import pandas as pd
import plotly.express as px
from utils import load_data, categorize_expenses

def show_dashboard():
    st.title("📊 Personal Finance Dashboard")

    uploaded_file = st.file_uploader("📁 Upload your transaction CSV", type="csv")

    if uploaded_file:
        df = load_data(uploaded_file)
        df = categorize_expenses(df)

        # --- Summary Metrics --- #
        st.subheader("🔎 Financial Summary")
        income = df[df['Category'] == 'Income']['Amount'].sum()
        expenses = df[df['Category'] != 'Income']['Amount'].sum()
        savings = income - expenses

        col1, col2, col3 = st.columns(3)
        col1.metric("Total Income", f"₹{income:,.0f}")
        col2.metric("Total Expenses", f"₹{abs(expenses):,.0f}")
        col3.metric("Net Savings", f"₹{savings:,.0f}", delta_color="normal" if savings >= 0 else "inverse")

        # --- Spend by Category --- #
        st.subheader("🧾 Spend by Category")

        expense_df = df[df['Category'] != 'Income']
        category_data = (
            expense_df.groupby("Category")["Amount"]
            .sum()
            .abs()
            .reset_index()
            .sort_values(by="Amount", ascending=False)
        )

        chart_type = st.radio("📊 View as:", ["Pie Chart", "Bar Chart"], horizontal=True)

        if not category_data.empty:
            if chart_type == "Pie Chart":
                fig = px.pie(category_data, names='Category', values='Amount', hole=0.4,
                             title="Expense Distribution")
            else:
                fig = px.bar(category_data, x='Category', y='Amount', text='Amount',
                             title="Expense by Category", color='Category')

            st.plotly_chart(fig, use_container_width=True)

            # --- Optional table view --- #
            st.subheader("📋 Top Spending Categories")
            st.dataframe(category_data.reset_index(drop=True))
        else:
            st.info("No expenses found to categorize.")

        # --- Optional: Filtered view by category --- #
        st.subheader("🔍 View Transactions by Category")
        categories = df['Category'].unique().tolist()
        selected_category = st.selectbox("Choose a category to explore", categories)

        filtered = df[df['Category'] == selected_category]
        st.write(f"Showing {len(filtered)} transactions in **{selected_category}**")
        st.dataframe(filtered)

    else:
        st.info("Please upload your `.csv` file to begin.")

       

       
