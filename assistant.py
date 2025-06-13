from openai import OpenAI
import streamlit as st
import pandas as pd

# ✅ Uses API key from Streamlit secrets
client = OpenAI(api_key=st.secrets["openai"]["api_key"])

SYSTEM_PROMPT = (
    "You are a helpful financial coach. "
    "You receive a user's transaction dataframe in CSV format and the user's question. "
    "Give concise, actionable answers with numeric references when helpful."
)

def df_to_csv_text(df: pd.DataFrame) -> str:
    """Convert DataFrame to text, limiting to first 200 rows if large."""
    if len(df) > 200:
        df_small = df.head(200)
        note = f"(showing first 200 of {len(df)} rows to save tokens)\n"
        return note + df_small.to_csv(index=False)
    return df.to_csv(index=False)

def show_ai_assistant(df):
    st.header("💬 Ask FinSight AI")
    st.write("I know your uploaded data — ask anything like:")
    st.markdown("""
    - "What was my highest spending category last month?"
    - "Do I spend more on food or transport?"
    - "Summarize my expenses"
    """)

    q = st.text_area("📝 Your question", height=120)

    if st.button("Ask") and q.strip():
        with st.spinner("Thinking…"):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "assistant", "content": df_to_csv_text(df)},
                        {"role": "user", "content": q},
                    ],
                    temperature=0.7,
                )
                st.success("🧠 Answer")
                st.write(response.choices[0].message.content)
            except Exception as e:
                st.error(f"❌ Error: {e}")
