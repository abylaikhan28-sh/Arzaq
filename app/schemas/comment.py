# arzaq/app/schemas/comment.py

from pydantic import BaseModel

class CommentCreate(BaseModel):
    place_id: int 
    text: str

class CommentResponse(BaseModel):
    id: int
    text: str
    user_id: int
    place_id: int

    class Config:
        from_attributes = True