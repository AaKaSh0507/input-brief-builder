from pathlib import Path
from typing import Dict, Tuple
import mimetypes
import pandas as pd
import uuid
import os

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)

class DocumentService:

    async def save_file(self, content: bytes, filename: str) -> Tuple[str, str]:
        ext = filename.rsplit(".", 1)[-1].lower()
        safe_name = f"{uuid.uuid4()}.{ext}"
        path = UPLOAD_DIR / safe_name

        with open(path, "wb") as f:
            f.write(content)

        mime_type, _ = mimetypes.guess_type(filename)
        return str(path), mime_type or "application/octet-stream"

    async def extract_text_content(self, file_path: str, file_type: str) -> Dict[str, str] | None:
        if file_type not in {"xlsx", "xls"}:
            return None

        df = pd.read_excel(file_path)

        if df.empty:
            return None

        row = df.iloc[0]

        # Explicit mapping from Excel → section fields
        FIELD_MAP = {
            "Executive Sponsor": "Executive Sponsor",
            "Event SPOC": "Event SPOC",
            "Content Lead": "Content Lead",
            "Demand Strategist": "Demand Strategist",
            "Field Marketer": "Field Marketer",
        }

        extracted: Dict[str, str] = {}

        for excel_col, field_name in FIELD_MAP.items():
            if excel_col in row and pd.notna(row[excel_col]):
                extracted[field_name] = str(row[excel_col]).strip()

        return extracted

    def delete_file(self, path: str) -> None:
        if os.path.exists(path):
            os.remove(path)

document_service = DocumentService()
