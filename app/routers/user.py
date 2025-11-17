from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.user import UserResponse 
from app.utils.security import get_current_user
from sqlalchemy import select 
from pydantic import EmailStr

router = APIRouter(
    prefix="/api/users",
    tags=["Users Management"] 
)

# --- ЛОГИКА РЕГИСТРАЦИИ УДАЛЕНА И ПЕРЕМЕЩЕНА В app/routers/auth.py ---

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, 
                   db: Session = Depends(get_db), 
                   # Этот роут требует, чтобы пользователь был авторизован
                   current_user: dict = Depends(get_current_user)):
    """Получает пользователя по ID. Требуется JWT токен."""
    
    db_user = db.scalar(
        select(models.User).where(models.User.id == user_id)
    )
    
    if db_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="User not found"
        )
        
    return db_user