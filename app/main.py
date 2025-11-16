from fastapi import FastAPI
from app.database import engine, Base
from app.routers import user, place, comment, post

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(user.router)
app.include_router(place.router)
app.include_router(comment.router)
app.include_router(post.router)

@app.get("/")
def root():
    return {"message": "Arzaq API"}
