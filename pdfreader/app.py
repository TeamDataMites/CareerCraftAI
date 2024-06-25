from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  
import uvicorn
import requests
import httpx

app = FastAPI()

def extract_text_from_pdf(file):
    document = fitz.open(stream=file, filetype="pdf")
    extracted_text = ""
    for page_num in range(len(document)):
        page = document.load_page(page_num)
        extracted_text += page.get_text()
        
    return extracted_text

@app.post("/extract-text")
async def extract_text(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        return JSONResponse(status_code=400, content={"message": "Invalid file type. Only PDFs are allowed."})
    
    pdf_content = await file.read()
    extracted_text = extract_text_from_pdf(pdf_content)

    return {"extratedtext": extracted_text}
