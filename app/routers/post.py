# arzaq/app/routers/post.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.post import Post as PostModel 
from app.schemas.post import PostCreate, PostResponse
from app.utils.security import get_current_user
from app.schemas.user import UserResponse

router = APIRouter(
    prefix="/api/posts",
    tags=["Posts"],
)

# 1. СОЗДАНИЕ ПОСТА (CREATE)
@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(
    post_data: PostCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user) 
):
    new_post = PostModel(
        **post_data.model_dump(),
        user_id=current_user.id 
    )
    
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# 2. ЧТЕНИЕ ВСЕХ ПОСТОВ (READ ALL)
@router.get("/", response_model=List[PostResponse])
def read_posts(db: Session = Depends(get_db)):
    posts = db.query(PostModel).all()
    return posts

# 3. ОБНОВЛЕНИЕ ПОСТА (UPDATE)
@router.put("/{post_id}", response_model=PostResponse)
def update_post(
    post_id: int, 
    post_data: PostCreate,
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user)
):
    post_query = db.query(PostModel).filter(PostModel.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this post (Forbidden)"
        )
    post_query.update(post_data.model_dump(exclude_unset=True), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post
    
# 4. УДАЛЕНИЕ ПОСТА (DELETE)
@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    post_id: int, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user) 
):
    post_query = db.query(PostModel).filter(PostModel.id == post_id)
    post = post_query.first()
    
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id {post_id} not found"
        )
    if post.user_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this post (Forbidden)"
        )
        
    post_query.delete(synchronize_session=False)
    db.commit()
    return