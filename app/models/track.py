from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=True) 
    title = Column(String, nullable=False)

    user = relationship("User", back_populates="tracks")
    methods = relationship("Method", back_populates="track")