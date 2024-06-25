from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from database import models
from database.database import engine
from auth import authentication
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()
app.include_router(authentication.router)


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

models.Base.metadata.create_all(engine)

app.mount('/pdf', StaticFiles(directory='pdf'), name='pdf')
