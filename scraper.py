import scrapy

class NewsSpider(scrapy.Spider):
    name = "news"
    start_urls = [
        "https://www.breitbart.com/",
        "https://www.foxnews.com/opinion"
    ]

    def parse(self, response):
        for article in response.css("h2 a::attr(href)").getall():
            yield response.follow(article, self.parse_article)

    def parse_article(self, response):
        yield {
            "title": response.css("h1::text").get(),
            "text": response.css("p::text").getall()
        }
