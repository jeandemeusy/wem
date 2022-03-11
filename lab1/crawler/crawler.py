from typing import Iterator, Tuple
import scrapy


class Crawler(scrapy.Spider):
    name = "quotes"
    start_urls = [
        "https://quotes.toscrape.com/page/1/",
        "https://quotes.toscrape.com/page/2/",
    ]


def parse(self, response):
    print(response.css("title::text").get())
