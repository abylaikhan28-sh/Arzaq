from pydantic import BaseModel

class PostCreate(BaseModel):
    title: str
    content: str | None = None
    user_id: int

class PostOut(BaseModel):
    id: int
    title: str
    content: str | None = None
    user_id: int

    class Config:
        orm_mode = True
