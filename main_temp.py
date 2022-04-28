from file import File


def main():
    huff_scrap = File(
        "huffingtonpost.com", {"title": "css-title", "content": "content-tag"}
    )
    daily_mail_scrap = File(
        "huffingtonpost.com", {"title": "css-title", "content": "content-tag"}
    )

    json.dump(huff_scrap, open("huff_scrap.json", "w"))
    print(huff_scrap)
    pass


if __name__ == "__main__":
    main()
