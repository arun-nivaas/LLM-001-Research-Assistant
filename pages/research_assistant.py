import streamlit as st
import llm_client
from const import Constants

st.set_page_config(layout = Constants.WIDE)

if "api_key" not in st.session_state:
    st.session_state.api_key = ""

if "agent_executor" not in st.session_state:
    st.session_state.agent_executor = None

st.header(Constants.HEADER_TITLE_RESEARCH)
st.markdown("---")
st.markdown(
            "Easily explore any research topic with instant summaries, videos, and papers. "
            "Turn your ideas into a comprehensive research brief within minutes 🚀"
        )

user_input = st.text_area("Enter your research topic here:", height=50, placeholder="e.g., Quantum Computing Applications in Healthcare")
        
# Submit Button for Topic

if st.button("🔍 Start Research"):
    if not user_input:
        st.warning("⚠️ Please enter a topic first.")
    elif not st.session_state.api_key:
        st.error("⚠️ Please enter your API key in the API key tab and submit.")
    elif len(user_input) < 15:
        st.warning("⚠️ Please provide a more detailed topic (at least 15 characters).")
    else:
        with st.spinner("⏳ Generating research insights..."):
            try:
                if st.session_state.agent_executor is None:
                    st.session_state.agent_executor = llm_client.llm_and_agent(st.session_state.api_key)

                agent_executor = st.session_state.agent_executor

                # result = asyncio.run(agent_executor.ainvoke({"input": user_input}))
                result = agent_executor.invoke({"input": user_input})
                output_text = result.get("output") if isinstance(result, dict) else result

                st.subheader("Answer:")
                st.markdown(output_text,width = "stretch")

            except Exception as e:
                st.error(f"Error: {str(e)}")

        