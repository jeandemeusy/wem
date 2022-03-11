import scrapy


class Crawler(scrapy.Spider):
    def __init__(self, name: str, start_urls: list[str]):
        self.name = name
        self.start_urls = start_urls

    def parse(self, response):
        for title in response.css(".oxy-post-title"):
            yield {"title": title.css("::text").get()}

        for next_page in response.css("a.next"):
            yield response.follow(next_page, self.parse)
