from typing import List, Sequence 
from langgraph.graph import MessageGraph, END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage

from utils.chat.mindmap.prompt import SYSTEM_PROMPT
import dotenv
import os

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')



class Reflexion:
    def __init__(self):
        self.search = TavilySearchResults(max_results=3)
        self.llm = ChatOpenAI(model='gpt-4o')
        self.llmy = ChatOpenAI(model='gpt-4-turbo-2024-04-09')

    def report_agent(self, desc: str = None):

        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    SYSTEM_PROMPT,
                ),
                MessagesPlaceholder(variable_name="messages"),
            ]
        )

        generate = prompt.partial(desc=desc) | self.llm

        return generate

    def reflexion(self):
        pass 

    def run_queries(search_queries: list[str], **kwargs):
        """Run the generated queries."""
        return Reflexion.search.batch([{"query": query} for query in search_queries])
    
    def tool_node(self):
        pass