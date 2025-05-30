import os
import openai
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def summarize_articles(articles: list[dict]) -> str:
    """
    Nimmt eine Liste von Artikeln (mit 'title','link','summary')
    und gibt ein HTML-Snippet mit Überschriften, Zusammenfassungen und Links zurück.
    """
    summaries = ""
    for article in articles:
        prompt = f"Fasse diesen Artikel zusammen:\n{article['summary']}\n"
        try:
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt=prompt,
                max_tokens=150,
                temperature=0.5
            )
            summary = response.choices[0].text.strip()
            summaries += (
                f"<h3>{article['title']}</h3>"
                f"<p>{summary}</p>"
                f"<a href='{article['link']}'>Read full article</a><hr>"
            )
        except Exception as e:
            print(f"Fehler bei der Zusammenfassung: {e}")
    return summaries