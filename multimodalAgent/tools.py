import os
from typing import Annotated
from dotenv import load_dotenv

from exa_py import Exa
from livekit import agents
from livekit.agents import (
    llm,
)
from livekit.agents.voice_assistant import AssistantContext

load_dotenv()
exa = Exa(api_key=os.getenv('EXA_API_KEY'))


class AssistantFunctions(llm.FunctionContext):

    @agents.llm.ai_callable(
        desc=(
                "Called when it is necessary to use webcam for any task"
                "Used to see the user and identify who asked the question"
                "uses webcam to identify who asked the question and to analyze their facial expressions before & after answering."
        )
    )
    async def image(
            self,
            user_msg: Annotated[
                str,
                agents.llm.TypeInfo(desc="The user message that triggered this function"),
            ],
    ):
        print(f"Message triggering vision capabilities: {user_msg}")
        context = AssistantContext.get_current()
        context.store_metadata("user_msg", user_msg)

    @agents.llm.ai_callable(
        desc=(
                "Can be used to search the web."
                "When asked questions related to your talk/context, but you do not know the answer."
        )
    )
    async def search(
            self,
            user_query: Annotated[
                str,
                agents.llm.TypeInfo(desc="The query to search the web.")
            ]
    ):
        print(f"Message triggering search capabilities: {user_query}")

        context = AssistantContext.get_current()
        results_resp = exa.search_and_contents(
            user_query,
            type='neural',
            use_autoprompt=True,
            num_results=4,
            text=True
        )
        results = ''
        for i in range(3):
            res = f'<result{i+1}> source: {results_resp.results[i].url} title: {results_resp.results[i].title}' + results_resp.results[i].text[:500] + '</result>\n\n'
            results.join(res)
        context.store_metadata("user_search", {'search_results': results, 'question': user_query})

    # @agents.llm.ai_callable(
    #     desc=(
    #         "Used to Retrieve the lecture transcript."
    #     )
    # )
    # async def retrieve(
    #         self
    # ):
    #     print("Retrieving lecture notes.")
    #

