import json
from datetime import datetime
from pathlib import Path
from pprint import pprint

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections

import click
from article import Article

# Define a default Elasticsearch client
@click.command()
@click.option("-f", "--field", help="field to make a query on")
def query(field):

    article = Article.get(id=6)
    print(article.title)


if __name__ == "__main__":
    connections.create_connection(hosts=["localhost"])
    query()
