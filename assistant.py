import streamlit as st
import openai
import os

def show_ai_assistant():
    st.subheader("💡 AI Financial Coach")

    openai.api_key = os.getenv("OPENAI_API_KEY")
    query = st.text_area("Ask anything about your finances:", height=150)

    if st.button("Get Advice") and query:
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": query}]
            )
            st.success(response['choices'][0]['message']['content'])
        except Exception as e:
            st.error(f"Error: {e}")
