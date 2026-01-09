from sqlalchemy.orm import Session
from models import Document, Brief
from services.document_service import document_service
import logging

logger = logging.getLogger(__name__)


class DocumentController:

    async def upload_document(
        self,
        db: Session,
        brief_id: str,
        filename: str,
        file_content: bytes,
    ) -> Document:

        brief = db.query(Brief).filter(Brief.id == brief_id).first()
        if not brief:
            raise ValueError("Brief not found")

        file_path, mime_type = await document_service.save_file(
            file_content, filename
        )

        file_type = filename.rsplit(".", 1)[-1].lower()

        extracted = await document_service.extract_text_content(
            file_path, file_type
        )

        document = Document(
            brief_id=brief_id,
            filename=filename,
            file_path=file_path,
            file_type=file_type,
            mime_type=mime_type,
            extracted_content=extracted,
        )

        db.add(document)
        db.commit()
        db.refresh(document)

        logger.info(f"Uploaded document {document.id}")
        return document

    def get_brief_documents(self, db: Session, brief_id: str):
        return (
            db.query(Document)
            .filter(Document.brief_id == brief_id)
            .order_by(Document.uploaded_at.desc())
            .all()
        )

    def get_document(self, db: Session, document_id: str):
        return (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

    def delete_document(self, db: Session, document_id: str) -> bool:
        document = (
            db.query(Document)
            .filter(Document.id == document_id)
            .first()
        )

        if not document:
            return False

        document_service.delete_file(document.file_path)
        db.delete(document)
        db.commit()

        logger.info(f"Deleted document {document_id}")
        return True


document_controller = DocumentController()
