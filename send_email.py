import smtplib
import ssl
from email.mime.text import MIMEText
from pathlib import Path

mail_password = Path(__file__).with_name("mail_info.txt")
mail_password = mail_password.read_text(encoding="utf-8").strip()


def send_email(message):
    host = "smtp.gmail.com"
    port = 465

    username = "ishiharu5232@gmail.com"
    password = mail_password

    receiver = "ishiharu5232@gmail.com"
    context = ssl.create_default_context()
    email_message = MIMEText(message, _charset="utf-8")
    email_message["Subject"] = "AI News Summary"
    email_message["From"] = username
    email_message["To"] = receiver

    with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
        server.login(username, password)
        server.send_message(email_message)
