from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session
from typing import List
import logging

from database import get_db
from schemas import DocumentResponse
from controllers.document_controller import document_controller

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/documents", tags=["Documents"])


@router.post(
    "/upload",
    response_model=DocumentResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_document(
    brief_id: str,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
):
    """
    Upload a document to a brief
    """

    if not file.filename:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Filename is required",
        )

    try:
        content = await file.read()

        document = await document_controller.upload_document(
            db=db,
            brief_id=brief_id,
            filename=file.filename,
            file_content=content,
        )

        return document

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.exception("Error uploading document")
        raise HTTPException(status_code=500, detail="Failed to upload document")


@router.post("/{document_id}/analyze")
async def analyze_document(
    document_id: str,
    section_name: str,
    db: Session = Depends(get_db),
):
    """
    Analyze a document with AI for a specific section
    """
    try:
        return await document_controller.analyze_document_with_ai(
            db=db,
            document_id=document_id,
            section_name=section_name,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        logger.exception("Error analyzing document")
        raise HTTPException(status_code=500, detail="Failed to analyze document")


@router.get("/brief/{brief_id}", response_model=List[DocumentResponse])
def get_brief_documents(brief_id: str, db: Session = Depends(get_db)):
    try:
        return document_controller.get_brief_documents(db, brief_id)
    except Exception:
        logger.exception("Error fetching documents")
        raise HTTPException(status_code=500, detail="Failed to fetch documents")


@router.get("/{document_id}", response_model=DocumentResponse)
def get_document(document_id: str, db: Session = Depends(get_db)):
    document = document_controller.get_document(db, document_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return document


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, db: Session = Depends(get_db)):
    success = document_controller.delete_document(db, document_id)
    if not success:
        raise HTTPException(status_code=404, detail="Document not found")
    return None
