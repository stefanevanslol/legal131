from docxtpl import DocxTemplate, RichText
import os
import re
import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class DocumentGenerator:
    def __init__(self, template_path: str):
        self.template_path = template_path

    def _process_rich_text(self, text: str):
        """
        Parses text for double asterisks (e.g. **bold**) and converts to RichText.
        """
        if not isinstance(text, str) or "**" not in text:
            return text
            
        rt = RichText()
        # Split by the bold pattern
        parts = re.split(r'(\*\*.*?\*\*)', text)
        
        for part in parts:
            if part.startswith('**') and part.endswith('**') and len(part) > 4:
                # Add bold part without asterisks
                rt.add(part[2:-2], bold=True)
            elif part:
                # Add normal part
                rt.add(part)
        return rt

    def generate_demand_letter(self, data: Dict[str, Any], output_path: str):
        """
        Generates a demand letter by filling in the template using docxtpl.
        """
        if not os.path.exists(self.template_path):
            raise FileNotFoundError(f"Template not found at {self.template_path}")

        # Use DocxTemplate for robust replacement
        doc = DocxTemplate(self.template_path)
        
        # Clean keys for Jinja2 (remove trailing spaces like in "ClaimNo ")
        # And process rich text
        context = {}
        for k, v in data.items():
            clean_key = k.strip()
            if isinstance(v, str) and "**" in v:
                val = self._process_rich_text(v)
            else:
                val = v
            context[clean_key] = val

        # DUAL MAPPING STRATEGY: 
        # Ensure both spellings (Diagnoses/Diagnosses) exist to match whatever the template has.
        if "TreatmentsAndDiagnosses" in context and "TreatmentsAndDiagnoses" not in context:
            context["TreatmentsAndDiagnoses"] = context["TreatmentsAndDiagnosses"]
        elif "TreatmentsAndDiagnoses" in context and "TreatmentsAndDiagnosses" not in context:
            context["TreatmentsAndDiagnosses"] = context["TreatmentsAndDiagnoses"]
            
        if "TreatmentsAndDiagnosses2" in context and "TreatmentsAndDiagnoses2" not in context:
            context["TreatmentsAndDiagnoses2"] = context["TreatmentsAndDiagnosses2"]
        elif "TreatmentsAndDiagnoses2" in context and "TreatmentsAndDiagnosses2" not in context:
            context["TreatmentsAndDiagnosses2"] = context["TreatmentsAndDiagnoses2"]
        
        # Render the template
        doc.render(context)
        
        # Save
        doc.save(output_path)
        return output_path
