import os
import openai

# OpenAI-API-Schlüssel aus Umgebungsvariablen laden
openai.api_key = os.getenv('OPENAI_API_KEY')


def summarize_articles(articles, max_sentences=3, model="gpt-3.5-turbo"):
    """
    Erzeugt HTML-Schnipsel mit Überschriften, Kurzfassungen und Links für eine Liste von Artikeln.

    Args:
        articles (list of dict): Jeder dict enthält 'title', 'link', 'summary' (Text des Artikels).
        max_sentences (int): Maximale Anzahl Sätze pro Zusammenfassung.
        model (str): Modellname für die OpenAI-API.

    Returns:
        str: HTML-String mit zusammengefassten Artikeln.
    """
    html_output = []

    for article in articles:
        prompt = (
            f"Fasse bitte in maximal {max_sentences} Sätzen den folgenden LinkedIn-Beitrag zusammen:\n"
            f"Überschrift: {article['title']}\n"
            f"Inhalt: {article['summary']}\n"
            f"Link: {article['link']}\n"
        )
        try:
            response = openai.ChatCompletion.create(
                model=model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3,
                max_tokens=200
            )
            summary_text = response.choices[0].message.content.strip()
        except Exception as e:
            print(f"[ERROR] Zusammenfassung fehlgeschlagen für {article['link']}: {e}")
            summary_text = "Zusammenfassung nicht verfügbar."

        html_output.append(
            f"<h3><a href='{article['link']}'>{article['title']}</a></h3>"
            f"<p><em>Zusammenfassung ({max_sentences} Sätze):</em> {summary_text}</p><hr>"
        )

    return "\n".join(html_output)
