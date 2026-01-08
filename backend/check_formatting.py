from docx import Document

output_path = "backend/outputs/debug_direct.docx"
doc = Document(output_path)

found_text = "DIRECT REPLACEMENT TEST"

print(f"Checking formatting for: '{found_text}'")

for p in doc.paragraphs:
    if found_text in p.text:
        print(f"Found in paragraph: '{p.text}'")
        for run in p.runs:
            if found_text in run.text:
                print(f"Run text: '{run.text}'")
                print(f"Bold: {run.bold}")
                print(f"Underline: {run.underline}")
                # None means "inherit", usually false if paragraph style is Normal.
                
                # Check paragraph style
                print(f"Paragraph style: {p.style.name}")

# Also check tables if needed (previous script found it in paragraphs?)
# Step 478 said "Found replacement text in paragraphs."
