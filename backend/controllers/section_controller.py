from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from models import BriefSection, Brief
from schemas import SectionCreate, SectionUpdate
from services.cache_service import cache_service
from brief_schema import BRIEF_SCHEMA
import logging

logger = logging.getLogger(__name__)

class SectionController:
    
    def initialize_sections(self, db: Session, brief_id: str) -> List[BriefSection]:
        """Initialize all default sections for a brief"""
        try:
            sections = []
            
            for section_def in BRIEF_SCHEMA["sections"]:
                # Initialize content structure based on schema
                content = {}
                for field_group in section_def["inputFields"]:
                    for field in field_group["fields"]:
                        field_name = field["inputName"]
                        if field["dataType"] == "Object":
                            # For Object types (Name/Email pairs)
                            content[field_name] = {"Name": "", "Email": ""}
                        elif field["dataType"] == "Array":
                            content[field_name] = []
                        else:
                            content[field_name] = ""
                
                section = BriefSection(
                    brief_id=brief_id,
                    section_number=section_def["sectionNumber"],
                    section_name=section_def["sectionName"],
                    content=content,
                    ai_generated={}
                )
                db.add(section)
                sections.append(section)
            
            db.commit()
            
            for section in sections:
                db.refresh(section)
            
            logger.info(f"Initialized {len(sections)} sections for brief: {brief_id}")
            return sections
        except Exception as e:
            db.rollback()
            logger.error(f"Error initializing sections: {str(e)}")
            raise
    
    def create_section(self, db: Session, brief_id: str, section_data: SectionCreate) -> BriefSection:
        """Create a new section"""
        try:
            section = BriefSection(
                brief_id=brief_id,
                section_number=section_data.section_number,
                section_name=section_data.section_name,
                content=section_data.content or {},
                ai_generated={}
            )
            
            db.add(section)
            db.commit()
            db.refresh(section)
            
            # Clear cache
            cache_service.delete(f"briefs:{brief_id}")
            
            logger.info(f"Created section: {section.id}")
            return section
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating section: {str(e)}")
            raise
    
    def get_section(self, db: Session, section_id: str) -> Optional[BriefSection]:
        """Get a section by ID"""
        return db.query(BriefSection).filter(BriefSection.id == section_id).first()
    
    def get_brief_sections(self, db: Session, brief_id: str) -> List[BriefSection]:
        """Get all sections for a brief"""
        return db.query(BriefSection).filter(BriefSection.brief_id == brief_id).order_by(BriefSection.section_number).all()
    
    def update_section(self, db: Session, section_id: str, section_data: SectionUpdate) -> Optional[BriefSection]:
        """Update a section"""
        try:
            section = db.query(BriefSection).filter(BriefSection.id == section_id).first()
            
            if not section:
                return None
            
            if section_data.content is not None:
                section.content = section_data.content
            
            if section_data.ai_generated is not None:
                section.ai_generated = section_data.ai_generated
            
            db.commit()
            db.refresh(section)
            
            # Clear cache
            cache_service.delete(f"briefs:{section.brief_id}")
            
            logger.info(f"Updated section: {section_id}")
            return section
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating section: {str(e)}")
            raise
    
    def delete_section(self, db: Session, section_id: str) -> bool:
        """Delete a section"""
        try:
            section = db.query(BriefSection).filter(BriefSection.id == section_id).first()
            
            if not section:
                return False
            
            brief_id = section.brief_id
            db.delete(section)
            db.commit()
            
            # Clear cache
            cache_service.delete(f"briefs:{brief_id}")
            
            logger.info(f"Deleted section: {section_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting section: {str(e)}")
            raise

# Singleton instance
section_controller = SectionController()
