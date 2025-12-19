from sqlalchemy.orm import Session
from typing import Dict, Any, List
from models import BriefSection, Document
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class AIController:
    
    async def generate_section_content(self, db: Session, section_id: str, context: Dict[str, Any], custom_prompt: str = None) -> Dict[str, Any]:
        """Generate AI content for a specific section"""
        try:
            section = db.query(BriefSection).filter(BriefSection.id == section_id).first()
            
            if not section:
                raise ValueError(f"Section not found: {section_id}")
            
            # Get existing content as context
            full_context = {
                "section_name": section.section_name,
                "existing_content": section.content,
                **context
            }
            
            # Generate content
            result = await ai_service.generate_section_content(
                section_name=section.section_name,
                context=full_context,
                prompt=custom_prompt
            )
            
            # Update AI generated field
            section.ai_generated = result
            db.commit()
            
            logger.info(f"Generated AI content for section: {section_id}")
            return result
        except Exception as e:
            logger.error(f"Error generating section content: {str(e)}")
            raise
    
    async def get_field_suggestions(self, field_name: str, context: Dict[str, Any]) -> List[str]:
        """Get AI suggestions for a field"""
        try:
            suggestions = await ai_service.get_field_suggestions(field_name, context)
            return suggestions
        except Exception as e:
            logger.error(f"Error getting field suggestions: {str(e)}")
            return []
    
    async def auto_populate_from_documents(self, db: Session, brief_id: str, section_id: str) -> Dict[str, Any]:
        """Auto-populate section from uploaded documents"""
        try:
            section = db.query(BriefSection).filter(BriefSection.id == section_id).first()
            
            if not section:
                raise ValueError(f"Section not found: {section_id}")
            
            # Get all documents for this brief
            documents = db.query(Document).filter(Document.brief_id == brief_id).all()
            
            if not documents:
                return {"message": "No documents available"}
            
            # Combine extracted content from all documents
            all_content = "\n\n".join([
                f"Document: {doc.filename}\n{doc.extracted_content or '[No text extracted]'}"
                for doc in documents
            ])
            
            # Use AI to extract relevant info for this section
            result = await ai_service.extract_structured_data(
                document_content=all_content,
                section_name=section.section_name
            )
            
            # Update section with AI generated content
            section.ai_generated = result
            db.commit()
            
            logger.info(f"Auto-populated section {section_id} from documents")
            return result
        except Exception as e:
            logger.error(f"Error auto-populating from documents: {str(e)}")
            raise

# Singleton instance
ai_controller = AIController()
