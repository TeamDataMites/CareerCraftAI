from typing import List, Sequence, TypedDict 
from langgraph.graph import END
from langchain_openai import ChatOpenAI
from langchain_core.tools import tool
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import AIMessage, BaseMessage, HumanMessage
from langchain_core.output_parsers import StrOutputParser
from utils.chat.notes.prompt import (outline_llm_prompt, 
                                     refine_outline_prompt, 
                                     section_writer_prompt, 
                                     writer_prompt, 
                                     gen_related_topics_prompt, 
                                     gen_perspectives_prompt,
                                     gen_queries_prompt,
                                     gen_answer_prompt)
from utils.chat.notes.output import Outline, Section, Subsection, RelatedSubjects, Editor, Perspectives, Queries, AnswerWithCitations


import dotenv
import os

dotenv.load_dotenv()
os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')
os.environ['TAVILY_API_KEY'] = os.getenv('TAVILY_API_KEY')


class LectureGenerator:
    def __init__(self):
        self.llm = ChatOpenAI(model='gpt-4o')
        self.llmy = ChatOpenAI(model='gpt-4-turbo-2024-04-09')
        self.llmx = ChatOpenAI(model='gpt-3.5-turbo')
        
    def generate_outline(self):
        generate_outline_chain = outline_llm_prompt | self.llm.with_structured_output(Outline)
        return generate_outline_chain
    
    def expand_chain(self):
        expand_chain = gen_related_topics_prompt | self.llm.with_structured_output(RelatedSubjects)
        return expand_chain
    
    def gen_perspectives(self):
        gen_perspectives_chain = gen_perspectives_prompt | self.llm.with_structured_output(Perspectives)
        return gen_perspectives_chain
    
    def gen_queries(self):
        gen_queries_chain = gen_queries_prompt | self.llm.with_structured_output(Queries, include_raw=True)
        return gen_queries_chain

    def gen_answers(self):
        gen_answers_chain = gen_answer_prompt | self.llmy.with_structured_output(AnswerWithCitations, include_raw=True)
        return gen_answers_chain
    
    