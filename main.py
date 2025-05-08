import os
from dotenv import load_dotenv
import openai

from news_fetcher import fetch_articles
from gpt_summary import summarize_articles
from email_sender import send_newsletter

# Umgebungsvariablen laden (OpenAI-API, Gmail-Zugangsdaten, RSS-URL)
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

# Konstanten
RSS_BASE_URL = os.getenv('LINKEDIN_RSS_URL')  # z. B. 'https://www.linkedin.com/rss/search?q='
DAYS_BACK    = int(os.getenv('DAYS_BACK', 3))

# Suchbegriffe aus Datei einlesen
def read_search_terms(path='Search.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]


def build_subject(count):
    from datetime import datetime
    date_str = datetime.utcnow().strftime('%Y-%m-%d')
    return f"LinkedIn-Newsletter: {count} neue Beiträge ({date_str})"


def main():
    # 1. Suche: Suchbegriffe und Artikel
    terms    = read_search_terms()
    articles = fetch_articles(terms, RSS_BASE_URL, days_back=DAYS_BACK)

    if not articles:
        print("[INFO] Keine neuen Artikel gefunden. Newsletter wird nicht gesendet.")
        return

    # 2. Zusammenfassung: HTML-Schnipsel generieren
    articles_html = summarize_articles(articles)

    # 3. Betreff erstellen
    subject = build_subject(len(articles))

    # 4. E-Mail versenden
    send_newsletter(subject, articles_html)


if __name__ == '__main__':
    main()
