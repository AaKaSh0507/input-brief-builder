from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from database import get_db
from controllers.ai_controller import ai_controller

router = APIRouter(prefix="/ai", tags=["AI"])


@router.post("/auto-populate/{section_id}")
def auto_populate_section(
    section_id: str,
    brief_id: str,
    db: Session = Depends(get_db),
):
    return ai_controller.auto_populate(db, section_id, brief_id)
