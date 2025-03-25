import scrapy

class ReichSpider(scrapy.Spider):
    name = "reich"
    start_urls = ["https://robertreich.substack.com/archive"]

    def parse(self, response):
        # Extract all article links
        for link in response.css("a[href*='/p/']::attr(href)").getall():
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        title = response.css("h1::text").get()

        # Grab all visible text from paragraphs
        paragraphs = response.css("div#root p::text, div#root p strong::text").getall()
        clean_text = [p.strip() for p in paragraphs if p.strip()]

        yield {
            "title": title,
            "text": clean_text,
            "source": response.url
        }

class ReichSpider(scrapy.Spider):
    name = "reich"
    start_urls = ["https://robertreich.substack.com/archive"]

    def parse(self, response):
        for link in response.css("a[href*='/p/']::attr(href)").getall():
            full_url = response.urljoin(link)
            yield scrapy.Request(full_url, callback=self.parse_article)

    def parse_article(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "text": response.css("div.post-body p::text").getall(),
            "source": response.url
        }

