from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    method_id = Column(UUID(as_uuid=True), ForeignKey("methods.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    
    method = relationship("Method", back_populates="scenarios")
    submissions = relationship("Submission", back_populates="scenario")