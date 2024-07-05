import json
import asyncio
from typing import Optional
from langgraph.graph import END, StateGraph
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, ToolMessage
from langgraph.checkpoint.memory import MemorySaver
from langchain_core.documents import Document
from langchain_core.runnables import RunnableConfig
from langchain_core.runnables import RunnableLambda
from langchain_core.runnables import chain as as_runnable
from langchain_core.output_parsers import StrOutputParser
from utils.chat.notes.prompt import (outline_llm_prompt, 
                                     refine_outline_prompt, 
                                     section_writer_prompt, 
                                     writer_prompt, 
                                     gen_related_topics_prompt, 
                                     gen_perspectives_prompt,
                                     gen_queries_prompt,
                                     gen_answer_prompt,
                                     gen_qa_prompt)
from utils.chat.notes.output import Outline, RelatedSubjects, Perspectives, Queries, AnswerWithCitations, LectureSection
from utils.chat.notes.retrievers import wikipedia_retriever, format_docs, search_engine, vectorstore, retrieve
from utils.chat.notes.helpers import swap_roles, tag_with_name, InterviewState, ResearchState


import dotenv
import os

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')

llm = ChatOpenAI(model='gpt-4o')
llmy = ChatOpenAI(model='gpt-4-turbo-2024-04-09')


generate_outline_chain = outline_llm_prompt | llm.with_structured_output(Outline)
expand_chain = gen_related_topics_prompt | llm.with_structured_output(RelatedSubjects)
gen_perspectives_chain = gen_perspectives_prompt | llm.with_structured_output(Perspectives)
gen_queries_chain = gen_queries_prompt | llm.with_structured_output(Queries, include_raw=True)
gen_answers_chain = gen_answer_prompt | llmy.with_structured_output(AnswerWithCitations, include_raw=True)
refine_outline_chain = refine_outline_prompt | llm.with_structured_output(Outline)
write_section_chain = retrieve | section_writer_prompt | llm.with_structured_output(LectureSection)
write_lecture_chain = writer_prompt | llm | StrOutputParser()

# class LectureGenerator:
#     def __init__(self):
#         self.llm = ChatOpenAI(model='gpt-4o')
#         self.llmy = ChatOpenAI(model='gpt-4-turbo-2024-04-09')
        
#     # def generate_outline(self):
#     #     generate_outline_chain = outline_llm_prompt | self.llm.with_structured_output(Outline)
#     #     return generate_outline_chain
    
#     # def expand_chain(self):
#     #     expand_chain = gen_related_topics_prompt | self.llm.with_structured_output(RelatedSubjects)
#     #     return expand_chain
    
#     # def gen_perspectives(self):
#     #     gen_perspectives_chain = gen_perspectives_prompt | self.llm.with_structured_output(Perspectives)
#     #     return gen_perspectives_chain
    
#     def gen_queries(self):
#         gen_queries_chain = gen_queries_prompt | self.llm.with_structured_output(Queries, include_raw=True)
#         return gen_queries_chain

#     def gen_answers(self):
#         gen_answers_chain = gen_answer_prompt | self.llmy.with_structured_output(AnswerWithCitations, include_raw=True)
#         return gen_answers_chain
    
#     def refine_outline(self):
#         refine_outline_chain = refine_outline_prompt | self.llm.with_structured_output(Outline)
#         return refine_outline_chain
    
#     def write_section(self, retrieve: dict):
#         write_section_chain = retrieve | section_writer_prompt | self.llmy.with_structured_output(LectureSection)
#         return write_section_chain
    
#     def write_lecture(self):
#         write_lecture_chain = writer_prompt | self.llm | StrOutputParser()
#         return write_lecture_chain

@as_runnable
async def survey_subjects(input: dict):
    related_subjects = await expand_chain.ainvoke({"topic": input['topic'], "domain": input['domain']})
    retrieved_docs = await wikipedia_retriever.abatch(related_subjects.topics, return_exceptions=True)

    doc_list = []
    for doc in retrieved_docs:
        if isinstance(doc, BaseException):
            continue
        doc_list.extend(doc)
    formatted_docs = format_docs(doc_list)
    return gen_perspectives_chain.invoke({"topic": input['topic'], "examples": formatted_docs})


@as_runnable
async def generate_question(state: InterviewState):
    editor = state['editor']
    gn_chain = (
        RunnableLambda(swap_roles).bind(name=editor.name)
        | gen_qa_prompt.partial(persona=editor.persona)
        | llmy
        | RunnableLambda(tag_with_name).bind(name=editor.name)
    )
    result = await gn_chain.ainvoke(state)
    return {"messages": [result]}


async def gen_answer(
    state: InterviewState,
    config: Optional[RunnableConfig] = None,
    name: str = "Subject_Matter_Expert",
    max_str_len: int = 15000,
):
    swapped_state = swap_roles(state, name)
    queries = await gen_queries_chain.ainvoke(swapped_state)
    query_results = await search_engine.abatch(
        queries["parsed"].queries, config, return_exceptions=True
    )
    successful_results = [
        res for res in query_results if not isinstance(res, Exception)
    ]
    all_query_results = {
        res["url"]: res["content"] for results in successful_results for res in results
    }

    dumped = json.dumps(all_query_results)[:max_str_len]
    ai_message: AIMessage = queries["raw"]
    tool_call = queries["raw"].additional_kwargs["tool_calls"][0]
    tool_id = tool_call["id"]
    tool_message = ToolMessage(tool_call_id=tool_id, content=dumped)
    swapped_state["messages"].extend([ai_message, tool_message])

    generated = await gen_answers_chain.ainvoke(swapped_state)
    cited_urls = set(generated["parsed"].cited_urls)

    cited_references = {k: v for k, v in all_query_results.items() if k in cited_urls}
    formatted_message = AIMessage(name=name, content=generated["parsed"].as_str)
    return {"messages": [formatted_message], "references": cited_references}

max_num_turns = 5

def route_messages(state: InterviewState, name: str = "Subject_Matter_Expert"):
    messages = state["messages"]
    num_responses = len(
        [m for m in messages if isinstance(m, AIMessage) and m.name == name]
    )
    if num_responses >= max_num_turns:
        return END
    last_question = messages[-2]
    if last_question.content.endswith("Thank you so much for your help!"):
        return END
    return END

def interview_graph():
    builder = StateGraph(InterviewState)

    builder.add_node("ask_question", generate_question)
    builder.add_node("answer_question", gen_answer)
    builder.add_conditional_edges("answer_question", route_messages)
    builder.add_edge("ask_question", "answer_question")

    builder.set_entry_point("ask_question")
    interview_graph = builder.compile().with_config(run_name="Conduct Interviews")
    return interview_graph

interview_agent = interview_graph()

async def initialize_research(state: ResearchState):
    topic = state["topic"]
    domain = state['domain']
    coros = (
        generate_outline_chain.ainvoke({"topic": topic, "domain": domain}),
        survey_subjects.ainvoke({"topic": topic, "domain": domain}),
    )
    results = await asyncio.gather(*coros)
    return {
        **state,
        "outline": results[0],
        "editors": results[1].editors,
    }

async def conduct_interviews(state: ResearchState):
    topic = state["topic"]
    initial_states = [
        {
            "editor": editor,
            "messages": [
                AIMessage(
                    content=f"So you said you were writing an article on {topic}?",
                    name="Subject_Matter_Expert",
                )
            ],
        }
        for editor in state["editors"]
    ]
    # We call in to the sub-graph here to parallelize the interviews
    interview_results = await interview_graph.abatch(initial_states)

    return {
        **state,
        "interview_results": interview_results,
    }

def format_conversation(interview_state):
    messages = interview_state["messages"]
    convo = "\n".join(f"{m.name}: {m.content}" for m in messages)
    return f'Conversation with {interview_state["editor"].name}\n\n' + convo


async def refine_outline(state: ResearchState):
    convos = "\n\n".join(
        [
            format_conversation(interview_state)
            for interview_state in state["interview_results"]
        ]
    )

    updated_outline = await refine_outline_chain.ainvoke(
        {
            "topic": state["topic"],
            "old_outline": state["outline"].as_str,
            "conversations": convos,
        }
    )
    return {**state, "outline": updated_outline}

async def conduct_interviews(state: ResearchState):
    topic = state["topic"]
    initial_states = [
        {
            "editor": editor,
            "messages": [
                AIMessage(
                    content=f"So you said you were writing an article on {topic}?",
                    name="Subject_Matter_Expert",
                )
            ],
        }
        for editor in state["editors"]
    ]
    # We call in to the sub-graph here to parallelize the interviews
    interview_results = await interview_agent.abatch(initial_states)

    return {
        **state,
        "interview_results": interview_results,
    }

async def index_references(state: ResearchState):
    all_docs = []
    for interview_state in state["interview_results"]:
        reference_docs = [
            Document(page_content=v, metadata={"source": k})
            for k, v in interview_state["references"].items()
        ]
        all_docs.extend(reference_docs)
    await vectorstore.aadd_documents(all_docs)
    return state


async def write_sections(state: ResearchState):
    outline = state["outline"]
    sections = await write_section_chain.abatch(
        [
            {
                "outline": section.as_str,
                "section": section.section_title,
                "topic": state["topic"],
            }
            for section in outline.sections
        ]
    )
    return {
        **state,
        "sections": sections,
    }

async def write_script(state: ResearchState):
    topic = state["topic"]
    sections = state["sections"]
    domain = state["domain"]
    draft = "\n\n".join([section.as_str for section in sections])
    article = await write_lecture_chain.ainvoke({"topic": topic, "draft": draft, "domain": domain})
    return {
        **state,
        "article": article,
    }


def lecture_graph():
    lecture_storm = StateGraph(ResearchState)

    nodes = [
        ("init_research", initialize_research),
        ("conduct_interviews", conduct_interviews),
        ("refine_outline", refine_outline),
        ("index_references", index_references),
        ("write_sections", write_sections),
        ("write_script", write_script),
    ]

    for i in range(len(nodes)):
        name, node = nodes[i]
        lecture_storm.add_node(name, node)
        if i > 0:
            lecture_storm.add_edge(nodes[i - 1][0], name)


    lecture_storm.set_entry_point(nodes[0][0])
    lecture_storm.set_finish_point(nodes[-1][0])
    storm = lecture_storm.compile(checkpointer=MemorySaver())
    return storm

async def run_graph(topic: str, domain: str):
    config = {"configurable": {"thread_id": "my-thread"}}
    storm = lecture_graph()
    async for step in storm.astream(
        {
            "topic": topic,
            "domain": domain,
        },
        config,
    ):
        name = next(iter(step))
        print(name)
        print("-- ", str(step[name])[:300])

    checkpoint = storm.get_state(config)
    article = checkpoint.values["article"]
    return article