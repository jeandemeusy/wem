from .crawler import Crawler


def main():
    crawler = Crawler("blogspider", ["https://www.zyte.com/blog/"])

    print(crawler)


if __name__ == "__main__":
    main()
