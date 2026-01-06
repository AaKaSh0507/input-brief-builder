import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


class AIService:
    """
    Local development stub for AI features.
    Replace with Emergent integration in production.
    """

    def generate_section_content(self, section_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.warning("AIService stub called for section: %s", section_name)
        return {
            "generated": True,
            "content": f"[AI stub] Generated content for section '{section_name}'."
        }

    def get_field_suggestions(self, field_name: str, context: Dict[str, Any]) -> Dict[str, Any]:
        logger.warning("AIService stub called for field: %s", field_name)
        return {
            "suggestions": [
                f"[AI stub] Suggestion 1 for {field_name}",
                f"[AI stub] Suggestion 2 for {field_name}"
            ]
        }

    def auto_populate_from_documents(self, section_name: str, documents: list) -> Dict[str, Any]:
        logger.warning("AIService stub auto-populate called for section: %s", section_name)
        return {
            "auto_populated": True,
            "content": f"[AI stub] Auto-populated content for '{section_name}'."
        }


ai_service = AIService()
