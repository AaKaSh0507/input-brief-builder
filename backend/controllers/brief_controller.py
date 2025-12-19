from sqlalchemy.orm import Session
from typing import List, Optional
from models import Brief, BriefSection, BriefVersion, BriefStatus
from schemas import BriefCreate, BriefUpdate, BriefResponse
from services.cache_service import cache_service
from services.export_service import export_service
import logging
import json

logger = logging.getLogger(__name__)

class BriefController:
    
    def create_brief(self, db: Session, brief_data: BriefCreate) -> Brief:
        """Create a new brief"""
        try:
            brief = Brief(
                title=brief_data.title,
                event_type=brief_data.event_type,
                metadata=brief_data.metadata or {}
            )
            db.add(brief)
            db.commit()
            db.refresh(brief)
            
            # Clear cache
            cache_service.clear_pattern("briefs:*")
            
            logger.info(f"Created brief: {brief.id}")
            return brief
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating brief: {str(e)}")
            raise
    
    def get_brief(self, db: Session, brief_id: str) -> Optional[Brief]:
        """Get a brief by ID with caching"""
        cache_key = f"briefs:{brief_id}"
        
        # Try cache first
        cached = cache_service.get(cache_key)
        if cached:
            # Return from database to get relationships
            return db.query(Brief).filter(Brief.id == brief_id).first()
        
        brief = db.query(Brief).filter(Brief.id == brief_id).first()
        
        if brief:
            # Cache for 1 hour
            cache_service.set(cache_key, {"id": brief.id}, ttl=3600)
        
        return brief
    
    def get_all_briefs(self, db: Session, status: Optional[str] = None, skip: int = 0, limit: int = 100) -> List[Brief]:
        """Get all briefs with optional status filter"""
        query = db.query(Brief)
        
        if status:
            query = query.filter(Brief.status == status)
        
        briefs = query.order_by(Brief.updated_at.desc()).offset(skip).limit(limit).all()
        return briefs
    
    def update_brief(self, db: Session, brief_id: str, brief_data: BriefUpdate) -> Optional[Brief]:
        """Update a brief"""
        try:
            brief = db.query(Brief).filter(Brief.id == brief_id).first()
            
            if not brief:
                return None
            
            # Update fields
            if brief_data.title is not None:
                brief.title = brief_data.title
            if brief_data.event_type is not None:
                brief.event_type = brief_data.event_type
            if brief_data.status is not None:
                brief.status = brief_data.status
            if brief_data.metadata is not None:
                brief.metadata = brief_data.metadata
            
            db.commit()
            db.refresh(brief)
            
            # Clear cache
            cache_service.delete(f"briefs:{brief_id}")
            cache_service.clear_pattern("briefs:list:*")
            
            logger.info(f"Updated brief: {brief_id}")
            return brief
        except Exception as e:
            db.rollback()
            logger.error(f"Error updating brief: {str(e)}")
            raise
    
    def delete_brief(self, db: Session, brief_id: str) -> bool:
        """Delete a brief"""
        try:
            brief = db.query(Brief).filter(Brief.id == brief_id).first()
            
            if not brief:
                return False
            
            db.delete(brief)
            db.commit()
            
            # Clear cache
            cache_service.delete(f"briefs:{brief_id}")
            cache_service.clear_pattern("briefs:list:*")
            
            logger.info(f"Deleted brief: {brief_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting brief: {str(e)}")
            raise
    
    def create_version(self, db: Session, brief_id: str) -> Optional[BriefVersion]:
        """Create a new version snapshot of a brief"""
        try:
            brief = db.query(Brief).filter(Brief.id == brief_id).first()
            
            if not brief:
                return None
            
            # Get all sections
            sections = db.query(BriefSection).filter(BriefSection.brief_id == brief_id).all()
            
            # Create snapshot
            snapshot = {
                "title": brief.title,
                "event_type": brief.event_type,
                "status": brief.status.value,
                "metadata": brief.metadata,
                "sections": [
                    {
                        "section_number": s.section_number,
                        "section_name": s.section_name,
                        "content": s.content,
                        "ai_generated": s.ai_generated
                    }
                    for s in sections
                ]
            }
            
            # Increment version
            brief.version += 1
            
            version = BriefVersion(
                brief_id=brief_id,
                version_number=brief.version,
                content_snapshot=snapshot
            )
            
            db.add(version)
            db.commit()
            db.refresh(version)
            
            logger.info(f"Created version {version.version_number} for brief: {brief_id}")
            return version
        except Exception as e:
            db.rollback()
            logger.error(f"Error creating version: {str(e)}")
            raise
    
    def get_versions(self, db: Session, brief_id: str) -> List[BriefVersion]:
        """Get all versions of a brief"""
        return db.query(BriefVersion).filter(BriefVersion.brief_id == brief_id).order_by(BriefVersion.version_number.desc()).all()
    
    def export_brief(self, db: Session, brief_id: str, format: str = "pdf") -> Optional[str]:
        """Export brief to PDF or Word"""
        try:
            brief = db.query(Brief).filter(Brief.id == brief_id).first()
            
            if not brief:
                return None
            
            # Get all sections
            sections = db.query(BriefSection).filter(BriefSection.brief_id == brief_id).order_by(BriefSection.section_number).all()
            
            # Prepare data
            brief_data = {
                "id": brief.id,
                "title": brief.title,
                "event_type": brief.event_type,
                "status": brief.status.value,
                "version": brief.version,
                "created_at": brief.created_at.strftime("%Y-%m-%d %H:%M"),
                "sections": [
                    {
                        "section_number": s.section_number,
                        "section_name": s.section_name,
                        "content": s.content
                    }
                    for s in sections
                ]
            }
            
            if format == "pdf":
                file_path = export_service.export_to_pdf(brief_data)
            elif format == "word":
                file_path = export_service.export_to_word(brief_data)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return file_path
        except Exception as e:
            logger.error(f"Error exporting brief: {str(e)}")
            raise

# Singleton instance
brief_controller = BriefController()
