from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Method(Base):
    __tablename__ = "methods"
    
    id = Column(Integer, primary_key=True, index=True)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    tutorial = Column(String)
    
    track = relationship("Track", back_populates="methods")
    scenarios = relationship("Scenario", back_populates="method")