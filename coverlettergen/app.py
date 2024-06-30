from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
import os
from openai import OpenAI
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv()

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QueryRequest(BaseModel):
    query: str
    jobposition: str

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("Please set OPENAI_API_KEY environment variable")

client = OpenAI(api_key=openai_api_key)

def generate_cover_letter(query: str, jobposition: str):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages = [
            {
                "role": "system",
                "content": "The candidate has experience with Python, JavaScript, and React. The candidate has worked on projects involving {query}."
            },
            {
                "role": "user",
                "content": "Write a cover letter for a {jobposition} position."
            },
            {
                "role": "system",
                "content": "The candidate has experience with Python, JavaScript, and React. The candidate has worked on projects involving {query}."
            }
        ],
        temperature=0,
        max_tokens=1000
    )
    
    return response.choices[0].message.content

@app.post("/generate_cover_letter")
def search(query_request: QueryRequest):
    query = query_request.query.lower()
    jobposition = query_request.jobposition.lower()
    try:
        letter = generate_cover_letter(query, jobposition)
        return {"cover_letter": letter}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
