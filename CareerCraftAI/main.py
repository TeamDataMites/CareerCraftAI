from fastapi import FastAPI
from starlette.staticfiles import StaticFiles


from fastapi.middleware.cors import CORSMiddleware
from auth.authentication import router as auth_router
from router import model


app = FastAPI()
app.include_router(auth_router)
app.include_router(model.router)


origins = [
    'http://localhost:3000'
]

app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/pdf', StaticFiles(directory='pdf'), name='pdf')
