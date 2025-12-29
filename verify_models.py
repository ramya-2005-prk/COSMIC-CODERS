
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    print("No API Key found")
    exit()

client = genai.Client(api_key=api_key)

try:
    print("Listing models...")
    for m in client.models.list():
        print(f"Model: {m.name}")
except Exception as e:
    print(f"Error listing models: {e}")
