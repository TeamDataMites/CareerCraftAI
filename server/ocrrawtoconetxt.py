import requests
from bs4 import BeautifulSoup
import pandas as pd 
import sqlite3
import re
import json
import os
from langchain.chat_models import ChatOpenAI
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from dotenv import load_dotenv

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")


def json_clean(extracted_text):
    template = (
        "Identify and Extract the data related to job vacancy:\n" 
        "vacany , company, job Requirements, contact details\n"
        "from text if not keep as None\n\n"
        + extracted_text + 
        "give summerized job requirements and responsibilities only as a paragraph no need company details or contact"
    ).replace("{", "{{").replace("}", "}}")

    prompt = PromptTemplate(template=template, input_variables=[])

    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY', 'your_openai_api_key')

    llm = ChatOpenAI(model="gpt-3.5-turbo", openai_api_key=OPENAI_API_KEY)

    chain = LLMChain(prompt=prompt, llm=llm)

    output = chain.run({})

    try:
        return output
    except json.JSONDecodeError:
        print("Failed to decode JSON response")


def run_ocr_pipeline(extracted_text):
    cleaned_text = json_clean(extracted_text)
    return cleaned_text
