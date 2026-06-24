from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os

from app.api import auth, books, orders
from app.core.database import engine, Base
from app.core.config import settings

# Создание таблиц
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_TITLE)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Static files
if os.path.exists("frontend/assets"):
    app.mount("/assets", StaticFiles(directory="frontend/assets"), name="assets")

# Роутеры
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(orders.router)

@app.get("/")
def root():
    return {"message": "BookStore API", "version": "1.0.0"}