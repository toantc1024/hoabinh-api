from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import users, document, chat, visitor_logs
from app.db.qdrant import *
from app.config import config

app = FastAPI(title="BanDoSo - API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"], 
)

app.include_router(users.router)
app.include_router(chat.router)
app.include_router(document.router)
app.include_router(visitor_logs.router)