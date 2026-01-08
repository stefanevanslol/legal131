import requests
import io

def test_upload():
    url = "http://127.0.0.1:8000/api/analyze"
    # Create a dummy PDF content (minimal)
    dummy_pdf = b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n/Resources << >>\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000060 00000 n \n0000000157 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n255\n%%EOF"
    
    files = {
        'files': ('test.pdf', dummy_pdf, 'application/pdf')
    }
    
    print(f"Sending POST to {url}...")
    try:
        response = requests.post(url, files=files, timeout=30)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text[:500]}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_upload()
