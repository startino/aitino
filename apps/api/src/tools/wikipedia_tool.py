from typing import Type

from langchain.agents import Tool
from langchain.pydantic_v1 import BaseModel, Field
from langchain.tools import BaseTool
from langchain_community.tools import WikipediaQueryRun
from langchain_community.utilities import WikipediaAPIWrapper

ID = "243f1c6b-dfc5-4d64-ab7f-331e74858393"


class WikipediaToolInput(BaseModel):
    query: str = Field(
        title="Query", description="Search query input to search wikipedia"
    )


class WikipediaTool(Tool, BaseTool):
    args_schema: Type[BaseModel] = WikipediaToolInput

    def __init__(self):
        wiki_tool = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
        super().__init__(
            name="wikipedia",
            func=wiki_tool.run,
            description="""A wrapper around Wikipedia. Useful for when you need to answer general questions
            about people, places, companies, facts, historical events, or other subjects.
            Input should be a search query.scrapes web with serper""",
        )
