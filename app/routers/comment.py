# arzaq/app/routers/comment.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.comment import Comment as CommentModel 
from app.models.place import Place as PlaceModel 
from app.schemas.comment import CommentCreate, CommentResponse
from app.utils.security import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/api/comments",
    tags=["Comments"],
)

# 1. СОЗДАНИЕ КОММЕНТАРИЯ (CREATE)
@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    comment_data: CommentCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user) 
):
    place = db.query(PlaceModel).filter(PlaceModel.id == comment_data.place_id).first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {comment_data.place_id} not found"
        )
    
    new_comment = CommentModel(
        **comment_data.model_dump(),
        user_id=current_user.id
    )
    
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

# 2. ЧТЕНИЕ ВСЕХ КОММЕНТАРИЕВ (READ ALL)
@router.get("/", response_model=List[CommentResponse])
def read_comments(place_id: int = None, db: Session = Depends(get_db)):
    query = db.query(CommentModel)
    if place_id:
        query = query.filter(CommentModel.place_id == place_id)
        
    comments = query.all()
    return comments

# 3. УДАЛЕНИЕ КОММЕНТАРИЯ (DELETE)
@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    comment_id: int, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    comment_query = db.query(CommentModel).filter(CommentModel.id == comment_id)
    comment = comment_query.first()
    
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with id {comment_id} not found"
        )
        
    if comment.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this comment (Forbidden)"
        )
        
    comment_query.delete(synchronize_session=False)
    db.commit()
    return