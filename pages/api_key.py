import streamlit as st
from const import Constants
import markdown

st.header(Constants.HEADER_TITLE_API_KEY)
st.markdown("---")
st.write(markdown.api_key_info)

api_key = st.text_input("Enter API Key", type= Constants.PASSWORD, placeholder="Paste your key here...")

if st.button("Submit Key"):

    if not api_key:
        st.error("❌ Please enter your API key.")

    elif api_key and api_key.startswith("AIza"):
        st.session_state.api_key = api_key
        st.session_state.agent_executor = None # Reset agent executor when API key changes
        st.success("✅ API Key Saved Successfully!")
        
    else:
        st.error("❌ Please enter a valid API key.")

st.info("⚠️ Tip: Never share your API key with others. Keys are unique and tied to your account.")
