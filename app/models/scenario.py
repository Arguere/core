from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Scenario(Base):
    __tablename__ = "scenarios"
    
    id = Column(Integer, primary_key=True, index=True)
    method_id = Column(Integer, ForeignKey("methods.id"))
    title = Column(String, nullable=False)
    description = Column(String)
    
    method = relationship("Method", back_populates="scenarios")
    submissions = relationship("Submission", back_populates="scenario")