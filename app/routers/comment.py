from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.schemas.comment import CommentCreate, CommentOut  # <- прямой импорт схем
from app.database import get_db

router = APIRouter(prefix="/comments", tags=["comments"])

@router.post("/", response_model=CommentOut)
def create_comment(comment: CommentCreate, db: Session = Depends(get_db)):
    db_comment = models.Comment(**comment.dict(), owner_id=1)  # если есть владелец
    db.add(db_comment)
    db.commit()
    db.refresh(db_comment)
    return db_comment

@router.get("/", response_model=list[CommentOut])
def get_comments(db: Session = Depends(get_db)):
    return db.query(models.Comment).all()
