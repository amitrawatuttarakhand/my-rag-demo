import streamlit as st
import os

st.set_page_config(page_title="Local RAG Chatbot", layout="wide")
st.title("🤖 Local RAG AI Assistant")

# Sidebar for API Key input
with st.sidebar:
    api_key = st.text_input("OpenRouter API Key", type="password", value=os.getenv("OPENROUTER_API_KEY", ""))
    if api_key:
        os.environ["OPENROUTER_API_KEY"] = api_key

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Question
if prompt := st.chat_input("Ask a question about your documents..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        st.markdown("This is a place holder response. Connect your search & LLM generation function here.")
        st.session_state.messages.append({"role": "assistant", "content": "Response generated."})
