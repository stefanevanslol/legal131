import requests

url = "http://localhost:8000/api/analyze"

# Create dummy PDF content
files = [
    ('files', ('test1.pdf', b'%PDF-1.4 dummy content 1', 'application/pdf')),
    ('files', ('test2.pdf', b'%PDF-1.4 dummy content 2', 'application/pdf'))
]

try:
    response = requests.post(url, files=files)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
