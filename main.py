import requests
from pathlib import Path
from send_email import send_email
from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
NEWS_API_KEY = os.getenv("NEWS_API_KEY")



topic = 'amazon'

url = (
    f"https://newsapi.org/v2/everything?"
    f"q={topic}&"
    f"from=2026-06-21&sortBy=publishedAt&"
    f"pageSize=3&"
    f"apiKey={NEWS_API_KEY}&"
    f"language=en"
)
# Make request
request = requests.get(url)

# Make request
r = requests.get(url)

# Get a dictionary with data
content = request.json()
articles = content["articles"][:5]


#AI summarizing the news
model = init_chat_model(
    model="gemini-2.5-flash",
    model_provider="google-genai",
    api_key=GOOGLE_API_KEY,
)

prompt = f"""
You are a news summarizer.
Write 3 short paragraphs.
Paragraph 1: summarize the most important news about {topic}.
Paragraph 2: translate the summary into Japanese.
Paragraph 3: list the most relevant article URL.
Use only the articles below:
{articles}
"""

response = model.invoke(prompt)
response_str = response.content


body = "Subject: News Summary\n\n" + response_str + "\n\n"

body = body.encode('utf-8')

send_email(message=body)

