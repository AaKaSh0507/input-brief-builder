from sqlalchemy.orm import Session
from fastapi import HTTPException
from models import BriefSection, Document
import uuid
import json
import logging

logger = logging.getLogger(__name__)


class SectionController:

    # --------------------------------------------------
    # Initialize sections when a brief is created
    # --------------------------------------------------
    def initialize_sections(self, db: Session, brief_id: str):
        """
        Creates the initial 11 sections for a new brief
        """

        initial_sections = [
            (1, "Event Overview"),
            (2, "Objectives & Success Metrics"),
            (3, "Audience & Attendees"),
            (4, "Event Format & Structure"),
            (5, "Program & Agenda"),
            (6, "Speakers & Talent"),
            (7, "Branding & Creative Direction"),
            (8, "Production & Technical Requirements"),
            (9, "Logistics & Operations"),
            (10, "Budget & Commercials"),
            (11, "Timeline & Key Milestones"),
        ]

        sections = []

        for number, name in initial_sections:
            section = BriefSection(
                id=str(uuid.uuid4()),
                brief_id=brief_id,
                section_number=number,
                section_name=name,
                content={},
                ai_generated={}
            )
            db.add(section)
            sections.append(section)

        db.commit()
        logger.info(f"Initialized {len(sections)} sections for brief {brief_id}")
        return sections

    # --------------------------------------------------
    # Get all sections for a brief
    # --------------------------------------------------
    def get_brief_sections(self, db: Session, brief_id: str):
        return (
            db.query(BriefSection)
            .filter(BriefSection.brief_id == brief_id)
            .order_by(BriefSection.section_number)
            .all()
        )

    # --------------------------------------------------
    # Update section content (manual edit)
    # --------------------------------------------------
    def update_section(self, db: Session, section_id: str, data: dict):
        section = (
            db.query(BriefSection)
            .filter(BriefSection.id == section_id)
            .first()
        )

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        content = data.get("content", {})
        normalized: dict[str, str] = {}

        for key, value in content.items():
            if value is None:
                normalized[key] = ""
            elif isinstance(value, (dict, list)):
                normalized[key] = json.dumps(value, ensure_ascii=False)
            else:
                normalized[key] = str(value)

        section.content = normalized

        db.commit()
        db.refresh(section)
        logger.info(f"Updated section {section_id}")

        return section

    # --------------------------------------------------
    # Auto-populate section from uploaded documents
    # --------------------------------------------------
    def auto_populate_from_document(
        self,
        db: Session,
        section_id: str,
        brief_id: str
    ):
        """
        Uses extracted document text to populate section content.
        For now, this aggregates document text into a single field.
        """

        section = (
            db.query(BriefSection)
            .filter(BriefSection.id == section_id)
            .first()
        )

        if not section:
            raise HTTPException(status_code=404, detail="Section not found")

        documents = (
            db.query(Document)
            .filter(Document.brief_id == brief_id)
            .all()
        )

        if not documents:
            raise HTTPException(
                status_code=400,
                detail="No documents uploaded for this brief"
            )

        combined_text = "\n\n".join(
            doc.extracted_content or ""
            for doc in documents
            if doc.extracted_content
        ).strip()

        if not combined_text:
            raise HTTPException(
                status_code=400,
                detail="Uploaded documents contain no extractable text"
            )

        section.content = {
            "auto_populated_notes": combined_text
        }

        db.commit()
        db.refresh(section)

        logger.info(f"Auto-populated section {section_id} from documents")
        return section


section_controller = SectionController()
