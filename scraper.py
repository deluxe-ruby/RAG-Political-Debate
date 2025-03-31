import json
import os
import scrapy
from scrapy.crawler import CrawlerProcess

CONFIG_FILE = "sources.json"
OUTPUT_FILE = "left_articles.json"

def load_sources(side="left"):
    if not os.path.exists(CONFIG_FILE):
        print("❌ No sources.json found.")
        return []
    with open(CONFIG_FILE, "r") as f:
        config = json.load(f)
        return config.get(f"{side}_sources", {}).get("website", [])

class ArticleSpider(scrapy.Spider):
    name = "article_scraper"

    def __init__(self, start_urls=None, **kwargs):
        super().__init__(**kwargs)
        self.start_urls = start_urls or []

    def parse(self, response):
        print("\n🔍 URL:", response.url)
        print("🧱 RAW HTML (first 3000 chars):\n", response.text[:3000])

if __name__ == "__main__":
    websites = load_sources("left")
    urls = [site["url"] for site in websites]
    if not urls:
        print("⚠️ No website sources found for scraping.")
    else:
        process = CrawlerProcess(settings={
            "FEEDS": {
                OUTPUT_FILE: {"format": "json"},
            },
            "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36"
        })
        process.crawl(ArticleSpider, start_urls=urls)
        process.start()
