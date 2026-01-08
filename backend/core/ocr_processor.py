import pytesseract
import logging
import io
import os
from PIL import Image
import fitz  # PyMuPDF

logger = logging.getLogger(__name__)

class OCRProcessor:
    def __init__(self, tesseract_cmd: str = None):
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
        else:
            # Check standard Windows location
            default_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
            if os.path.exists(default_path):
                pytesseract.pytesseract.tesseract_cmd = default_path

    def extract_text_from_pdf(self, file_content: bytes) -> str:
        """
        Robust text extraction using PyMuPDF (Fitz).
        1. Tries to extract digital text directly.
        2. If text is sparse (< 50 chars) or empty, renders page as image and runs Tesseract OCR.
        3. No Poppler dependency required.
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
                    # and likely has images, we run OCR.
                    # Increased threshold to 400 chars (approx 1 paragraph) to be safer.
                    if len(clean_text) > 400:
                        # We found substantial digital text! Use it.
                        text += f"\n--- Page {i+1} (Digital) ---\n{page_text}"
                    else:
                        # 2. Sparse or no text found? Likely a scan or mixed content.
                        logger.info(f"Page {i+1}: Digital text sparse ({len(clean_text)} chars). Running OCR.")
                        
                        # Zoom factor for better OCR quality (3.0 = 300% DPI approx ~216-300 DPI)
                        # Higher DPI is crucial for medical records which often have small fonts or poor scan quality.
                        matrix = fitz.Matrix(3.0, 3.0)
                        pix = page.get_pixmap(matrix=matrix)
                        
                        # Convert to PIL Image
                        img_data = pix.tobytes("png")
                        image = Image.open(io.BytesIO(img_data))
                        
                        ocr_text = pytesseract.image_to_string(image)
                        
                        # Combine both just in case digital text had some valid headers/metadata
                        if clean_text:
                            text += f"\n--- Page {i+1} (Digital Artifacts) ---\n{clean_text}"
                            
                        text += f"\n--- Page {i+1} (OCR) ---\n{ocr_text}"

        except Exception as e:
            logger.error(f"PDF Processing failed: {e}")
            # Do not raise, return what we have or error message so analysis can continue
            return f"[Error processing PDF: {e}]"

        # Final check
        if not text.strip():
            logger.warning("Empty text after processing.")
            return "[No text could be extracted from this document]"

        return text

    def extract_text_from_image(self, image_content: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(image_content))
            return pytesseract.image_to_string(image)
        except Exception as e:
            logger.error(f"Image OCR failed: {e}")
            raise e
