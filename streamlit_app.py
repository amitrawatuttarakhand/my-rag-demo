import os
import streamlit as st
import openrouter

st.set_page_config(page_title="Local RAG Chatbot", layout="wide")
st.title("🤖 Local RAG AI Assistant")

# 1. Fetch API Key secretly from Streamlit Secrets or Environment
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# 2. Import project RAG logic safely
try:
    from src.generate.answer_synthesis import generate_answer
except ImportError:
    generate_answer = None

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Handle User Input
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response = "⚠️ OPENROUTER_API_KEY is missing. Please add it to your Streamlit secrets."
        elif generate_answer:
            # Calls your actual RAG pipeline search & OpenRouter generation
            with st.spinner("Searching documents & generating answer..."):
                response = generate_answer(prompt)
        else:
            response = "Could not load `src.generate.answer_synthesis`. Ensure all files from the repo are uploaded."

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
