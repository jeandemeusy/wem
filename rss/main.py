import hashlib
import json
from xml.etree import ElementTree as etree

import requests
import unidecode
from bs4 import BeautifulSoup
import sys
from pathlib import Path

# usage:
# python3 rss/main.py <outfolder>
# folder should exists


def RSS_content(
    infile: str = None,
    outfile: Path = None,
    feed: dict = None,
    tag: str = None,
    class_attr: str = None,
):
    """
    Get content of all items in an RSS feed.
    """

    assert tag != None, "Tag must be specified"
    assert class_attr != None, "Class attribute must be specified"

    print(f"Parsing {infile if infile else ''}...")

    if infile:
        with open(infile, "r") as f:
            feed = json.load(f)

    content_dict = {}

    for idx, f in enumerate(feed):
        if f["link"]:
            r = requests.get(f["link"])
            soup = BeautifulSoup(r.text, "html.parser")
            texts = soup.find_all(tag, attrs={"class": class_attr})

            hashed = hashlib.sha224(f["link"].encode("utf-8")).hexdigest()

            decoded_texts = [
                unidecode.unidecode(t.text).replace('"', "'") for t in texts
            ]
            content_dict[hashed] = " ".join(decoded_texts)
            
        print(f"{idx}/{len(feed)}", end="\r")

    if outfile:
        try:
            with open(str(outfile), "r") as f:
                content_dict = dict(
                    list(content_dict.items()) + list(json.load(f).items())
                )
        except FileNotFoundError as e:
            print(f"No data to merge from {str(outfile)}")
        finally:
            with open(str(outfile), "w") as f:
                json.dump(content_dict, f)

    print("\t...Done")
    return content_dict


def RSS_feed(url: str, outfile: Path = None):
    """
    Get the RSS feed from the given URL.
    """

    response = requests.get(url)

    # entire feed
    root = etree.fromstring(response.text)
    item = root.findall("channel/item")

    feed = []
    for entry in item:
        e = {}

        e["title"] = entry.findtext("title")
        e["link"] = entry.findtext("link")
        e["pubdate"] = entry.findtext("pubDate")

        feed.append(e)

    new_feed = [f for f in feed]

    if outfile:
        try:
            with open(str(outfile), "r") as f:
                feed.extend(json.load(f))
        except FileNotFoundError as e:
            print(f"No data to merge from {str(outfile)}")
        finally:
            with open(str(outfile), "w") as f:
                json.dump(feed, f)

    return feed, new_feed


if __name__ == "__main__":

    folder = Path(".")
    if len(sys.argv) == 2:
        folder = Path(sys.argv[1])

    # DAILY MAIL
    _, daily_feed = RSS_feed(
        "https://www.dailymail.co.uk/news/index.rss",
        outfile=folder.joinpath("items_dailymail.json"),
    )

    RSS_content(
        feed=daily_feed,
        outfile=folder.joinpath("content_daily.json"),
        tag="p",
        class_attr="mol-para-with-font",
    )

    # THE GUARDIAN
    _, guardian_feed = RSS_feed(
        "https://www.theguardian.com/international/rss",
        outfile=folder.joinpath("items_guardian.json"),
    )
    RSS_content(
        feed=guardian_feed,
        outfile=folder.joinpath("content_guardain.json"),
        tag="p",
        class_attr="dcr-xry7m2",
    )

    # HUFFINGTONPOST
    _, huffpost_feed = RSS_feed(
        "https://www.huffingtonpost.co.uk/feeds/index.xml",
        outfile=folder.joinpath("items_huffpost.json"),
    )
    RSS_content(
        feed=huffpost_feed,
        outfile=folder.joinpath("content_huffpost.json"),
        tag="div",
        class_attr="primary-cli cli cli-text",
    )

    # REUTERS
    _, reuters_feed = RSS_feed(
        "https://www.reuters.com/news/rss/topnews",
        outfile=folder.joinpath("items_reuters.json"),
    )
    RSS_content(
        feed=reuters_feed,
        outfile=folder.joinpath("content_reuters.json"),
        tag="p",
        class_attr="StandardArticleBody_body_1",
    )


