from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import uvicorn
import requests
import httpx
import ocrrawtoconetxt
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

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


@app.post("/middleware/ocrtextcontext")
async def middleware(textrequest: TextRequest):
  cleaned_text = ocrrawtoconetxt.json_clean(textrequest.extract_text)
  
  return JSONResponse(content=cleaned_text)

  