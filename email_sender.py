import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime


def send_newsletter(subject, articles_html, to_email=None):
    """
    Sendet eine HTML-Newsletter-E-Mail via Gmail SMTP.

    Args:
        subject (str): Betreff der E-Mail.
        articles_html (str): HTML-Inhalt der Artikel.
        to_email (str, optional): Empfängeradresse. Standard: Umgebungsvariable EMAIL_USER.
    """
    # E-Mail-Konfiguration aus Umgebungsvariablen
    from_email = os.getenv('EMAIL_USER')
    password   = os.getenv('EMAIL_APP_PASS')
    recipient  = to_email or from_email

    # MIME-Nachricht aufbauen
    msg = MIMEMultipart('alternative')
    msg['From']    = from_email
    msg['To']      = recipient
    msg['Subject'] = subject

    # HTML-Teil anhängen
    html_content = f"""
    <html><body>
      <h2>{subject}</h2>
      {articles_html}
      <hr>
      <p style=\"font-size:small; color:gray;\">Automatisch generiert am {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}</p>
    </body></html>
    """
    msg.attach(MIMEText(html_content, 'html'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            server.login(from_email, password)
            server.send_message(msg)
        print(f"[INFO] Newsletter gesendet an {recipient}")
    except Exception as e:
        print(f"[ERROR] Fehler beim E-Mail-Versand: {e}")
