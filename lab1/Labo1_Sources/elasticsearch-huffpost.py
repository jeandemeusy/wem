import json
from datetime import datetime
from pathlib import Path
from pprint import pprint

from elasticsearch_dsl import Document, Date, Integer, Keyword, Text, connections

# Define a default Elasticsearch client
connections.create_connection(hosts=['localhost'])

file = Path("../../lab1/crawler/quotes.json")

with open(file, "r") as f:
    page_scrawler = json.load(f)


class Article(Document):
    title = Text(analyzer='snowball', fields={'raw': Keyword()})
    description = Text(analyzer='snowball')
    author = Text(analyzer='snowball')
    tag = Keyword()

    class Index:
        name = 'huffpost'
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(Article, self).save(**kwargs)


# create the mappings in elasticsearch
Article.init()

# # create and save and article
for index, page in enumerate(page_scrawler):
    article = Article(meta={'id': index}, title=page["title"], description=page["description"], author=page["author"])
    article.save()

article = Article.get(id=6)
print(article.title)

# Display cluster health
pprint(connections.get_connection().cluster.health())
