import uuid
import requests
import streamlit as st
from constants.constant import Const

BACKEND_URL = Const.BACKEND_URL

CHAT_POLL_ENDPOINT = f"{BACKEND_URL}/api/vanna/v2/chat_poll"

st.set_page_config(page_title="Vanna AI", page_icon="🤖", layout="centered")
st.title("Vanna AI Assistant")
st.write("Ask questions in plain English and get answers from your data.")

# Session state
if "conversation_id" not in st.session_state:
    st.session_state.conversation_id = str(uuid.uuid4())

if "history" not in st.session_state:
    st.session_state.history = []

# Input
message = st.text_input("Ask a question", placeholder="e.g. show top 10 users by orders")
send = st.button("Send")

def call_chat_poll(user_message: str):
    payload = {
        "message": user_message,
        "conversation_id": st.session_state.conversation_id,
        "request_id": str(uuid.uuid4()),
        "request_context": {
            "cookies": {
                # Optional: this matches your SimpleUserResolver cookie key
                # "vanna_email": "admin@example.com",
            },
            "headers": {},
            "remote_addr": "127.0.0.1",
            "query_params": {},
            "metadata": {}
        },
        "metadata": {}
    }

    r = requests.post(CHAT_POLL_ENDPOINT, json=payload, timeout=120)
    r.raise_for_status()
    return r.json()

if send and message.strip():
    with st.spinner("Thinking..."):
        try:
            result = call_chat_poll(message.strip())
            st.session_state.history.append({"role": "user", "content": message.strip()})
            st.session_state.history.append({"role": "assistant", "content": result})
        except requests.HTTPError as e:
            st.error(f"Backend error: {e.response.status_code} - {e.response.text}")
        except Exception as e:
            st.error(f"Request failed: {e}")

# Render history (latest at bottom)
for item in st.session_state.history:
    if item["role"] == "user":
        st.markdown("### You")
        st.write(item["content"])
    else:
        st.markdown("### Assistant")

        resp = item["content"]

        # The poll response returns "chunks". We’ll try to display the most useful bits.
        chunks = resp.get("chunks", [])
        if not chunks:
            st.write(resp)
            st.divider()
            continue

        # Show all chunk content nicely
        for i, ch in enumerate(chunks, start=1):
            simple = ch.get("simple", {}) or {}
            rich = ch.get("rich", {}) or {}

            # Most common: the assistant text is usually in simple
            if simple:
                st.write(simple)

            # If rich contains SQL/data/viz instructions, show it too
            if rich:
                with st.expander(f"Chunk {i} (rich payload)"):
                    st.json(rich)

        st.divider()

# Controls
col1, col2 = st.columns(2)
with col1:
    if st.button("New conversation"):
        st.session_state.conversation_id = str(uuid.uuid4())
        st.session_state.history = []
        st.rerun()

with col2:
    st.caption(f"conversation_id: {st.session_state.conversation_id}")
