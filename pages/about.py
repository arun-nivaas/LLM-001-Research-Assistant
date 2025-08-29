import streamlit as st
from const import Constants

st.header("ℹ️ ABOUT THE APPLICATION",divider="gray")

st.set_page_config(layout= Constants.WIDE)

assistant_info = st.container()
with assistant_info:
    st.markdown(
    """
    <div style="background-color:#f0f6ff; padding:20px; border-radius:12px; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
        <h2 style="color:#1f77b4; text-align:center;">🧠 AI Research Assistant</h2>
        <p style="font-size:16px; text-align:center; color:#444;">
            Your personal guide to <b>research smarter, not harder</b>.  
            Explore topics, find trusted resources, and get answers — all in one place.
        </p>
        <ul style="font-size:15px; line-height:1.8; color:#333;">
            <li>📌 <b>Subtopic Suggestions</b> → Break down broad topics into clear, focused research angles.</li>
            <li>🎥 <b>YouTube Learning</b> → Discover top educational videos explained in simple terms.</li>
            <li>📑 <b>Research Papers</b> → Access credible papers from Semantic Scholar with quick summaries.</li>
            <li>🌐 <b>Wikipedia Insights</b> → Get crisp background knowledge in just a few lines.</li>
            <li>📝 <b>Structured Reports</b> → Receive organized summaries with actionable next steps.</li>
            <li>✅ <b>Who is it for?</b> → Students, researchers, and professionals who want to save time and gain deeper insights.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("---")

chat_bot_info = st.container()
with chat_bot_info:
    st.markdown(
    """
    <div style="background-color:#fff8e6; padding:20px; border-radius:12px; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
        <h2 style="color:#e67e22; text-align:center;">🤖 Research QA Chatbot</h2>
        <p style="font-size:16px; text-align:center; color:#444;">
            Upload any <b>research paper</b> and instantly <b>chat with it</b>.  
            Get clear answers, explore related resources, and save hours of searching.
        </p>
        <ul style="font-size:15px; line-height:1.8; color:#333;">
            <li>📂 <b>Upload Your Paper</b> → Simply drop a PDF to start the conversation.</li>
            <li>💬 <b>Ask Anything</b> → Get precise answers directly from the paper’s content.</li>
            <li>🎥 <b>YouTube Learning</b> → Receive top 3 videos that simplify tough concepts.</li>
            <li>📑 <b>Semantic Scholar</b> → Find related papers with titles, abstracts, and author info.</li>
            <li>🌐 <b>Wikipedia Summaries</b> → Quick, easy-to-digest background explanations.</li>
            <li>⚡ <b>Why it’s awesome?</b> → Turns static PDFs into an <b>interactive learning companion</b>.</li>
        </ul>
    </div>
    """,
    unsafe_allow_html=True
)

quick_tip_info = st.container()
with quick_tip_info:
    st.markdown("---")
    st.markdown(
        """
        <div style="background-color:#f0f9ff; padding:20px; border-radius:12px; box-shadow:0px 2px 8px rgba(0,0,0,0.1);">
            <h3 style="color:#0077b6; text-align:center;">⚡ Quick Tip</h3>
            <ul style="font-size:15px; line-height:1.8; color:#333; list-style-type:none; padding-left:0;">
                <li>💡 <b>Upload your research paper PDF</b> in the <b>QA Chatbot</b> to chat and get instant answers.</li>
                <li>🎥 <b>YouTube Links</b> → Learn complex concepts with top videos.</li>
                <li>📑 <b>Semantic Scholar & Wikipedia</b> → Deeper background + related research.</li>
                <li>🔑 <b>Set your API key</b> before starting to unlock all features.</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True
    )