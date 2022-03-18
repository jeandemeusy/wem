import click
from elasticsearch import Elasticsearch
from elasticsearch_dsl import Search, connections


@click.command()
@click.option("-f", "--field", help="field to make a query on", type=str, required=True)
@click.option("-t", "--text", help="text to query", type=str, required=True)
def query(field: str, text: str):

    client = Elasticsearch()

    s: Search = Search(using=client, index="huffpost")

    if field == "title":
        s = s.query("match", title=text)
    elif field == "description":
        s = s.query("match", description=text)
    elif field == "author":
        s = s.query("match", author=text)
    else:
        print(f"Unknown query field '{field}'")
        return

    s.aggs.bucket("per_tag", "terms", field="tags")

    response = s.execute()

    for hit in response:
        print(f"{hit.meta.score:.2f}", hit.title)


if __name__ == "__main__":
    connections.create_connection(hosts=["localhost"])
    query()
