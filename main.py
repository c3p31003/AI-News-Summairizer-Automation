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


topic = "tesla"

url = (
    f"https://newsapi.org/v2/everything?"
    f"q={topic}&"
    f"from=2026-06-20&sortBy=publishedAt&"
    f"pageSize=3&"
    f"apiKey={api_key_path}&"
    f"language=en"
)

# Make request
r = requests.get(url, timeout=20)
r.raise_for_status()

# Get a dictionary with data
content = r.json()

articles = content["articles"][:3]

article_text = "\n\n".join(
    f"Title: {article.get('title', '')}\n"
    f"Description: {article.get('description', '')}\n"
    f"URL: {article.get('url', '')}"
    for article in articles
)

# AI summarizing the news
model = init_chat_model(
    model="gemini-3-flash-preview", model_provider="google-genai",
    api_key=GOOGLE_API_KEY
)

prompt = f"""
You are a news summarizer.
Write 3 short paragraphs.
Paragraph 1: summarize the most important news about {topic}.
Paragraph 2: translate the summary into Japanese.
Paragraph 3: list the most relevant article URL.
Use only the articles below:
{article_text}
"""

print("Generating summary...")
response = model.invoke(prompt)
response_content = response.content
if isinstance(response_content, list):
    response_str = "\n".join(
        item.get("text", "") if isinstance(item, dict) else str(item)
        for item in response_content
    )
else:
    response_str = str(response_content)


print("Sending email...")
send_email(message=response_str)

print("Done.")


# body = body.encode("utf-8")
