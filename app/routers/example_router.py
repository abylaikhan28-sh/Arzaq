from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.example import ExampleModel
from app.schemas.example import ExampleSchema
from app.schemas import UserCreate, UserOut, PlaceCreate, PlaceOut


router = APIRouter(prefix="/examples", tags=["Examples"])

@router.post("/", response_model=ExampleSchema)
def create_example(example: ExampleSchema, db: Session = Depends(get_db)):
    db_example = ExampleModel(name=example.name)
    db.add(db_example)
    db.commit()
    db.refresh(db_example)
    return db_example

@router.get("/")
def read_examples(db: Session = Depends(get_db)):
    return db.query(ExampleModel).all()
