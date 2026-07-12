import time
import requests
import streamlit as st

# -------------------------------
# Page Config
# -------------------------------

st.set_page_config(
    page_title="Customer Support AI",
    page_icon="🤖",
    layout="wide",
)

# -------------------------------
# Load CSS
# -------------------------------



from pathlib import Path

css_path = Path(__file__).parent / "style.css"

with open(css_path, encoding="utf-8") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)



# -------------------------------
# Backend URL
# -------------------------------

## API_URL = "http://127.0.0.1:8000/chat"

API_URL = "https://customer-support-ai-xxxx.onrender.com/chat"


# -------------------------------
# Sidebar
# -------------------------------

with st.sidebar:

    ## st.image("assets/hr_logo.png", width=130)

    st.title("AI Assistant")

    st.markdown("---")

    st.write("### Features")

    st.write("✅ AI Chat")

    st.write("✅ Fast Responses")

    st.write("✅ Chat History")

    st.write("✅ Hugging Face Model")

    st.write("✅ FastAPI Backend")

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

# -------------------------------
# Session State
# -------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------------
# Title
# -------------------------------

st.title("🤖 Customer Support AI")

st.caption("Ask your questions below.")

# -------------------------------
# Display Chat History
# -------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# Chat Input
# -------------------------------

prompt = st.chat_input("Type your question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            try:

                response = requests.post(
                    API_URL,
                    json={
                        "question": prompt,
                    },
                    timeout=180,
                )

                response.raise_for_status()

                answer = response.json()["answer"]

            except Exception as e:

                answer = f"⚠️ Unable to connect to backend.\n\n{e}"

        placeholder = st.empty()

        text = ""

        for word in answer.split():

            text += word + " "

            placeholder.markdown(text)

            time.sleep(0.02)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer,
        }
    )