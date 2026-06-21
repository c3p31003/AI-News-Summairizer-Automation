import requests
from pathlib import Path
from send_email import send_email
from langchain.chat_models import init_chat_model

# Gmail_api_key
api_key_path = Path(__file__).with_name("news_api_key.txt")
api_key_path = api_key_path.read_text(encoding="utf-8").strip()

# Google_gemini_api_key
GOOGLE_API_KEY = Path(__file__).with_name("gemini_api_key.txt")
GOOGLE_API_KEY = GOOGLE_API_KEY.read_text(encoding="utf-8").strip()

topic = 'amazon'

url = (
    f"https://newsapi.org/v2/everything?"
    f"q={topic}&"
    f"from=2026-06-20&sortBy=publishedAt&"
    f"pageSize=3&"
    f"apiKey={api_key_path}&"
    f"language=en"
)
# Make request
request = requests.get(url)

# Make request
r = requests.get(url)

# Get a dictionary with data
content = request.json()
articles = content["articles"][:5]


# AI summarizing the news
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

