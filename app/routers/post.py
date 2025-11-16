from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.schemas.post import PostCreate, PostOut  # <- прямой импорт схем
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["posts"])

@router.post("/", response_model=PostOut)
def create_post(post: PostCreate, db: Session = Depends(get_db)):
    db_post = models.Post(**post.dict(), owner_id=1)  # если есть владелец
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@router.get("/", response_model=list[PostOut])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
