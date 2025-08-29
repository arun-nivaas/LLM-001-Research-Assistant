import streamlit as st

# ---------Page Setup---------

about_page = st.Page(
    page = "pages/about.py",
    title="About",
    icon="📘",
    default=True,
)

api_key_page = st.Page(
    page = "pages/api_key.py",
    title="API Key",
    icon="🔑",
    default=False,
)
research_page = st.Page(
    page = "pages/research_assistant.py",
    title="Research Assistant",
    icon="📊",
    default=False,
)
chat_bot_page = st.Page(
    page = "pages/chat_bot.py",
    title="Chat Bot",
    icon="💬",
    default=False,
)

page = st.navigation(
    {
        "Info":[about_page, api_key_page],
        "Research":[research_page, chat_bot_page]
    }
)

st.sidebar.badge("Version : 1.0.0")


page.run()

