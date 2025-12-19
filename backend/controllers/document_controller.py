from sqlalchemy.orm import Session
from typing import List, Optional
from models import Document, Brief
from services.document_service import document_service
from services.ai_service import ai_service
import logging

logger = logging.getLogger(__name__)

class DocumentController:
    
    async def upload_document(self, db: Session, brief_id: str, filename: str, file_content: bytes) -> Document:
        """Upload and process a document"""
        try:
            # Save file
            file_path, mime_type = await document_service.save_file(file_content, filename)
            
            # Determine file type
            file_type = filename.split('.')[-1].lower()
            
            # Create document record
            document = Document(
                brief_id=brief_id,
                filename=filename,
                file_path=file_path,
                file_type=file_type,
                mime_type=mime_type
            )
            
            # Extract text content
            extracted_text = await document_service.extract_text_content(file_path, file_type)
            
            if extracted_text:
                document.extracted_content = extracted_text
            
            db.add(document)
            db.commit()
            db.refresh(document)
            
            logger.info(f"Uploaded document: {document.id}")
            return document
        except Exception as e:
            db.rollback()
            logger.error(f"Error uploading document: {str(e)}")
            raise
    
    async def analyze_document_with_ai(self, db: Session, document_id: str, section_name: str) -> dict:
        """Analyze document with AI for a specific section"""
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            
            if not document:
                raise ValueError(f"Document not found: {document_id}")
            
            # Prepare analysis prompt
            prompt = f"""
            Analyze this document and extract relevant information for the '{section_name}' section 
            of an event input brief. Structure the extracted information as field-value pairs.
            Focus on key details, dates, objectives, and any relevant context.
            """
            
            # Use AI to analyze
            if document.extracted_content:
                # Use extracted text
                result = await ai_service.extract_structured_data(document.extracted_content, section_name)
            else:
                # Use file directly (for images, complex PDFs, etc.)
                result = await ai_service.analyze_document(
                    file_path=document.file_path,
                    mime_type=document.mime_type,
                    analysis_prompt=prompt
                )
            
            return {"document_id": document_id, "analysis": result}
        except Exception as e:
            logger.error(f"Error analyzing document: {str(e)}")
            raise
    
    def get_document(self, db: Session, document_id: str) -> Optional[Document]:
        """Get a document by ID"""
        return db.query(Document).filter(Document.id == document_id).first()
    
    def get_brief_documents(self, db: Session, brief_id: str) -> List[Document]:
        """Get all documents for a brief"""
        return db.query(Document).filter(Document.brief_id == brief_id).order_by(Document.uploaded_at.desc()).all()
    
    def delete_document(self, db: Session, document_id: str) -> bool:
        """Delete a document"""
        try:
            document = db.query(Document).filter(Document.id == document_id).first()
            
            if not document:
                return False
            
            # Delete file from disk
            document_service.delete_file(document.file_path)
            
            # Delete from database
            db.delete(document)
            db.commit()
            
            logger.info(f"Deleted document: {document_id}")
            return True
        except Exception as e:
            db.rollback()
            logger.error(f"Error deleting document: {str(e)}")
            raise

# Singleton instance
document_controller = DocumentController()
