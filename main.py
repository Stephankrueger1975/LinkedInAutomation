import os
from dotenv import load_dotenv
from news_fetcher import fetch_articles
from gpt_summary import summarize_articles
from email_sender import send_email

def read_search_terms(path: str = "Search.txt") -> list[str]:
    with open(path, "r") as f:
        return [line.strip() for line in f if line.strip()]

def main() -> None:
    load_dotenv()
    terms = read_search_terms()
    articles = fetch_articles(terms)  # nutzt defaults: rss_base_url & days_back=3

    if not articles:
        print("Keine neuen Artikel gefunden.")
        return

    newsletter = summarize_articles(articles)
    send_email(
        subject  = "Dein LinkedIn-Newsletter",
        body     = newsletter,
        to_email = os.getenv("EMAIL_USER")
    )
    print("Newsletter verschickt!")

if __name__ == "__main__":
    main()