import os
import dotenv
import json
from datetime import datetime
from typing import List

from typing import Literal
from langgraph.graph import MessageGraph, END, START
from langchain_openai import ChatOpenAI
from langchain_core.output_parsers.openai_tools import PydanticToolsParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, BaseMessage, AIMessage, ToolMessage

from utils.chat.report.output import TopicReport, ResponderWithRetries, ReviseAnswer, execute_tools, parser
from utils.chat.report.prompt import SYSTEM_PROMPT, SYSTEM_PROMPT_REVISE

from termcolor import colored


dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')



class Reflexion:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4o')
        self.llmy = ChatOpenAI(model='gpt-4-turbo-2024-04-09')
        self.actor_prompt = ChatPromptTemplate.from_messages(
                                [
                                    ("system", SYSTEM_PROMPT),
                                    MessagesPlaceholder(variable_name="messages"),
                                    (
                                        "user",
                                        "\n\n<reminder>Reflect on the user's original question and the"
                                        " actions taken thus far. Respond using the {function_name} functions.</reminder>",
                                    ),
                                ]
                            ).partial(time = lambda:datetime.now().isoformat())

    def report_agent(self):

        initial_answer_chain = self.actor_prompt.partial(
        first_instruction="Provide a structured report covering all the aspects mentioned above.",
        function_name=TopicReport.__name__,
        ) | self.llmy.bind_tools(tools=[TopicReport], tool_choice='TopicReport')
        validator = PydanticToolsParser(tools=[TopicReport])

        first_responder = ResponderWithRetries(
            runnable=initial_answer_chain, validator=validator
        )

        return first_responder

    def reflexion(self):
        revision_chain = self.actor_prompt.partial(
            first_instruction=SYSTEM_PROMPT_REVISE,
            function_name=ReviseAnswer.__name__,
        ) | self.llm.bind_tools(tools=[ReviseAnswer], tool_choice='ReviseAnswer')
        revision_validator = PydanticToolsParser(tools=[ReviseAnswer])

        revisor = ResponderWithRetries(runnable=revision_chain, validator=revision_validator)

        return revisor


reflexion = Reflexion()

first_responder = reflexion.report_agent()

revisor = reflexion.reflexion()

    
MAX_ITERATIONS=5

builder = MessageGraph()

builder.add_node("draft", first_responder.respond)
builder.add_node("execute_tools", execute_tools)
builder.add_node("revise", revisor.respond)

builder.add_edge("draft", "execute_tools")
builder.add_edge("execute_tools", "revise")

def _get_num_iterations(state: List[BaseMessage]):
    i = 0
    for m in state[::-1]:
        if not isinstance(m, (ToolMessage, AIMessage)):
            break
        i += 1
    return i


def should_continue(state: List[BaseMessage]) -> str:
    # in our case, we'll just stop after N plans
    num_iterations = _get_num_iterations(state)
    if num_iterations > MAX_ITERATIONS:
        return END
    return "execute_tools"



builder.add_conditional_edges("revise", should_continue)
builder.add_edge(START, "draft")
graph = builder.compile()

def run_report_agent(desc: str):
    answer = graph.invoke([HumanMessage(content=desc)])
    # print(colored(answer[-1], 'blue'))
    # print('\n\n')
    # print(colored(answer, 'green'))
    item = json.loads(answer[-1].additional_kwargs['tool_calls'][0]['function']['arguments'])
    return item['report']
