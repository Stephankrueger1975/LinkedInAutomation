import feedparser
import urllib.parse
from datetime import datetime, timedelta, timezone

def fetch_articles(search_terms, rss_base_url, days_back=3):
    """
    Ruft Artikel aus LinkedIn-RSS-Feeds ab, filtert nach Datum und Suchbegriffen.

    Args:
        search_terms (list of str): Liste der Schlagwörter.
        rss_base_url (str): Basis-URL für LinkedIn-RSS-Feeds (z.B. "https://www.linkedin.com/rss/search?q=").
        days_back (int): Zeitraum in Tagen für Rückwärtssuche (Standard: 3).

    Returns:
        list of dict: Gefilterte Artikel mit 'title', 'link', 'summary' und 'published'.
    """
    cutoff = datetime.now(timezone.utc) - timedelta(days=days_back)
    collected = []
    seen_links = set()

    for term in search_terms:
        encoded = urllib.parse.quote(term)
        feed_url = f"{rss_base_url}{encoded}"
        feed = feedparser.parse(feed_url)

        if feed.bozo:
            print(f"[WARN] Fehler beim Parsen des Feeds für '{term}': {feed.bozo_exception}")
            continue

        for entry in getattr(feed, 'entries', []):
            # Einträge ohne published_parsed ignorieren
            if not hasattr(entry, 'published_parsed'):
                continue

            # Veröffentlichungstermin mit UTC-Zeitzone
            published = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published < cutoff:
                continue

            # Duplikate anhand des Links vermeiden
            if entry.link in seen_links:
                continue

            text = (entry.title + ' ' + getattr(entry, 'summary', '')).lower()
            if any(term.lower() in text for term in search_terms):
                collected.append({
                    'title': entry.title,
                    'link': entry.link,
                    'summary': entry.summary,
                    'published': published
                })
                seen_links.add(entry.link)

    print(f"[INFO] Gefundene Artikel: {len(collected)} (letzte {days_back} Tage)")
    return collected