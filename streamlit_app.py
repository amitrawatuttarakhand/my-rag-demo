import sys
from pathlib import Path

# Fix module import paths so Streamlit Cloud finds 'src'
root_path = Path(__file__).resolve().parent
if str(root_path) not in sys.path:
    sys.path.append(str(root_path))

import os
import streamlit as st

# Configure page layout
st.set_page_config(page_title="Cascade Bank RAG Assistant", page_icon="🤖")
st.title("🤖 Cascade Bank AI Assistant")

# Retrieve API key securely from Streamlit Secrets or Environment
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get(
    "OPENROUTER_API_KEY", ""
)
if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key

# Import project's RAG module safely
try:
    from src.generate.answer_synthesis import generate_answer
except Exception as e:
    generate_answer = None
    st.error(f"Error loading RAG modules: {e}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render past chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Process User Input
if prompt := st.chat_input("Ask a question about Cascade Bank policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response = "⚠️ **OPENROUTER_API_KEY** is missing in Streamlit Secrets. Please add it to your app settings."
        elif generate_answer is None:
            response = "⚠️ Could not load `src.generate.answer_synthesis`. Ensure the `src/` directory is present in your GitHub repository."
        else:
            with st.spinner("Searching Cascade Bank documents..."):
                try:
                    response = generate_answer(prompt)
                except Exception as e:
                    response = f"⚠️ Error generating answer: {e}"

        st.markdown(response)
        st.session_state.messages.append(
            {"role": "assistant", "content": response}
        )
