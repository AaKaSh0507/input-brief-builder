from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from schemas import DocumentResponse
from controllers.document_controller import document_controller
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])

@router.post("/upload", response_model=DocumentResponse, status_code=status.HTTP_201_CREATED)
async def upload_document(brief_id: str, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload a document to a brief"""
    try:
        # Read file content
        content = await file.read()
        
        # Upload and process document
        document = await document_controller.upload_document(db, brief_id, file.filename, content)
        
        return document
    except Exception as e:
        logger.error(f"Error uploading document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/{document_id}/analyze")
async def analyze_document(document_id: str, section_name: str, db: Session = Depends(get_db)):
    """Analyze a document with AI for a specific section"""
    try:
        result = await document_controller.analyze_document_with_ai(db, document_id, section_name)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error analyzing document: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/brief/{brief_id}", response_model=List[DocumentResponse])
def get_brief_documents(brief_id: str, db: Session = Depends(get_db)):
    """Get all documents for a brief"""
    try:
        documents = document_controller.get_brief_documents(db, brief_id)
        return documents
    except Exception as e:
        logger.error(f"Error getting documents: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    """Get a specific document"""
    document = document_controller.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document

@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    """Delete a document"""
    success = document_controller.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return None
