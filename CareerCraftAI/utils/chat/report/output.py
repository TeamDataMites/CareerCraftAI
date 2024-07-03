import os
import json
import dotenv
from typing import List
from langsmith import traceable
from collections import defaultdict
from langchain_core.messages import ToolMessage
from langchain_core.pydantic_v1 import BaseModel, Field, ValidationError
from langchain_core.output_parsers.openai_tools import JsonOutputToolsParser
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.messages import BaseMessage, AIMessage, HumanMessage
from langgraph.prebuilt import ToolExecutor, ToolInvocation

from termcolor import colored

dotenv.load_dotenv()
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

search = TavilySearchAPIWrapper()
search_tool = TavilySearchResults(api_wrapper=search, max_results=5)
tool_executor = ToolExecutor([search_tool])

parser = JsonOutputToolsParser(return_id=True)

class Reflection(BaseModel):
  missing: str = Field(description="critique of what's missing.")
  superfluous: str = Field(description="critique of what's superfluous.")

class TopicReport(BaseModel):
    """Create Report under the Topic. Provide a Report, reflection, and then follow up with search queries to improve the answer."""

    report: str = Field(description="~500 word detailed report to the job.")
    reflection: Reflection = Field(description="Your reflection on the initial report.")
    search_queries: list[str] = Field(
        description="1-3 search queries for researching improvements to address the critique of your current answer."
    )
class ReviseAnswer(TopicReport):
    """Revise your original answer to your question. Provide an answer, reflection,

    cite your reflection with references, and finally
    add search queries to improve the answer."""

    references: list[str] = Field(
        description="Citations motivating your updated answer."
    )


def execute_tools(state: List[BaseMessage]) -> List[BaseMessage]:
    tool_invocation: AIMessage = state[-1]
    parsed_tool_calls = parser.invoke(tool_invocation)
    ids = []
    tool_invocations = []
    for tool_call in parsed_tool_calls:
        for query in tool_call['args']['search_queries']:
            print(colored(f"current tool call: {tool_call}", 'green'))
            tool_invocations.append(ToolInvocation(tool='tavily_search_result_json', tool_input=query))
        ids.append(tool_call['id'])
    
    outputs = tool_executor.batch(tool_invocations)
    outputs_map = defaultdict(dict)
    for _id, output, invocations in zip(ids, outputs, tool_invocations):
        outputs_map[_id][invocations.tool_input] = output
    return [
        ToolMessage(content=json.dumps(query_outputs), tool_call_id=id_)
        for id_, query_outputs in outputs_map.items()
    ]

class ResponderWithRetries:
    def __init__(self, runnable, validator):
        self.runnable = runnable
        self.validator = validator

    @traceable
    def respond(self, state: List[BaseMessage]):
        response = []
        for attempt in range(3):
            try:
                response = self.runnable.invoke({"messages": state})
                self.validator.invoke(response)
                return response
            except ValidationError as e:
                state = state + [HumanMessage(content=repr(e))]
        return response
   