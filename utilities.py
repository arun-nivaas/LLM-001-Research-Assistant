from langchain_community.tools import YouTubeSearchTool
from langchain_community.tools.semanticscholar import SemanticScholarQueryRun
from langchain_community.utilities.semanticscholar import SemanticScholarAPIWrapper
from langchain_community.retrievers import WikipediaRetriever


# Function to perform YouTube search
def youtube_search(topic :str):
    youtube_search = YouTubeSearchTool()
    return youtube_search.run(topic, max_results=3)
    
# Function to perform Wikipedia search
def wikipedia_search(topic :str):
    wiki_retriever = WikipediaRetriever()
    return wiki_retriever.invoke(topic)

# Function to perform Semantic Scholar search
def semantic_scholar(topic: str):
    s2_wrapper = SemanticScholarAPIWrapper(doc_content_chars_max=1000, top_k_results=5)
    scholar_tool = SemanticScholarQueryRun(api_wrapper=s2_wrapper)
    return scholar_tool.run(topic)


   