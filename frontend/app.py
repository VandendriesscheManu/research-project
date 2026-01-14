import os
import uuid
import requests
import streamlit as st
from pathlib import Path

# Try to read the dynamically generated URL from the shared env file
def get_api_base_url():
    """
    Read PUBLIC_API_BASE_URL from shared/.env.public if it exists,
    otherwise fall back to environment variable or default.
    Appends /docs to the URL.
    """
    shared_env_file = Path(__file__).parent.parent / "shared" / ".env.public"
    
    base_url = None
    
    if shared_env_file.exists():
        try:
            with open(shared_env_file, 'r') as f:
                for line in f:
                    if line.startswith('PUBLIC_API_BASE_URL='):
                        base_url = line.split('=', 1)[1].strip()
                        break
        except Exception as e:
            st.sidebar.warning(f"⚠️ Could not read shared env file: {e}")
    
    # Ensure we don't double-add /docs
    if not base_url.endswith('/docs'):
        base_url = base_url.rstrip('/') + '/docs'
    
    return base_url

API_BASE_URL = get_api_base_url()

# Lees API key uit env (Streamlit Cloud Secrets)
API_KEY = os.getenv("API_KEY", "")

st.set_page_config(page_title="Marketing Plan Generator", page_icon="📊")

st.title("📊 Marketing Plan Generator")
st.caption("AI-powered marketing plan creation: Streamlit → FastAPI → MCP → Ollama → Postgres")

if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("Settings")
    st.write("API:", API_BASE_URL)
    st.write("Session:", st.session_state.session_id)

    # Toon niet de volledige key in UI
    st.write("API key:", "✅ configured" if API_KEY else "⚠️ not configured")

    if st.button("New Marketing Plan"):
        st.session_state.session_id = str(uuid.uuid4())
        st.session_state.messages = []
        st.rerun()
    
    st.divider()
    st.subheader("💡 Tips")
    st.markdown("""
    **Provide details about:**
    - Product name & description
    - Target market & customers
    - Budget range
    - Business goals
    - Timeline for launch
    - Unique features
    """)

# Toon berichten
for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        st.markdown(m["content"])

prompt = st.chat_input("Describe your product and marketing needs...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    try:
        headers = {}
        if API_KEY:
            headers["X-API-KEY"] = API_KEY

        r = requests.post(
            f"{API_BASE_URL}/chat",
            json={"session_id": st.session_state.session_id, "user_message": prompt},
            headers=headers,
            timeout=60,
        )

        # Specifieke error handling voor auth
        if r.status_code == 401:
            raise Exception("Unauthorized (401) — check API_KEY in Streamlit Secrets and in your .env on the server.")

        r.raise_for_status()
        assistant = r.json().get("assistant_message", "")

        if not assistant:
            assistant = "I received an empty response from the API."

    except Exception as e:
        assistant = f"Something went wrong with the API: {e}"

    st.session_state.messages.append({"role": "assistant", "content": assistant})
    with st.chat_message("assistant"):
        st.markdown(assistant)
