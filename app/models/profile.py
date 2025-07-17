from sqlalchemy import Column, String, DateTime, UUID, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB
from app.core.database import Base
from sqlalchemy.orm import relationship
import uuid

class Profile(Base):
    __tablename__ = "profiles"
    id = Column(UUID(as_uuid=True), primary_key=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String)
    onboarding_options = Column(JSONB, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now()) # TODO: i have a feeling that this will not work with supabase auth because idk if it updates automatically, need to test it
    
    track = relationship("Track", back_populates="profile")
    submissions = relationship("Submission", back_populates="profile")
    