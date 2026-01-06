import os
import logging
from pathlib import Path
from typing import Optional
from fastapi import UploadFile

logger = logging.getLogger(__name__)


class DocumentService:
    def __init__(self):
        BASE_DIR = Path(__file__).resolve().parent.parent
        self.upload_dir = BASE_DIR / "uploads"
        self.upload_dir.mkdir(parents=True, exist_ok=True)

    def save_file(self, file: UploadFile) -> Path:
        file_path = self.upload_dir / file.filename

        with open(file_path, "wb") as f:
            f.write(file.file.read())

        logger.info("File saved to %s", file_path)
        return file_path

    def delete_file(self, filename: str) -> bool:
        file_path = self.upload_dir / filename

        if file_path.exists():
            file_path.unlink()
            return True

        return False


document_service = DocumentService()
