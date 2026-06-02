from fastapi import UploadFile

from app.config import get_settings


class OCRService:
    async def extract_text(self, file: UploadFile) -> str:
        try:
            from PIL import Image
            import pytesseract
        except ImportError as exc:
            raise RuntimeError("OCR dependencies are not installed.") from exc

        settings = get_settings()
        if settings.tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = settings.tesseract_cmd

        image = Image.open(file.file)
        text = pytesseract.image_to_string(image)
        return text.strip()
