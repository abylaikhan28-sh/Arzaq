from pydantic import BaseModel

class PlaceCreate(BaseModel):
    name: str
    description: str | None = None
    owner_id: int

class PlaceOut(BaseModel):
    id: int
    name: str
    description: str | None = None
    owner_id: int

    class Config:
        orm_mode = True
