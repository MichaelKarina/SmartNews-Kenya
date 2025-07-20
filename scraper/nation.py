# scraper/nation.py
import requests
from bs4 import BeautifulSoup

def get_nation_articles():
    url = "https://nation.africa/kenya/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    articles = []

    try:
        res = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        stories = soup.select("div.teaser__content")

        for story in stories:
            a_tag = story.find("a", href=True)
            title = a_tag.get_text(strip=True)
            link = a_tag["href"]
            if not link.startswith("http"):
                link = "https://nation.africa" + link

            image_tag = story.find_previous("img")
            image = image_tag["src"] if image_tag else None

            articles.append({
                "title": title,
                "link": link,
                "image": image,
                "source": "Nation Africa",
                "category": "GENERAL"
            })

        return articles

    except Exception as e:
        print("❌ Nation scrape error:", e)
        return []
