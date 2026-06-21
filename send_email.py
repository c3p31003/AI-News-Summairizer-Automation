import smtplib
import ssl
from email.message import EmailMessage
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
    
    if isinstance(message, bytes):
        message = message.decode('utf-8')
    
    msg = EmailMessage()
    msg.set_content(message)          # 本文をセット（日本語も自動で正しくエンコードされます）
    msg['Subject'] = 'News Summary'   # 件名
    msg['From'] = username            # 送信元
    msg['To'] = receiver              # 送信先

    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL(host, port, context=context, timeout=20) as server:
        server.login(username, password)

        server.send_message(msg)

