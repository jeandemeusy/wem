import hashlib
import json
from bs4 import BeautifulSoup

import requests
import unidecode


def RSS_content(
    infile: str = None,
    outfile: str = None,
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
        r = requests.get(f["link"])
        soup = BeautifulSoup(r.text, "html.parser")

        texts = soup.find_all(tag, attrs={"class": class_attr})

        hashed = hashlib.sha224(f["link"].encode("utf-8")).hexdigest()

        decoded_texts = [unidecode.unidecode(t.text).replace('"', "'") for t in texts]
        content_dict[hashed] = " ".join(decoded_texts)

        print(f"{idx}/{len(feed)}", end="\r")

    if outfile:
        with open(outfile, "w+") as f:
            json.dump(content_dict, f)

    print("\t...Done")
    return content_dict


if __name__ == "__main__":
    daily_content = RSS_content(
        infile="items_dailymail.json",
        # outfile="content_daily.json",
        tag="p",
        class_attr="mol-para-with-font",
    )

    # THE GUARDIAN
    guardian_content = RSS_content(
        infile="items_guardian.json",
        # outfile="content_guardain.json",
        tag="p",
        class_attr="dcr-xry7m2",
    )

    # HUFFINGTONPOST
    huffpost_content = RSS_content(
        infile="items_huffpost.json",
        # outfile="content_huffpost.json",
        tag="div",
        class_attr="primary-cli cli cli-text",
    )

    print(f"{len(daily_content)} items in dailymail")
    print(f"{len(guardian_content)} items in guardian")
    print(f"{len(huffpost_content)} items in huffpost")
