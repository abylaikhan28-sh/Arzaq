# arzaq/app/main.py

from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, place, comment, post, auth
from app import models # <--- Загружаем модели, чтобы SQLAlchemy их видела

# Создаем таблицы в БД (если их нет)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Arzaq API")

# Включаем роутеры
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(place.router)
app.include_router(comment.router)
app.include_router(post.router)

@app.get("/")
def root():
    return {"message": "Arzaq API is running! Check /docs"}