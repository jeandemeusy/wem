from elasticsearch_dsl import Document, Keyword, Text


class Article(Document):
    title = Text(analyzer="snowball", fields={"raw": Keyword()})
    description = Text(analyzer="snowball")
    author = Text(analyzer="snowball")
    tag = Keyword()

    class Index:
        name = "huffpost"
        settings = {
            "number_of_shards": 2,
        }

    def save(self, **kwargs):
        return super(Article, self).save(**kwargs)
