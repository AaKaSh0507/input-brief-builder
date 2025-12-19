from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import SectionCreate, SectionUpdate, SectionResponse
from controllers.section_controller import section_controller
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/sections", tags=["Sections"])

@router.post("/", response_model=SectionResponse, status_code=status.HTTP_201_CREATED)
def create_section(section: SectionCreate, brief_id: str, db: Session = Depends(get_db)):
    """Create a new section"""
    try:
        new_section = section_controller.create_section(db, brief_id, section)
        return new_section
    except Exception as e:
        logger.error(f"Error creating section: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brief/{brief_id}", response_model=List[SectionResponse])
def get_brief_sections(brief_id: str, db: Session = Depends(get_db)):
    """Get all sections for a brief"""
    try:
        sections = section_controller.get_brief_sections(db, brief_id)
        return sections
    except Exception as e:
        logger.error(f"Error getting sections: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{section_id}", response_model=SectionResponse)
def get_section(section_id: str, db: Session = Depends(get_db)):
    """Get a specific section"""
    section = section_controller.get_section(db, section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Section not found")
    return section

@router.put("/{section_id}", response_model=SectionResponse)
def update_section(section_id: str, section: SectionUpdate, db: Session = Depends(get_db)):
    """Update a section"""
    updated_section = section_controller.update_section(db, section_id, section)
    if not updated_section:
        raise HTTPException(status_code=404, detail="Section not found")
    return updated_section

@router.delete("/{section_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_section(section_id: str, db: Session = Depends(get_db)):
    """Delete a section"""
    success = section_controller.delete_section(db, section_id)
    if not success:
        raise HTTPException(status_code=404, detail="Section not found")
    return None
