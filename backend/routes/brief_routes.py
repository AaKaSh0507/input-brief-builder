from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from schemas import BriefCreate, BriefUpdate, BriefResponse
from controllers.brief_controller import brief_controller
from controllers.section_controller import section_controller
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/briefs", tags=["Briefs"])

@router.post("/", response_model=BriefResponse, status_code=status.HTTP_201_CREATED)
def create_brief(brief: BriefCreate, db: Session = Depends(get_db)):
    """Create a new brief and initialize sections"""
    try:
        # Create brief
        new_brief = brief_controller.create_brief(db, brief)
        
        # Initialize all sections
        section_controller.initialize_sections(db, new_brief.id)
        
        return new_brief
    except Exception as e:
        logger.error(f"Error creating brief: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=List[BriefResponse])
def get_briefs(status: Optional[str] = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """Get all briefs with optional status filter"""
    try:
        briefs = brief_controller.get_all_briefs(db, status, skip, limit)
        return briefs
    except Exception as e:
        logger.error(f"Error getting briefs: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{brief_id}", response_model=BriefResponse)
def get_brief(brief_id: str, db: Session = Depends(get_db)):
    """Get a specific brief"""
    brief = brief_controller.get_brief(db, brief_id)
    if not brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return brief

@router.put("/{brief_id}", response_model=BriefResponse)
def update_brief(brief_id: str, brief: BriefUpdate, db: Session = Depends(get_db)):
    """Update a brief"""
    updated_brief = brief_controller.update_brief(db, brief_id, brief)
    if not updated_brief:
        raise HTTPException(status_code=404, detail="Brief not found")
    return updated_brief

@router.delete("/{brief_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brief(brief_id: str, db: Session = Depends(get_db)):
    """Delete a brief"""
    success = brief_controller.delete_brief(db, brief_id)
    if not success:
        raise HTTPException(status_code=404, detail="Brief not found")
    return None

@router.post("/{brief_id}/versions")
def create_version(brief_id: str, db: Session = Depends(get_db)):
    """Create a version snapshot of a brief"""
    version = brief_controller.create_version(db, brief_id)
    if not version:
        raise HTTPException(status_code=404, detail="Brief not found")
    return {"version_number": version.version_number, "created_at": version.created_at}

@router.get("/{brief_id}/versions")
def get_versions(brief_id: str, db: Session = Depends(get_db)):
    """Get all versions of a brief"""
    versions = brief_controller.get_versions(db, brief_id)
    return [{"version_number": v.version_number, "created_at": v.created_at, "id": v.id} for v in versions]

@router.get("/{brief_id}/export")
def export_brief(brief_id: str, format: str = "pdf", db: Session = Depends(get_db)):
    """Export brief to PDF or Word"""
    try:
        file_path = brief_controller.export_brief(db, brief_id, format)
        if not file_path:
            raise HTTPException(status_code=404, detail="Brief not found")
        
        return FileResponse(
            path=file_path,
            filename=file_path.split("/")[-1],
            media_type="application/octet-stream"
        )
    except Exception as e:
        logger.error(f"Error exporting brief: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
