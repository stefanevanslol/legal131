from backend.core.document_generator import DocumentGenerator
import os
import logging

# Setup basic logging
logging.basicConfig(level=logging.INFO)

template_path = "backend/templates/Natale - GEICO BI Demand (3) (6).docx"
output_path = "backend/outputs/debug_output.docx"

data = {
    "clientName": "Test Client",
    "TreatmentsAndDiagnosses": "This is a TEST treatment description.\nShould not be bold.",
    "TreatmentsAndDiagnosses2": "This is a TEST treatment description 2.\nShould not be bold.",
    "ClaimNo": "12345",
    "DateOfLoss": "01/01/2024"
}

try:
    print(f"Generating document using template: {template_path}")
    generator = DocumentGenerator(template_path)
    generator.generate_demand_letter(data, output_path)
    print(f"Document generated at: {output_path}")
    print("Please check this document manually.")
except Exception as e:
    print(f"Error: {e}")
