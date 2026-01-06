import os
import logging
from typing import Dict, Any
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch

logger = logging.getLogger(__name__)


class ExportService:
    def __init__(self):
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.export_dir = os.path.join(BASE_DIR, "exports")
        os.makedirs(self.export_dir, exist_ok=True)

    def export_to_pdf(self, brief_data: Dict[str, Any], filename: str | None = None) -> str:
        if not filename:
            filename = f"brief_{brief_data.get('id', 'export')}.pdf"

        file_path = os.path.join(self.export_dir, filename)

        c = canvas.Canvas(file_path, pagesize=A4)
        width, height = A4
        y_position = height - inch

        c.setFont("Helvetica-Bold", 16)
        c.drawString(inch, y_position, brief_data.get("title", "Event Brief"))
        y_position -= inch

        c.setFont("Helvetica", 11)

        for section in brief_data.get("sections", []):
            if y_position < inch:
                c.showPage()
                y_position = height - inch
                c.setFont("Helvetica", 11)

            c.setFont("Helvetica-Bold", 13)
            c.drawString(inch, y_position, section.get("section_name", ""))
            y_position -= 0.4 * inch

            c.setFont("Helvetica", 11)
            content = section.get("content", {})

            if isinstance(content, dict):
                for key, value in content.items():
                    c.drawString(inch, y_position, f"{key}: {value}")
                    y_position -= 0.3 * inch
            else:
                c.drawString(inch, y_position, str(content))
                y_position -= 0.3 * inch

            y_position -= 0.2 * inch

        c.save()
        logger.info("PDF exported to %s", file_path)
        return file_path


export_service = ExportService()
