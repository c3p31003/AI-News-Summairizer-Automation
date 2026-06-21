import smtplib
import ssl
from email.message import EmailMessage
from pathlib import Path
from dotenv import load_dotenv
import os

# Load environment variables from .env file
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

MAIL_PASSWORD = os.getenv("MAIL_PASSWORD")

def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "ishiharu5232@gmail.com"
    password = MAIL_PASSWORD

    receiver = "ishiharu5232@gmail.com"
    context = ssl.create_default_context()
    
    if isinstance(message, bytes):
        message = message.decode('utf-8')
    
    msg = EmailMessage()
    msg.set_content(message)          
    msg['Subject'] = 'News Summary'   # 件名
    msg['From'] = username            # 送信元
    msg['To'] = receiver              # 送信先

    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
        server.login(username, password)

        server.send_message(msg)

