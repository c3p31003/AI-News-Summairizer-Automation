from pathlib import Path
import requests
from langchain.chat_models import init_chat_model

GOOGLE_API_KEY = Path(__file__).with_name("gemini_api_key.txt")
GOOGLE_API_KEY = GOOGLE_API_KEY.read_text(encoding="utf-8").strip()

model = init_chat_model(
    model="gemini-3-flash-preview", model_provider="google-genai",
    api_key=GOOGLE_API_KEY
    )

response = model.invoke("Is a pen better than a pencil?")

item = response.content[0]['text']


with open("response.txt","w",encoding="utf-8") as f:
    f.write(item)
    
