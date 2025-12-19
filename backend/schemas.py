from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from datetime import datetime
from enum import Enum

class BriefStatus(str, Enum):
    DRAFT = "draft"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class BriefCreate(BaseModel):
    title: str
    event_type: Optional[str] = None
    brief_metadata: Optional[Dict[str, Any]] = {}

class BriefUpdate(BaseModel):
    title: Optional[str] = None
    event_type: Optional[str] = None
    status: Optional[BriefStatus] = None
    metadata: Optional[Dict[str, Any]] = None

class BriefResponse(BaseModel):
    id: str
    title: str
    event_type: Optional[str]
    status: str
    created_at: datetime
    updated_at: datetime
    version: int
    metadata: Dict[str, Any]
    
    class Config:
        from_attributes = True

class SectionCreate(BaseModel):
    section_number: int
    section_name: str
    content: Dict[str, Any] = {}

class SectionUpdate(BaseModel):
    content: Optional[Dict[str, Any]] = None
    ai_generated: Optional[Dict[str, Any]] = None

class SectionResponse(BaseModel):
    id: str
    brief_id: str
    section_number: int
    section_name: str
    content: Dict[str, Any]
    ai_generated: Dict[str, Any]
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

class DocumentResponse(BaseModel):
    id: str
    brief_id: str
    filename: str
    file_type: str
    uploaded_at: datetime
    extracted_content: Optional[str]
    
    class Config:
        from_attributes = True

class AIGenerateRequest(BaseModel):
    section_name: str
    context: Optional[Dict[str, Any]] = {}
    prompt: Optional[str] = None

class AIGenerateResponse(BaseModel):
    section_name: str
    generated_content: Dict[str, Any]
