# arzaq/app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, place, comment, post, auth
from fastapi.middleware.cors import CORSMiddleware
from app import models


# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Arzaq API")



origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://arzaqmeal.vercel.app",
    "https://*.vercel.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Включаем роутеры
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(place.router)
app.include_router(comment.router)
app.include_router(post.router)

@app.get("/")
def root():
    return {"message": "Arzaq API is running! Check /docs"}
