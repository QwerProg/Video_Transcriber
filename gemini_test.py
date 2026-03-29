import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("未读取到 GOOGLE_API_KEY，请检查 .env")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-3.1-flash-lite-preview",
    contents="你叫什么名字",
)
print(response.text)
