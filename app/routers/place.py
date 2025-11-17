# arzaq/app/routers/place.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.database import get_db
from app.models.place import Place as PlaceModel 

from app.schemas.place import PlaceCreate, PlaceResponse
from app.utils.security import get_current_user
from app.schemas.user import UserResponse 

router = APIRouter(
    prefix="/api/places",
    tags=["Places"],
)

# 1. СОЗДАНИЕ МЕСТА (CREATE)
@router.post("/", response_model=PlaceResponse, status_code=status.HTTP_201_CREATED)
def create_place(
    place_data: PlaceCreate, 
    db: Session = Depends(get_db), 
    current_user: UserResponse = Depends(get_current_user) 
):
    new_place = PlaceModel(
        **place_data.model_dump(),
        owner_id=current_user.id 
    )
    db.add(new_place)
    db.commit()
    db.refresh(new_place)
    return new_place

# 2. ЧТЕНИЕ ВСЕХ МЕСТ (READ ALL)
@router.get("/", response_model=List[PlaceResponse])
def read_places(db: Session = Depends(get_db)):
    places = db.query(PlaceModel).all()
    return places

# 3. ЧТЕНИЕ ОДНОГО МЕСТА (READ SINGLE)
@router.get("/{place_id}", response_model=PlaceResponse)
def read_place(place_id: int, db: Session = Depends(get_db)):
    place = db.query(PlaceModel).filter(PlaceModel.id == place_id).first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found"
        )
    return place

# 4. ОБНОВЛЕНИЕ МЕСТА (UPDATE)
@router.put("/{place_id}", response_model=PlaceResponse)
def update_place(
    place_id: int, 
    place_data: PlaceCreate, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user) 
):
    place_query = db.query(PlaceModel).filter(PlaceModel.id == place_id)
    place = place_query.first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found"
        )
    if place.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to update this place (Forbidden)"
        )
    update_data = place_data.model_dump(exclude_unset=True)
    place_query.update(update_data, synchronize_session=False)
    db.commit()
    db.refresh(place)
    return place

# 5. УДАЛЕНИЕ МЕСТА (DELETE)
@router.delete("/{place_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_place(
    place_id: int, 
    db: Session = Depends(get_db),
    current_user: UserResponse = Depends(get_current_user) 
):
    place_query = db.query(PlaceModel).filter(PlaceModel.id == place_id)
    place = place_query.first()
    if not place:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Place with id {place_id} not found"
        )
    if place.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to delete this place (Forbidden)"
        )
    place_query.delete(synchronize_session=False)
    db.commit()
    return