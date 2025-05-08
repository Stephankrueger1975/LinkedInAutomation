import sys
import os
import pytest
from datetime import datetime, timedelta, timezone

# Damit pytest Dein Modul findet
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from news_fetcher import fetch_articles

# Dummy-Klassen für Tests
class DummyEntry:
    def __init__(self, title, link, summary, published_dt):
        self.title = title
        self.link = link
        self.summary = summary
        # Simuliere published_parsed
        self.published_parsed = published_dt.timetuple()

class DummyFeed:
    def __init__(self, entries, bozo=False):
        self.entries = entries
        self.bozo = bozo

def make_feed(entries):
    return DummyFeed(entries)

def test_import_fetch_articles():
    # Sicherstellen, dass die Funktion existiert
    assert callable(fetch_articles)

def test_fetch_articles_empty(monkeypatch):
    # Leerer Feed → leere Liste
    class EmptyFeed:
        bozo = False
        entries = []
    monkeypatch.setattr('news_fetcher.feedparser.parse', lambda url: EmptyFeed())

    result = fetch_articles([], 'https://example.com/rss', days_back=1)
    assert isinstance(result, list)
    assert result == []

def test_date_filter(monkeypatch):
    # Erzeuge einen alten (4 Tage) und einen neuen Eintrag (1 Tag)
    old = DummyEntry(
        "Alt", "http://a", "Inhalt",
        datetime.now(timezone.utc) - timedelta(days=4)
    )
    new = DummyEntry(
        "Neu", "http://b", "Inhalt",
        datetime.now(timezone.utc) - timedelta(days=1)
    )
    monkeypatch.setattr('news_fetcher.feedparser.parse', lambda url: make_feed([old, new]))
    
    # Suche nach "Inhalt", das in beiden Summaries vorkommt
    result = fetch_articles(["Inhalt"], "https://example.com/rss", days_back=3)
    # Nur der neue Artikel (1 Tag alt) soll zurückkommen
    assert len(result) == 1
    assert result[0]['link'] == "http://b"

def test_duplicate_links(monkeypatch):
    # Zwei Einträge mit gleichem Link
    ent1 = DummyEntry("Titel1", "http://dup", "Inhalt", datetime.now(timezone.utc))
    ent2 = DummyEntry("Titel2", "http://dup", "Inhalt", datetime.now(timezone.utc))
    monkeypatch.setattr('news_fetcher.feedparser.parse', lambda url: make_feed([ent1, ent2]))
    
    result = fetch_articles(["Inhalt"], "https://example.com/rss", days_back=1)
    # Trotz zweier Einträge mit demselben Link nur ein Eintrag
    assert len(result) == 1
    assert result[0]['title'] in {"Titel1", "Titel2"}