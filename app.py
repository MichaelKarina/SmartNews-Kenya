from apscheduler.schedulers.background import BackgroundScheduler
from scraper.tuko import get_tuko_articles
from scraper.filters import categorize_article
from flask import Flask, render_template, jsonify
import json
import datetime
import time
import os

app = Flask(__name__)

# Absolute path to the JSON file in storage folder
ARTICLE_PATH = os.path.join("storage", "articles.json")

@app.route("/")
def home():
    with open("storage/articles.json", "r", encoding="utf-8") as f:
        articles = json.load(f)
    updated_at = datetime.datetime.fromtimestamp(os.path.getmtime("storage/articles.json"))
    return render_template("index.html", articles=articles, updated_at=updated_at)

@app.route("/api/articles")
def api_articles():
    try:
        with open(ARTICLE_PATH, "r", encoding="utf-8") as f:
            articles = json.load(f)
    except:
        articles = []
    return jsonify(articles)

if __name__ == "__main__":
    app.run(debug=True)
    
    
def load_articles():
    with open("storage/articles.json", "r", encoding="utf-8") as f:
        return json.load(f)

@app.route("/")
def index():
    articles = load_articles()
    return render_template("index.html", articles=articles)

@app.route("/category/<category_name>")
def category_page(category_name):
    articles = load_articles()
    filtered = [a for a in articles if a["category"].upper() == category_name.upper()]
    return render_template("index.html", articles=filtered, category=category_name.upper())

def update_articles():
    print("🔄 Auto-updating articles...")
    articles = get_tuko_articles()
    for article in articles:
        article["category"] = categorize_article(article["title"])
    with open("storage/articles.json", "w", encoding="utf-8") as f:
        json.dump(articles, f, indent=4, ensure_ascii=False)
    print(f"✅ {len(articles)} articles saved.")

scheduler = BackgroundScheduler()
scheduler.add_job(update_articles, 'interval', minutes=10)
scheduler.start()

