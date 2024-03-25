from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

ID = "243f1c6b-dfc5-4d64-ab7f-331e74858393"

wikipedia_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
