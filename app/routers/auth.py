from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.database import get_db
from app import models
from app.schemas.user import UserCreate, UserResponse
from app.schemas.auth import Token, TokenData 
from app.utils.security import (
    hash_password, 
    verify_password, 
    create_access_token, 
    get_current_user
)
from sqlalchemy import select
from datetime import timedelta
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm # <-- НОВЫЙ ИМПОРТ

# Настройки для срока жизни токена
ACCESS_TOKEN_EXPIRE_MINUTES = 30

router = APIRouter(
    prefix="/api/auth",
    tags=["Auth & Users"] # Тег для группировки в Swagger
)

# NOTE: Схема UserLogin больше не используется для роутера логина,
# но мы оставляем ее для примера, если захочешь использовать JSON-логин
class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    """Регистрирует нового пользователя."""
    
    # 1. ПРОВЕРКА УНИКАЛЬНОСТИ EMAIL
    existing_user = db.scalar(
        select(models.User).where(models.User.email == user.email)
    )
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )
    
    # --- 2. Хеширование пароля ---
    password_str = user.password 
    safe_password_bytes = password_str.encode("utf-8")[:72] 
    hashed_password = hash_password(safe_password_bytes)
    
    # Создаем словарь данных пользователя из Pydantic-модели
    new_user = user.model_dump()
    
    # КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Удаляем 'password', добавляем 'password_hash'
    del new_user["password"]
    new_user["password_hash"] = hashed_password
    
    # 3. Сохранение пользователя
    db_user = models.User(**new_user)
    db.add(db_user)
    
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Database error: {e}")
        
    db.refresh(db_user)
    
    return db_user

# ----------------------------------------------------------------------
# КРИТИЧЕСКОЕ ИСПРАВЛЕНИЕ: Роутер Логина теперь использует Form Data
# ----------------------------------------------------------------------
@router.post("/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), # <-- Используем Form Data
    db: Session = Depends(get_db)
):
    """Аутентификация пользователя и выдача JWT токена."""
    
    # В Form Data поле "username" соответствует нашему полю "email"
    email = form_data.username
    password = form_data.password

    # 1. Находим пользователя по email
    db_user = db.scalar(
        select(models.User).where(models.User.email == email)
    )

    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 2. Проверяем пароль
    if not verify_password(password, db_user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Генерируем токен
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": str(db_user.id)}, # 'sub' - это ID пользователя
        expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=UserResponse)
def read_users_me(current_user: dict = Depends(get_current_user), db: Session = Depends(get_db)):
    """Получает информацию о текущем аутентифицированном пользователе."""
    
    user_id = current_user.get("user_id")
    
    # 1. Находим пользователя по ID
    db_user = db.scalar(
        select(models.User).where(models.User.id == int(user_id))
    )
    
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        
    return db_user
