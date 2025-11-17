# arzaq/app/schemas/place.py

from pydantic import BaseModel

class PlaceCreate(BaseModel):
    name: str
    latitude: float
    longitude: float

class PlaceResponse(BaseModel):
    id: int
    name: str
    latitude: float
    longitude: float
    owner_id: int

    class Config:
        from_attributes = True