from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Section(Base): 
    __tablename__ = "sections"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    type = Column(String, nullable=False)  # 'method-breakdown', 'examples', etc.
    method_id = Column(Integer, ForeignKey("methods.id"), nullable=False)
    
    method = relationship("Method", back_populates="sections")