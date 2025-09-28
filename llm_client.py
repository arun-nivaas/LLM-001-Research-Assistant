from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.agents import AgentExecutor, create_tool_calling_agent
import agents
import prompts



def llm_and_agent(api_key: str):
    llm = ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        google_api_key = api_key,
        safety_settings = {
    0: 2,  # DANGEROUS_CONTENT → medium block
    1: 2,  # HARASSMENT → medium block
    2: 2,  # HATE_SPEECH → medium block
    3: 2   # SEXUALLY_EXPLICIT → medium block
},
    temperature = 0.5)

    tools = [agents.wikipedia_tool, agents.youtube_tool, agents.semantic_scholar_tool]
    prompt = prompts.final_prompt
    
    calling_agent = create_tool_calling_agent(llm=llm, tools=tools,prompt=prompt)
    agent_executor = AgentExecutor.from_agent_and_tools(agent=calling_agent, tools=tools, verbose=True)

    return agent_executor

