from pydantic import BaseModel

# Схема для токена доступа, возвращаемая после логина
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# Схема для проверки данных, хранящихся в токене.
class TokenData(BaseModel):
    user_id: str | None = None