from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import models
from app.schemas.place import PlaceCreate, PlaceOut  # <- прямой импорт
from app.database import get_db

router = APIRouter(prefix="/places", tags=["places"])

@router.post("/", response_model=PlaceOut)
def create_place(place: PlaceCreate, db: Session = Depends(get_db)):
    db_place = models.Place(**place.dict(), owner_id=1)
    db.add(db_place)
    db.commit()
    db.refresh(db_place)
    return db_place

@router.get("/", response_model=list[PlaceOut])
def get_places(db: Session = Depends(get_db)):
    return db.query(models.Place).all()
