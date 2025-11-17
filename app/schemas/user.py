from pydantic import BaseModel, Field, EmailStr

# Базовая схема, от которой наследуются другие
class UserBase(BaseModel):
    # КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ: Используем EmailStr. 
    # Это заставит Pydantic требовать формат "имя@домен.зона"
    email: EmailStr = Field(...) 
    full_name: str = Field(...)
    
# Схема для создания (регистрации) нового пользователя
class UserCreate(UserBase):
    password: str = Field(...)
    
# Схема, которая возвращается в ответе API
class UserResponse(UserBase):
    id: int
    role: str = "user"
    
    # Конфигурация для SQLAlchemy
    class Config:
        from_attributes = True
