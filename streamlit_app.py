import os
import requests
import streamlit as st

# Page Configuration
st.set_page_config(page_title="Local RAG Chatbot", page_icon="🤖", layout="wide")
st.title("🤖 Local RAG AI Assistant")

# Retrieve API key securely from Streamlit Secrets or system environment
api_key = os.getenv("OPENROUTER_API_KEY") or st.secrets.get("OPENROUTER_API_KEY", "")

# Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Render Existing Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User Query Input
if prompt := st.chat_input("Ask a question about your documents..."):
    # Append user question to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Process and Generate AI Response
    with st.chat_message("assistant"):
        if not api_key:
            response = "⚠️ **API Key Missing**: Please set `OPENROUTER_API_KEY` in your Streamlit Cloud Secrets."
            st.warning(response)
        else:
            with st.spinner("Generating response..."):
                try:
                    # Make a direct REST call to OpenRouter API
                    res = requests.post(
                        url="https://openrouter.ai/api/v1/chat/completions",
                        headers={
                            "Authorization": f"Bearer {api_key}",
                            "Content-Type": "application/json",
                        },
                        json={
                            "model": "openai/gpt-4o-mini",
                            "messages": [
                                {
                                    "role": "system",
                                    "content": "You are a helpful AI assistant.",
                                },
                                {"role": "user", "content": prompt},
                            ],
                        },
                        timeout=30,
                    )

                    if res.status_code == 200:
                        data = res.json()
                        response = data["choices"][0]["message"]["content"]
                    else:
                        response = f"⚠️ **API Error ({res.status_code})**: {res.text}"

                except Exception as e:
                    response = f"⚠️ **Error**: Failed to connect to API ({e})"

            st.markdown(response)

        # Append assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": response})
