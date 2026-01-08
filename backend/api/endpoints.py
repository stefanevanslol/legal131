from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse
from fastapi.concurrency import run_in_threadpool
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import shutil
import os
import uuid
import json
import logging
import traceback

from backend.core.ocr_processor import OCRProcessor
from backend.core.ai_analyzer import AIAnalyzer
from backend.core.document_generator import DocumentGenerator

# Configure Logging
# Create a custom logger
logger = logging.getLogger("backend")
logger.setLevel(logging.INFO)

# Create handlers
f_handler = logging.FileHandler('backend/debug.log')
f_handler.setLevel(logging.INFO)

# Create formatters and add it to handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
f_handler.setFormatter(formatter)

# Add handlers to the logger
if not logger.handlers:
    logger.addHandler(f_handler)

# Prevent propagation to root logger (which might have broken stdout/stderr handlers)
logger.propagate = False

router = APIRouter()

# Directories
UPLOAD_DIR = "backend/uploads"
OUTPUT_DIR = "backend/outputs"
TEMPLATE_PATH = "backend/templates/Natale - GEICO BI Demand (3) (6).docx"

os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Services
ocr = OCRProcessor()
analyzer = AIAnalyzer()
doc_gen = DocumentGenerator(TEMPLATE_PATH)

class GenerateRequest(BaseModel):
    data: Dict[str, Any]

@router.post("/analyze")
async def analyze_file(files: List[UploadFile] = File(..., alias="files")):
    """
    Uploads PDFs, runs OCR/Text Extraction, and uses AI to extract medical data.
    """
    try:
        logger.info(f"Starting analysis for {len(files)} files...")
        combined_text = ""
        saved_files = []
        
        for file in files:
            # Save file
            file_id = str(uuid.uuid4())
            file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
            
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(file.file, buffer)
            
            saved_files.append(file.filename)
            logger.info(f"Saved file: {file.filename} as {file_path}")
                
            # Read file for processing
            with open(file_path, "rb") as f:
                content = f.read()
                
            # Extract Text
            # Run blocking OCR in a separate thread to avoid blocking the event loop
            logger.info(f"Running OCR for {file.filename}...")
            text = await run_in_threadpool(ocr.extract_text_from_pdf, content)
            combined_text += f"\n--- File: {file.filename} ---\n{text}"
        
        # Analyze with AI
        logger.info("Sending text to AIAnalyzer...")
        analysis_result = await analyzer.analyze_medical_records(combined_text)
        logger.info("Analysis complete.")
        
        if "error" in analysis_result:
             logger.error(f"AI Analysis returned error: {analysis_result['error']}")
        
        return {
            "file_ids": [f for f in saved_files],
            "extracted_data": analysis_result,
            "raw_text_preview": combined_text[:500] + "..."
        }
            
    except Exception as e:
        logger.error(f"Analysis Error: {e}")
        logger.error(traceback.format_exc())
        # print(f"DEBUG: Analysis Error: {e}")
        # traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/generate")
async def generate_document(request: GenerateRequest):
    """
    Generates the demand letter Word document from the provided data.
    """
    try:
        logger.info("Starting document generation...")
        output_filename = f"Demand_Letter_{uuid.uuid4()}.docx"
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        
        doc_gen.generate_demand_letter(request.data, output_path)
        
        logger.info(f"Document generated at {output_path}")
        
        return FileResponse(
            path=output_path, 
            filename=output_filename, 
            media_type='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )
    except Exception as e:
        logger.error(f"Generation Error: {e}")
        logger.error(traceback.format_exc())
        print(f"DEBUG: Generation Error: {e}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
