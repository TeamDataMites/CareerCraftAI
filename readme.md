# **CareerCraftAI**

CareerCraftAI is Interview preparation assistant that help in various fields using generative AI.
- It has AI voice help desk
- Mock interview chatbot 
- Job Recommendation
- Resume Optimizer
- Cover Letter Generator
- Mind Map Generator
- Lecture Note Generator
- Job research

## **Installation**

Folder Structure of this application
```bash
|
|- candi_bot
|- CareerCraftAI
|- client
|- coverlettergen
|- ocr-tesseract-docker
|- pdfreader
|- sementicsearch
|- server
```

### 1.candi_bot
set up environment variables as following in the .env file
```bash
GEMINI_API_KEY= 
GEMINI_API_ENDPOINT= 
MONGO_URI= 
DATABASE_NAME= "CVS"
COLLECTION_NAME= "result"
```
then run following commands in terminal
```bash
pip install --no-cache-dir -r requirements.txt
python app.py
```
### 2.CareerCraftAI
set up environment variables as following in the .env file
```bash
OPENAI_API_KEY = 
TAVILY_API_KEY = 
EXA_API_KEY = 
NVIDIA_NIM_API_KEY =
JINA_API_KEY =

MAIL_USERNAME=
MAIL_PASSWORD=
MAIL_FROM=
MAIL_TO=
PLAY_HT_ID=
PLAY_HT_API_KEY=
CARTESIA_SPEECH_KEY=
DEEPGRAM_API_KEY=
```
then run following commands in terminal
```bash
pip install --no-cache-dir -r requirements.txt
uvicorn main:app --port 8081 --reload
```
### 3.client
run following commands in terminal
```bash
npm install
npm start
```

### 4.coverlettergen
run following commands in terminal
```bash
cd cover-letter-gen
docker build -t cover-letter-gen .
docker run -e OPENAI_API_KEY="sk-xx" -p 8081:8081 cover-letter-gen
```

### 5.ocr-tesseract-docker
run following commands in terminal
```bash
cd ocr-tesseract-docker
docker build -t ocr-tesseract-docker .  
docker run -d -p 5000:5000 ocr-tesseract-docker   
```

### 6.pdfreader
run following commands in terminal
```bash
cd pdfreader
docker build -t pdfreader .            
docker run -p 8080:8080 pdfreader 
```

### 7.sementic-search 
run following commands in terminal
```bash
cd sementic-search 
docker build -t sementic-search . 
docker run -e OPENAI_API_KEY="sk-xx" -p 8084:8084 sementic-search
```

### 8.server
set up environment variables as following in the .env file
```bash
MONGODB_URL = 
```
then run following commands in terminal
```bash
cd server
docker build -t server . 
docker run -e OPENAI_API_KEY="sk-xx" -p 8082:8082 server
```

## Usage

```python
import foobar


```

## Contributing


## License
