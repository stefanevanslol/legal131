import os
from dotenv import load_dotenv

# Build path to .env file (assuming it's in the same directory as this config.py or parent)
# Since config.py is in backend/, and .env is in backend/.env:
env_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(env_path)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
