import streamlit as st
from const import Constants
from cache_setup import init_cache


# Initialize persistent cache

db_path = init_cache()                   # Creates cache/langchain_cache.sqlite if it doesn’t exist

# ---------Page Setup---------

about_page = st.Page(
    page = "pages/about.py",
    title= Constants.TITLE_ABOUT,
    icon="📘",
    default=True,
)

api_key_page = st.Page(
    page = "pages/api_key.py",
    title= Constants.TITLE_API_KEY,
    icon="🔑",
    default=False,
)
research_page = st.Page(
    page = "pages/research_assistant.py",
    title= Constants.TITLE_RESEARCH,
    icon="📊",
    default=False,
)
chat_bot_page = st.Page(
    page = "pages/chat_bot.py",
    title= Constants.TITLE_CHAT_BOT,
    icon="💬",
    default=False,
)

page = st.navigation(
    {
        "Info":[about_page, api_key_page],
        "Research":[research_page, chat_bot_page]
    }
)

st.sidebar.badge(f"Version : {Constants.VERSION}")


page.run()

