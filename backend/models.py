from sqlalchemy import Column, String, DateTime, Text, JSON, ForeignKey, Integer, Enum as SQLEnum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import enum
from database import Base

class BriefStatus(enum.Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Brief(Base):
    __tablename__ = "briefs"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    event_type = Column(String)
    status = Column(SQLEnum(BriefStatus), default=BriefStatus.DRAFT)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    version = Column(Integer, default=1)
    brief_metadata = Column(JSON, default=dict)
    
    sections = relationship("BriefSection", back_populates="brief", cascade="all, delete-orphan")
    documents = relationship("Document", back_populates="brief", cascade="all, delete-orphan")
    versions = relationship("BriefVersion", back_populates="brief", cascade="all, delete-orphan")

class BriefSection(Base):
    __tablename__ = "brief_sections"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brief_id = Column(String, ForeignKey("briefs.id"), nullable=False)
    section_number = Column(Integer, nullable=False)
    section_name = Column(String, nullable=False)
    content = Column(JSON, default=dict)  # Stores field-value pairs
    ai_generated = Column(JSON, default=dict)  # Stores AI suggestions
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    brief = relationship("Brief", back_populates="sections")

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brief_id = Column(String, ForeignKey("briefs.id"), nullable=False)
    filename = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String, nullable=False)
    mime_type = Column(String)
    extracted_content = Column(JSON, default=dict)

    uploaded_at = Column(DateTime, default=datetime.utcnow)
    
    brief = relationship("Brief", back_populates="documents")

class BriefVersion(Base):
    __tablename__ = "brief_versions"
    
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    brief_id = Column(String, ForeignKey("briefs.id"), nullable=False)
    version_number = Column(Integer, nullable=False)
    content_snapshot = Column(JSON, nullable=False)  # Full brief data
    created_at = Column(DateTime, default=datetime.utcnow)
    
    brief = relationship("Brief", back_populates="versions")
