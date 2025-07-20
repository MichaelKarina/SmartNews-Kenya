import requests
from bs4 import BeautifulSoup
import json
import os
from concurrent.futures import ThreadPoolExecutor, as_completed

HEADERS = {'User-Agent': 'Mozilla/5.0'}

def get_og_image(article_url):
    try:
        res = requests.get(article_url, headers=HEADERS, timeout=5)
        soup = BeautifulSoup(res.text, "html.parser")
        meta = soup.find("meta", property="og:image")
        if meta and meta.get("content"):
            return meta["content"]
    except Exception as e:
        print(f"⚠️ Image fetch failed: {article_url}\n→ {e}")
    return None

def classify_category(title, href):
    title = title.lower()
    if "siasa" in href or "ruto" in title or "rais" in title:
        return "POLITICS"
    elif "michezo" in href or "football" in title:
        return "FOOTBALL"
    elif "burudani" in href:
        return "ENTERTAINMENT"
    elif "mahusiano" in href:
        return "RELATIONSHIPS"
    elif "biashara" in href:
        return "BUSINESS"
    else:
        return "GENERAL"

def get_article_links():
    url = "https://kiswahili.tuko.co.ke/"
    try:
        res = requests.get(url, headers=HEADERS)
        soup = BeautifulSoup(res.text, "html.parser")
        links = []

        for link in soup.find_all("a", href=True):
            title = link.get_text(strip=True)
            href = link["href"]
            full_url = href if href.startswith("http") else "https://kiswahili.tuko.co.ke" + href

            if (
                "/" in href and
                href.count("/") > 2 and
                len(title) > 30 and
                "tuko.co.ke" in full_url and
                not any(x in href for x in ["#", "tag", "privacy", "login", "about", "category"])
            ):
                links.append((title, full_url))
        return links

    except Exception as e:
        print("❌ Error while scraping homepage:", e)
        return []

def get_full_article_data(title_url):
    title, url = title_url
    category = classify_category(title, url)
    image = get_og_image(url)

    return {
        "title": title,
        "link": url,
        "source": "Tuko Swahili",
        "category": category,
        "image": image
    }

def get_tuko_articles():
    links = get_article_links()
    articles = []

    print(f"🚀 Fetching {len(links)} articles with thumbnails (multithreaded)...")
    with ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(get_full_article_data, link) for link in links]

        for future in as_completed(futures):
            try:
                article = future.result()
                articles.append(article)
            except Exception as e:
                print("⚠️ Error in future:", e)

    return articles

def save_to_json(data, filename="storage/articles.json"):
    try:
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ Saved {len(data)} articles to {filename}")
    except Exception as e:
        print("❌ Failed to save articles:", str(e))

if __name__ == "__main__":
    articles = get_tuko_articles()
    if articles:
        save_to_json(articles)
    else:
        print("⚠️ No articles found.")
