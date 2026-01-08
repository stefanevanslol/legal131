
import pytesseract
from PIL import Image, ImageDraw, ImageFont
import os
import sys

# Configure Tesseract path explicitly as the app does
tesseract_path = r"C:\Program Files\Tesseract-OCR\tesseract.exe"
if os.path.exists(tesseract_path):
    pytesseract.pytesseract.tesseract_cmd = tesseract_path
    print(f"Tesseract found at: {tesseract_path}")
else:
    print("Tesseract NOT found at default location.")

def create_test_image():
    # Create white image
    img = Image.new('RGB', (400, 100), color='white')
    d = ImageDraw.Draw(img)
    
    # Add text
    # We don't need a specific font, default is fine usually, but let's try to be simple
    d.text((10,10), "TEST OCR SUCCESS 123", fill=(0,0,0))
    
    return img

def test_ocr():
    try:
        print("Creating test image...")
        img = create_test_image()
        
        print("Running OCR...")
        text = pytesseract.image_to_string(img)
        
        print("-" * 20)
        print(f"OCR Result: '{text.strip()}'")
        print("-" * 20)
        
        if "TEST OCR SUCCESS 123" in text:
            print("✅ VERIFICATION PASSED")
        else:
            print("❌ VERIFICATION FAILED: Text not matching")
            
    except Exception as e:
        print(f"❌ ERROR: {e}")

if __name__ == "__main__":
    test_ocr()
