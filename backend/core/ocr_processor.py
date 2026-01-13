import google.generativeai as genai
import logging
import io
import os
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, tesseract_cmd: str = None):
        # Tesseract cmd is legacy, ignoring it but keeping arg for compatibility
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logger.warning("GOOGLE_API_KEY not found. OCR for scanned docs will fail.")
        else:
            genai.configure(api_key=api_key)
            self.model = genai.GenerativeModel("gemini-2.0-flash-exp")

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Robust text extraction using PyMuPDF (Fitz) + Gemini 2.0 Flash.
        1. Tries to extract digital text directly.
        2. If text is sparse (< 400 chars), renders page as image and uses Gemini 2.0 Flash.
        """
        text = ""
        
        try:
            # Open PDF from bytes
            with fitz.open(stream=file_content, filetype="pdf") as doc:
                for i, page in enumerate(doc):
                    
                    # 1. Try Digital Text Extraction
                    page_text = page.get_text()
                    clean_text = page_text.strip()
                    
                    # Heuristic: If text is empty OR very short (likely artifacts/watermarks in a scan)
                    # and likely has images, we run OCR (Gemini).
                    if len(clean_text) > 400:
                        # We found substantial digital text! Use it.
                        text += f"\n--- Page {i+1} (Digital) ---\n{page_text}"
                    else:
                        # 2. Sparse or no text found? Likely a scan or mixed content.
                        logger.info(f"Page {i+1}: Digital text sparse ({len(clean_text)} chars). Running Gemini 2.0 Flash OCR.")
                        
                        # Zoom factor for better image quality (2.0 is usually enough for Vision models)
                        matrix = fitz.Matrix(2.0, 2.0)
                        pix = page.get_pixmap(matrix=matrix)
                        
                        # Convert to PIL Image
                        img_data = pix.tobytes("png")
                        image = Image.open(io.BytesIO(img_data))
                        
                        try:
                            # Call Gemini 2.0 Flash
                            response = self.model.generate_content([
                                "Transcribe the text from this medical record page exactly. Do not add any commentary.", 
                                image
                            ])
                            ocr_text = response.text
                        except Exception as e:
                            logger.error(f"Gemini OCR failed for page {i+1}: {e}")
                            ocr_text = "[Error extracting text from scan via Gemini]"

                        # Combine both just in case digital text had some valid headers/metadata
                        if clean_text:
                            text += f"\n--- Page {i+1} (Digital Artifacts) ---\n{clean_text}"
                            
                        text += f"\n--- Page {i+1} (Gemini OCR) ---\n{ocr_text}"

        except Exception as e:
            logger.error(f"PDF Processing failed: {e}")
            return f"[Error processing PDF: {e}]"

        # Final check
        if not text.strip():
            logger.warning("Empty text after processing.")
            return "[No text could be extracted from this document]"

        return text

    def extract_text_from_image(self, image_content: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_content))
            response = self.model.generate_content([
                "Transcribe the text from this image exactly. Do not add any commentary.", 
                image
            ])
            return response.text
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise e
