from sqlalchemy import Column, Integer, String, ForeignKey, UUID
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Track(Base):
    __tablename__ = "tracks"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("profiles.id", ondelete="CASCADE"), nullable=True) 
    title = Column(String, nullable=False)

    profile = relationship("Profile", back_populates="track")
    methods = relationship("Method", back_populates="track")