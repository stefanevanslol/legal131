from docxtpl import DocxTemplate
import re

template_path = r"backend/templates/Natale - GEICO BI Demand (3) (5).docx"

try:
    doc = DocxTemplate(template_path)
    # docxtpl doesn't have a direct "list variables" method easily accessible without parsing XML
    # But checking get_docx() text might help, or we can use a regex on the XML content.
    
    print(f"Reading template: {template_path}")
    
    # We can try to render with a dummy context to see what's missing, 
    # but simpler is to regex search the xml for {{...}}
    xml_content = doc.get_docx().parsed
    
    # This is a rough estimation. 
    # A better way is to use the undeclared_variables feature of jinja2 environment 
    # created by docxtpl, but docxtpl hides it.
    
    # Let's try to parse the text directly from the doc object first
    full_text = []
    for p in doc.docx.paragraphs:
        full_text.append(p.text)
    
    for table in doc.docx.tables:
        for row in table.rows:
            for cell in row.cells:
                full_text.append(cell.text)
                
    text = "\n".join(full_text)
    
    # Find patterns like {{ variable }}
    import re
    matches = re.findall(r"\{\{(.*?)\}\}", text)
    
    print("\n--- Found Jinja2 Tags (approx) ---")
    unique_tags = sorted(list(set([m.strip() for m in matches])))
    for tag in unique_tags:
        print(f"'{tag}'")
        
except Exception as e:
    print(f"Error reading template: {e}")
