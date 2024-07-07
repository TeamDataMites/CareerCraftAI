from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from langchain_community.cache import GPTCache
from langchain.globals import set_llm_cache

from fastapi.middleware.cors import CORSMiddleware
from auth.authentication import router as auth_router
from cache import init_gptcache
from router import model, mail

#set_llm_cache(GPTCache(init_gptcache))


app = FastAPI()
app.include_router(auth_router)
app.include_router(model.router)
app.include_router(mail.router)


origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
    allow_origins=['*']
)

app.mount('/pdf', StaticFiles(directory='pdf'), name='pdf')
