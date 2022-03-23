import scrapy


class Crawler(scrapy.Spider):
    name = "huff_scrap"

    start_urls = ["https://www.huffpost.com/news"]

    # def __init__(self):
    #     super.__init__(name=Crawler.name, start_urls=Crawler.start_urls)
    #     self.page_number = 0

    def parse(self, response):
        for page in response.css("div.card--standard"):
            if author := page.css("div.card__byline__author__name-title::text").get():
                yield {
                    "title": page.css("h3.card__headline__text::text").get(),
                    "description": page.css("div.card__description::text").get(),
                    "author": author,
                }

        for next_page in response.css("a.pagination__next-link"):
            # This is a recursive function that will call the `parse` function until there are no more
            # pages to crawl.
            yield response.follow(next_page, self.parse)
