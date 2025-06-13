from openai import OpenAI
import streamlit as st

# Initialize the OpenAI client
client = OpenAI()

def show_ai_assistant():
    st.title("💬 AI Financial Assistant")
    st.write("Ask me anything about your personal finances!")

    user_input = st.text_area("💡 Ask a question (e.g., 'How can I save more each month?')")

    if st.button("Ask") and user_input.strip():
        with st.spinner("Thinking..."):
            try:
                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are a helpful financial assistant."},
                        {"role": "user", "content": user_input}
                    ]
                )
                reply = response.choices[0].message.content
                st.success("🧠 Response:")
                st.write(reply)

            except Exception as e:
                st.error(f"❌ Error: {e}")
