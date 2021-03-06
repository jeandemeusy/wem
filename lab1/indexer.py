import json
from pathlib import Path
from pprint import pprint

from elasticsearch_dsl import connections
from queries.article import Article

# Define a default Elasticsearch client
connections.create_connection(hosts=["localhost"])

file = Path("quotes.json")

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
