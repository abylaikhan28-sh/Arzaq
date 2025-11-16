from sqlalchemy import Column, Integer, String
from app.database import Base

class ExampleModel(Base):
    __tablename__ = "examples"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
