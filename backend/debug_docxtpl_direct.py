from docxtpl import DocxTemplate, RichText

# Path to the ORIGINAL template (Standard tags)
template_path = "backend/templates/Natale - GEICO BI Demand (3) (6).docx"
output_path = "backend/debug_output.docx"

def test_render():
    doc = DocxTemplate(template_path)
    
    # Create a RichText object simulating what document_generator produces
    rt = RichText()
    rt.add("This part is normal. ")
    rt.add("This part is bold.", bold=True)
    
    # The template has {{TreatmentsAndDiagnosses}} (Standard tag)
    context = {
        "TreatmentsAndDiagnosses": rt,
        "clientName": "Debug Client" 
    }
    
    print(f"Rendering {template_path} with context: {context}")
    try:
        doc.render(context)
        doc.save(output_path)
        print(f"Saved to {output_path}. Check if 'TreatmentsAndDiagnosses' is visible.")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_render()
