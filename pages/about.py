import streamlit as st
from const import Constants
import markdown

st.header(Constants.HEADER_TITLE_ABOUT, divider = "gray")

st.set_page_config(layout= Constants.WIDE)

assistant_info = st.container()
with assistant_info:
    st.markdown(markdown.assistant_info, unsafe_allow_html=True)

st.markdown("---")

chat_bot_info = st.container()
with chat_bot_info:
    st.markdown(markdown.chat_bot_info, unsafe_allow_html=True)

quick_tip_info = st.container()
with quick_tip_info:
    st.markdown("---")
    st.markdown(markdown.quick_tip_info,unsafe_allow_html=True)