import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

def send_email(subject: str, body: str, to_email: str) -> None:
    """
    Sendet eine HTML-Mail mit dem gegebenen Subject und Body an to_email.
    """
    from_email = os.getenv("EMAIL_USER")
    password   = os.getenv("EMAIL_PASS")

    msg = MIMEMultipart("alternative")
    msg["From"]    = from_email
    msg["To"]      = to_email
    msg["Subject"] = subject

    html = (
        body +
        f"<p style=\"font-size:small; color:gray;\">"
        f"Automatisch generiert am {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}"
        f"</p>"
    )
    msg.attach(MIMEText(html, "html"))

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(from_email, password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        print("E-Mail erfolgreich gesendet!")
    except Exception as e:
        print(f"Fehler beim E-Mail-Versand: {e}")