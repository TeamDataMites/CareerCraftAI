from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import requests
import httpx
import ocrrawtoconetxt
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pymongo import MongoClient
import dotenv
import os
import recommendations

# Load environment variables from .env file
dotenv.load_dotenv()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=['*']
)

class TextRequest(BaseModel):
    extract_text: str

class SearchRequest(BaseModel):
    username: str
    desc: str

class SearchUserRequest(BaseModel):
    username: str

class IndexesFound(BaseModel):
    indexes: list

MONGODB_URL = os.getenv("MONGODB_URL")

client = MongoClient(MONGODB_URL)

db_name = MONGODB_URL.split('/')[-1].split('?')[0]
db = client[db_name]

collection_name = "career_searches"
collection = db[collection_name]

@app.post("/server/ocrtextcontext")
async def middleware(textrequest: TextRequest):
    cleaned_text = ocrrawtoconetxt.json_clean(textrequest.extract_text)
    return JSONResponse(content=cleaned_text)

@app.post("/server/retrievesearches")
async def retrievesearches(searchuserrequest: SearchUserRequest):
    results = []
    cursor = collection.find({"username": searchuserrequest.username})
    for document in cursor:
        results.append(document["desc"])
    
    if len(results) == 0:
        return JSONResponse(content={"status": "error", "search_results": "No search results found."})
    else:
        return JSONResponse(content={"status": "success", "search_results": results[0]})


@app.post("/server/recommendations")
async def recommendation(indexesfound: IndexesFound):
    recommendedlist = recommendations.recommender(indexesfound.indexes)
    return recommendedlist



@app.post("/server/saveinmongo")
async def saveinmongo(searchrequest: SearchRequest):
    document = {
        "username": searchrequest.username,
        "desc": searchrequest.desc
    }
    result = collection.insert_one(document)
    return JSONResponse(content={"status": "success", "inserted_id": str(result.inserted_id)})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
