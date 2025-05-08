# news_fetcher.py

import feedparser
from datetime import datetime, timedelta
import urllib.parse
import logging

logger = logging.getLogger(__name__)

def fetch_articles(
    search_terms: list[str],
    rss_base_url: str = "https://www.linkedin.com/rss/search",
    days_back: int = 3
) -> list[dict]:
    """
    Sucht in den letzten `days_back` Tagen nach öffentlichen LinkedIn-Beiträgen,
    die eines der `search_terms` im RSS-Feed enthalten.
    """
    cutoff = datetime.utcnow() - timedelta(days=days_back)
    seen_links = set()
    all_articles = []

    for term in search_terms:
        encoded = urllib.parse.quote(term)
        feed_url = f"{rss_base_url}?q={encoded}"
        feed = feedparser.parse(feed_url)

        for entry in feed.entries:
            # Ermittlung des Veröffentlichungsdatums
            pub = getattr(entry, "published_parsed", None)
            published = datetime(*pub[:6]) if pub else None

            # Nur Einträge innerhalb des Zeitfensters
            if published and published < cutoff:
                continue

            link = entry.get("link")
            if not link or link in seen_links:
                continue
            seen_links.add(link)

            all_articles.append({
                "title":   entry.get("title", ""),
                "link":    link,
                "summary": entry.get("summary", "")
            })

    logger.info(f"Gefundene Artikel: {len(all_articles)} (letzte {days_back} Tage)")
    return all_articles