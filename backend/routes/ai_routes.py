from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Dict, Any, List
from database import get_db
from schemas import AIGenerateRequest, AIGenerateResponse
from controllers.ai_controller import ai_controller
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/ai", tags=["AI"])

@router.post("/generate/{section_id}")
async def generate_section_content(
    section_id: str,
    request: AIGenerateRequest,
    db: Session = Depends(get_db)
):
    """Generate AI content for a section"""
    try:
        result = await ai_controller.generate_section_content(
            db,
            section_id,
            request.context,
            request.prompt
        )
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error generating content: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/suggestions")
async def get_field_suggestions(
    field_name: str,
    context: Dict[str, Any]
):
    """Get AI suggestions for a field"""
    try:
        suggestions = await ai_controller.get_field_suggestions(field_name, context)
        return {"field_name": field_name, "suggestions": suggestions}
    except Exception as e:
        logger.error(f"Error getting suggestions: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/auto-populate/{section_id}")
async def auto_populate_section(
    section_id: str,
    brief_id: str,
    db: Session = Depends(get_db)
):
    """Auto-populate section from uploaded documents"""
    try:
        result = await ai_controller.auto_populate_from_documents(db, brief_id, section_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error auto-populating: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
