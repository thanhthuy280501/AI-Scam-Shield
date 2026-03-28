"""
ocr_reader.py
Extract text from images and screenshots using Tesseract OCR or OpenAI Vision.

This is key for the AI Scam Shield because users may receive scam content
as physical letters (photographed) or screenshots from social media / messaging apps.

Install Tesseract:
  macOS:    brew install tesseract
  Ubuntu:   sudo apt install tesseract-ocr
  Windows:  https://github.com/UB-Mannheim/tesseract/wiki

Install Python binding:
  pip install pytesseract Pillow
"""

import os
from pathlib import Path

# Tesseract OCR (free, offline)
try:
    import pytesseract
    from PIL import Image
    _TESSERACT_AVAILABLE = True
except ImportError:
    _TESSERACT_AVAILABLE = False

# OpenAI Vision (paid, much more accurate — especially for messy photos)
import openai
openai.api_key = os.getenv("OPENAI_API_KEY")


class OCRReader:
    def __init__(self, prefer_vision_api: bool = False):
        """
        prefer_vision_api: If True and OPENAI_API_KEY is set, use GPT-4o Vision.
                           Otherwise falls back to Tesseract (free, offline).
        """
        self.prefer_vision_api = prefer_vision_api and bool(os.getenv("OPENAI_API_KEY"))

    def extract_text(self, image_path: str) -> str:
        """
        Extract text from an image file.
        Returns the extracted text string, or empty string on failure.
        """
        path = Path(image_path)
        if not path.exists():
            print(f"[OCR] File not found: {image_path}")
            return ""

        if self.prefer_vision_api:
            return self._extract_with_vision(path)
        elif _TESSERACT_AVAILABLE:
            return self._extract_with_tesseract(path)
        else:
            print("[OCR] No OCR engine available. Install pytesseract or set OPENAI_API_KEY.")
            return ""

    def _extract_with_tesseract(self, path: Path) -> str:
        """Use Tesseract for offline, free OCR."""
        try:
            image = Image.open(path)
            # lang="eng+vie+spa+chi_sim" — add languages as needed
            text = pytesseract.image_to_string(image, lang="eng")
            return text.strip()
        except Exception as e:
            print(f"[OCR] Tesseract error: {e}")
            return ""

    def _extract_with_vision(self, path: Path) -> str:
        """
        Use OpenAI GPT-4o Vision to extract text.
        More accurate for real-world photos, screenshots, and handwriting.
        """
        import base64

        try:
            with open(path, "rb") as f:
                image_data = base64.b64encode(f.read()).decode("utf-8")

            ext = path.suffix.lower().lstrip(".")
            media_type = "image/jpeg" if ext in ("jpg", "jpeg") else f"image/{ext}"

            response = openai.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image_url",
                                "image_url": {
                                    "url": f"data:{media_type};base64,{image_data}"
                                },
                            },
                            {
                                "type": "text",
                                "text": (
                                    "Extract ALL visible text from this image exactly as it appears. "
                                    "Include every word, number, and punctuation mark. "
                                    "Do not summarize or interpret — just transcribe."
                                ),
                            },
                        ],
                    }
                ],
                max_tokens=1000,
            )
            return response.choices[0].message.content.strip()

        except Exception as e:
            print(f"[OCR] Vision API error: {e}")
            return ""
