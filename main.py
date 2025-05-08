# main.py

import os
from dotenv import load_dotenv
from news_fetcher import fetch_articles
from gpt_summary import summarize_articles
from email_sender import send_email   # ← hier angepasst

def read_search_terms(path="Search.txt"):
    with open(path, "r") as f:
        return [l.strip() for l in f if l.strip()]

def main():
    load_dotenv()

    terms    = read_search_terms()
    articles = fetch_articles(terms, days_back=3)
    if not articles:
        print("Keine neuen Artikel gefunden.")
        return

    newsletter = summarize_articles(articles)
    send_email(
        subject  = "Dein LinkedIn-Newsletter",
        body     = newsletter,
        to_email = os.getenv("EMAIL_USER")  # oder eine beliebige Empfängeradresse
    )
    print("Newsletter verschickt!")

if __name__ == "__main__":
    main()