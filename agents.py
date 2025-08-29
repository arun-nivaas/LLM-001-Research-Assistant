from langchain.tools import Tool
import utilities

# Create Tool instances for youTube
youtube_tool = Tool(
    name="Youtube_search",
    func=utilities.youtube_search, 
    description="Search top 3 YouTube videos links for reference. "
)


# Create Tool instances for Wikipedia
wikipedia_tool = Tool(
    name="Wikipedia_Search",
    func=utilities.wikipedia_search, 
    description="Search Wikipedia for summaries related to the research topic."
)


# Create Tool instances for Semantic Scholar
semantic_scholar_tool = Tool(
    name="Semantic_Scholar_Search", 
    func=utilities.semantic_scholar, 
    description="Search Semantic Scholar for academic papers related to the research topic.")



