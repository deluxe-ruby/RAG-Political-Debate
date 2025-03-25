import scrapy

class LeftSpider(scrapy.Spider):
    name = "left_news"
    start_urls = [
        "https://www.mediamatters.org/latest"
    ]

    def parse(self, response):
        for article in response.css("div.latest-stories article a::attr(href)").getall():
            yield response.follow(article, self.parse_article)

    def parse_article(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "text": response.css("div.article-content p::text").getall(),
            "source": response.url
        }
