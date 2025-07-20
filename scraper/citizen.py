# scraper/citizen.py
import requests
from bs4 import BeautifulSoup

def get_citizen_articles():
    url = "https://citizen.digital/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        cards = soup.select("div.card-content")

        for card in cards:
            a_tag = card.find("a", href=True)
            title = a_tag.get_text(strip=True)
            link = a_tag["href"]
            if not link.startswith("http"):
                link = "https://citizen.digital" + link

            img_tag = card.find("img")
            image = img_tag["src"] if img_tag else None

            articles.append({
                "title": title,
                "link": link,
                "image": image,
                "source": "Citizen Digital",
                "category": "GENERAL"
            })

        return articles

    except Exception as e:
        print("❌ Citizen scrape error:", e)
        return []
