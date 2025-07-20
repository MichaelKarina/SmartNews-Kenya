import requests
from bs4 import BeautifulSoup
import json
import os

def get_tuko_articles():
    url = "https://kiswahili.tuko.co.ke/"
    headers = {
        'User-Agent': 'Mozilla/5.0'
    }

    try:
        response = requests.get(url, headers=headers)
        print("Status Code:", response.status_code)

        if response.status_code != 200:
            print("Error fetching page")
            return []

        print("✅ Page fetched successfully!")

        soup = BeautifulSoup(response.text, "html.parser")

        articles = []

        print("\n--- LINK DEBUG START ---")
        for link in soup.find_all("a", href=True):
            title = link.get_text(strip=True)
            href = link["href"]
            full_url = href if href.startswith("http") else "https://kiswahili.tuko.co.ke" + href

            print(f"🧪 Title: {title[:60]} | Href: {href}")

            # Improved filter for real article links
            if (
                "/" in href and
                href.count("/") > 2 and
                len(title) > 30 and
                "tuko.co.ke" in full_url and
                not any(x in href for x in ["#", "tag", "privacy", "login", "about", "category"])
            ):
                # Basic category detection
                if "siasa" in href or "ruto" in title.lower() or "rais" in title.lower():
                    category = "POLITICS"
                elif "michezo" in href or "football" in title.lower():
                    category = "FOOTBALL"
                elif "burudani" in href:
                    category = "ENTERTAINMENT"
                elif "mahusiano" in href:
                    category = "RELATIONSHIPS"
                elif "biashara" in href:
                    category = "BUSINESS"
                else:
                    category = "GENERAL"

                articles.append({
                    "title": title,
                    "link": full_url,
                    "source": "Tuko Swahili",
                    "category": category
                })
        print("--- LINK DEBUG END ---\n")

        return articles

    except Exception as e:
        print("❌ Error:", str(e))
        return []

def save_to_json(data, filename="articles.json"):
    try:
        filepath = os.path.abspath(filename)
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved {len(data)} articles to {filepath}")
    except Exception as e:
        print("❌ Failed to save articles:", str(e))

if __name__ == "__main__":
    articles = get_tuko_articles()

    if articles:
        save_to_json(articles)
    else:
        print("No articles found. Please check scraper or network.")
