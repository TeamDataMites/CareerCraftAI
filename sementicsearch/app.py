from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import os
import re

from langchain_openai import OpenAI
from langchain_community.document_loaders import CSVLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS

app = FastAPI()

class QueryRequest(BaseModel):
    query: str
    top_k: Optional[int] = 10


openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

loader = CSVLoader('job_data.csv')
documents = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=0,
)
docs  = text_splitter.split_documents(documents)

embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
library = FAISS.from_documents(docs, embeddings)

def extract_indexes(documents: List[object]) -> List[int]:
    indexes = []
    for doc in documents:
        page_content = getattr(doc, 'page_content', '')
        match = re.search(r'index:\s*(\d+)', page_content)
        if match:
            indexes.append(int(match.group(1)))
    return indexes

@app.post("/search")
def search(query_request: QueryRequest):
    query = query_request.query.lower()
    top_k = query_request.top_k
    
    try:
        query_answer = library.similarity_search(query, top_k=top_k)
        indexes = extract_indexes(query_answer)
        return {"indexes": indexes}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
