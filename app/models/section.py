from sqlalchemy import Column, Integer, String, UUID, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
import uuid

class Section(Base): 
    __tablename__ = "sections"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'method-breakdown', 'examples', etc.
    method_id = Column(UUID(as_uuid=True), ForeignKey("methods.id"), nullable=False)
    
    method = relationship("Method", back_populates="sections")