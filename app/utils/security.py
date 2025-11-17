import bcrypt # Используем bcrypt напрямую!
import os
from datetime import datetime, timedelta
from typing import Optional
from jose import jwt, JWTError
from fastapi import Depends, HTTPException, status # Добавлены Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

# Загрузка переменных окружения (SECRET_KEY)
load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Настройки для хэширования
BCRYPT_ROUNDS = 12

# Используем OAuth2PasswordBearer для получения токена из заголовков
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/login")

# --- ФУНКЦИИ ХЕШИРОВАНИЯ БЕЗ PASSLIB ---

def hash_password(password: bytes): 
    """Хэширует пароль, используя bcrypt."""
    # Генерируем "соль"
    salt = bcrypt.gensalt(rounds=BCRYPT_ROUNDS)
    # Хэшируем пароль с солью, возвращает байты
    return bcrypt.hashpw(password, salt).decode("utf-8") # Декодируем в строку для сохранения в БД

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Проверяет пароль."""
    # Кодируем оба значения в байты для сравнения
    hashed_bytes = hashed_password.encode("utf-8")
    plain_bytes = plain_password.encode("utf-8")
    
    # Сравниваем хэш и пароль
    return bcrypt.checkpw(plain_bytes, hashed_bytes)

# --- ФУНКЦИИ JWT ---

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        # Срок жизни токена по умолчанию: 30 минут
        expire = datetime.utcnow() + timedelta(minutes=30)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# --- ФУНКЦИИ АУТЕНТИФИКАЦИИ (DEPENDENCIES) ---

def verify_token(token: str, credentials_exception):
    """Проверяет JWT токен и возвращает полезную нагрузку (payload)."""
    try:
        # Декодируем токен
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        # Проверяем наличие 'sub' (user id)
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return payload
    except JWTError:
        raise credentials_exception

# Функция, которую искал роутер place.py
def get_current_user(token: str = Depends(oauth2_scheme)):
    """Извлекает и проверяет текущего пользователя из токена."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    # Используем функцию verify_token
    payload = verify_token(token, credentials_exception)
    
    # Возвращаем user_id
    return {"user_id": payload.get("sub")}