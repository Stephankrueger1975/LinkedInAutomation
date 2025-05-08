import sys
import os
import pytest
from email.mime.multipart import MIMEMultipart

# Damit pytest Dein Modul findet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import email_sender

def test_import_send_newsletter():
    assert callable(email_sender.send_newsletter)

class DummySMTP:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.logged_in = False
        self.sent = False

    def login(self, user, pwd):
        # Simuliere Login-Fehler, wenn falsche Daten
        if user != "user@example.com" or pwd != "secret":
            raise RuntimeError("Login failed")
        self.logged_in = True

    def send_message(self, msg):
        # Es muss eine MIMEMultipart-Nachricht sein und login erfolgreich
        assert isinstance(msg, MIMEMultipart)
        assert self.logged_in is True
        self.sent = True

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        return False

@pytest.fixture(autouse=True)
def set_env(monkeypatch):
    # Globale Umgebungsvariablen für Tests
    monkeypatch.setenv('EMAIL_USER', 'user@example.com')
    monkeypatch.setenv('EMAIL_APP_PASS', 'secret')

def test_send_success(monkeypatch):
    # Erfolgreiches Senden
    monkeypatch.setattr('email_sender.smtplib.SMTP_SSL', DummySMTP)
    # Sollte keine Exception werfen
    email_sender.send_newsletter(
        subject="Test Betreff",
        articles_html="<p>Content</p>"
    )

def test_send_login_failure(monkeypatch, capsys):
    # Falsche Credentials erzeugen Login-Fehler
    monkeypatch.setenv('EMAIL_USER', 'wrong@example.com')
    monkeypatch.setenv('EMAIL_APP_PASS', 'wrongpass')
    monkeypatch.setattr('email_sender.smtplib.SMTP_SSL', DummySMTP)

    # Aufruf: fängt den Fehler intern ab und printed eine Fehlermeldung
    email_sender.send_newsletter("Betreff", "<p>Text</p>")
    captured = capsys.readouterr()
    assert "[ERROR] Fehler beim E-Mail-Versand" in captured.out