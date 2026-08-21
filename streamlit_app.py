import os
import streamlit as st

# Set page layout
st.set_page_config(page_title="Cascade Bank RAG Assistant", page_icon="🤖")
st.title("🤖 Cascade Bank AI Assistant")

# Retrieve API key securely from Streamlit Secrets
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")
if api_key:
    os.environ["OPENROUTER_API_KEY"] = api_key

# Import project's answer synthesis module
try:
    from src.generate.answer_synthesis import generate_answer
except ImportError as e:
    generate_answer = None
    st.error(f"Error loading RAG modules: {e}")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Input
if prompt := st.chat_input("Ask a question about Cascade Bank policies..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not api_key:
            response = "⚠️ **OPENROUTER_API_KEY** is missing in Streamlit Secrets."
        elif generate_answer is None:
            response = "⚠️ Could not load `src.generate.answer_synthesis`. Ensure all repository files are uploaded."
        else:
            with st.spinner("Searching Cascade Bank documents..."):
                try:
                    # Executes full pipeline: Search -> Rerank -> OpenRouter Generation
                    response = generate_answer(prompt)
                except Exception as e:
                    response = f"⚠️ Error searching documents: {e}"

        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})
