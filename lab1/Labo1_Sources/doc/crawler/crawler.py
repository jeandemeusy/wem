import scrapy

class Crawler(scrapy.Spider):
    def __init__(self, name:str,start_urls: list[str]):
        self.name = name
        self.start_urls = start_urls

    def parse(self, response):
        print(response.css("title::text").get())

    