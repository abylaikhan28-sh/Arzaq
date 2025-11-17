# arzaq/app/models/place.py

from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class Place(Base):
    __tablename__ = "places"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    latitude = Column(Float)
    longitude = Column(Float)
    
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User")
    
    comments = relationship("Comment", back_populates="place")