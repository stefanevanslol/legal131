# Legal Demand Letter App

## Prerequisites

1. **Python 3.10+** (Installed)
2. **Node.js 18+** (Installed)
3. **Tesseract OCR**
   - Download and install from [UB-Mannheim/tesseract](https://github.com/UB-Mannheim/tesseract/wiki).
   - Add the installation path (e.g., `C:\Program Files\Tesseract-OCR`) to your System PATH, or update `backend/core/ocr_processor.py`.
4. **Poppler for Windows**
   - Required for `pdf2image`.
   - Download from [latest releases](https://github.com/oschwartz10612/poppler-windows/releases/).
   - Extract and add the `bin` folder to your System PATH.

## Setup

### Backend
1. Navigate to `backend`:
   ```bash
   cd backend
   ```
2. Create virtual environment (optional but recommended):
   ```bash
   python -m venv venv
   .\venv\Scripts\activate
   ```
3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Create a `.env` file in `backend`:
   ```
   OPENAI_API_KEY=your_key_here
   ```
5. Run the server:
   ```bash
   uvicorn main:app --reload
   ```

### Frontend
1. Navigate to `frontend`:
   ```bash
   cd frontend
   ```
2. Install dependencies (if not done):
   ```bash
   npm install
   ```
3. Run the development server:
   ```bash
   npm run dev
   ```

## Usage
1. Open http://localhost:3000
2. Upload a Medical PDF.
3. Review extracted data.
4. Click "Generate Demand" to download the Docx.
