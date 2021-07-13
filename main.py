from fastapi import FastAPI, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import *
from app.db import MongoDB
from app.routes import users_routes, requests_routes


app = FastAPI()

allowed_origins = [
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

db = MongoDB()


@app.get("/")
async def root():
    return {"status": 200}


app.include_router(users_routes.router)
app.include_router(requests_routes.router)
