from pydantic import BaseModel

class CommentCreate(BaseModel):
    text: str
    user_id: int
    place_id: int

class CommentOut(BaseModel):
    id: int
    text: str
    user_id: int
    place_id: int

    class Config:
        orm_mode = True
