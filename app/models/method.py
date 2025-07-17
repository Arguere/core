from sqlalchemy import Column, UUID, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
import uuid
from app.core.database import Base

class Method(Base):
    __tablename__ = "methods"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    track_id = Column(UUID(as_uuid=True), ForeignKey("tracks.id", ondelete="CASCADE"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    tutorial = Column(String)
    
    track = relationship("Track", back_populates="methods")
    scenarios = relationship("Scenario", back_populates="method")