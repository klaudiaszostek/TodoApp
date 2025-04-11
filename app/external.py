from app.models import Quote
from app.app import db
import requests

def fetch_and_store_quote():
    try:
        response = requests.get("https://zenquotes.io/api/random")
        data = response.json()
        quote_text = data[0]['q']
        author = data[0]['a']
        quote = Quote(text=quote_text, author=author)
        db.session.add(quote)
        db.session.commit()
    except Exception as e:
        print("Error getting quote: ", e)