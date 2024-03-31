import os

from dotenv import load_dotenv
from langchain_community.tools import BingSearchRun
from langchain_community.utilities import BingSearchAPIWrapper

load_dotenv()

key = os.environ.get("BING_SUBSCRIPTION_KEY")
os.environ["BING_SEARCH_URL"] = "https://api.bing.microsoft.com/v7.0/search"

ID = "71e4ddcc-4475-46f2-9816-894173b1292e"
bing_tool = BingSearchRun(api_wrapper=BingSearchAPIWrapper())
