import sys
import os
import pytest

# Damit pytest Dein Modul findet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from gpt_summary import summarize_articles

class DummyResponse:
    def __init__(self, content):
        # Simulation: resp.choices[0].message.content
        self.choices = [type("Choice", (), {"message": type("M", (), {"content": content})})]

def test_import_summarize_articles():
    assert callable(summarize_articles)

def test_summarize_single_article(monkeypatch):
    article = {
        'title': 'Test Titel',
        'link': 'http://link',
        'summary': 'Dies ist der Inhalt.'
    }

    # Mock der OpenAI-ChatCompletion
    def fake_create(model, messages, temperature, max_tokens):
        # Stellen wir sicher, dass der Prompt den Artikeltext enthält
        assert 'Dies ist der Inhalt.' in messages[0]['content']
        return DummyResponse("Kurze Zusammenfassung.")

    monkeypatch.setattr('gpt_summary.openai.ChatCompletion.create', fake_create)

    html = summarize_articles([article], max_sentences=2, model="fake-model")
    assert "<h3><a href='http://link'>Test Titel</a></h3>" in html
    assert "Kurze Zusammenfassung." in html

def test_summarize_api_error(monkeypatch):
    article = {
        'title': 'Fehlerfall',
        'link': 'http://error',
        'summary': 'Inhalt'
    }

    # Mock wirft RuntimeError
    def fake_error(*args, **kwargs):
        raise RuntimeError("API-Fehler")

    monkeypatch.setattr('gpt_summary.openai.ChatCompletion.create', fake_error)

    html = summarize_articles([article], max_sentences=1)
    # Bei Fehler sollte der Fallback-Text auftauchen
    assert "Zusammenfassung nicht verfügbar." in html