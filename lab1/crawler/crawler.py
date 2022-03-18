import scrapy


class Crawler(scrapy.Spider):
    name = "huff_scrap"
    base_url = "https://www.huffpost.com/news"

    # start_urls = [f"https://www.huffpost.com/news/?page={page}" for page in range(69)]
    start_urls = ["https://www.huffpost.com/news"]

    def parse(self, response):

        for title in response.css(".card__headlines"):
            print(title)
            yield {"title": title.css("::text").get()}

        for next_page in response.css("a.pagination__next-link"):
            # This is a recursive function that will call the `parse` function until there are no more
            # pages to crawl.
            yield response.follow(next_page, self.parse)
