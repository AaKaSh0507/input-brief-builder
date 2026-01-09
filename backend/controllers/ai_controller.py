from sqlalchemy.orm import Session
from controllers.section_controller import section_controller
import logging

logger = logging.getLogger(__name__)


class AIController:

    def auto_populate(
        self,
        db: Session,
        section_id: str,
        brief_id: str
    ):
        """
        Auto-populate a section using uploaded documents.
        """

        try:
            return section_controller.auto_populate_from_document(
                db=db,
                section_id=section_id,
                brief_id=brief_id
            )

        except Exception as e:
            logger.exception("AI auto-populate failed")
            raise e


ai_controller = AIController()
