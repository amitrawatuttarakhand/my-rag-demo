import os
import streamlit as st

st.set_page_config(page_title="Local RAG Chatbot", layout="wide")
st.title("🤖 Local RAG AI Assistant")

# Retrieve key securely from environment or Streamlit secrets (hidden from UI)
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Question Input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response = "⚠️ API Key is missing. Please configure OPENROUTER_API_KEY in Streamlit secrets."
        else:
            # Connect your retrieval & generation functions here
            response = "Response generated securely."

        st.markdown(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
