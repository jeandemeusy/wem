import json
from pathlib import Path
from pprint import pprint

from elasticsearch_dsl import connections
from queries.article import Article

# Define a default Elasticsearch client
connections.create_connection(hosts=["localhost"])

<<<<<<< HEAD:lab1/indexer.py
file = Path("quotes.json")
=======
file = Path("../crawler/quotes.json")
>>>>>>> 10bbdbc5e4201ef0d75a6abb6686a80771415316:lab1/elasticsearch/elasticsearch-huffpost-indexer.py

with open(file, "r") as f:
    page_scrawler = json.load(f)

# create the mappings in elasticsearch
Article.init()

# # create and save and article
for index, page in enumerate(page_scrawler):
    article = Article(
        meta={"id": index},
        title=page["title"],
        description=page["description"],
        author=page["author"],
    )
    article.save()

# Display cluster health
pprint(connections.get_connection().cluster.health())
