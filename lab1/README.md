# Labo #1

Membres du groupe:

- Maxime Clercq
- Jean Demeusy 
- Guillaume Riondet

## Fichiers utiles

- `crawler.py`: pour crawler la page "News" du HuffingtonPost,
- `indexer.py`: pour indexer les résultats du crawler avec ElasticSearch DSL,
- le module `queries` pour faire des requetes sur les données indexées.

## Condition préalables

Il faut que le container docker fourni pour la labo tourne. Pour cela:
```bash
> cd Labo1_Sources
> docker compose up
> cd ..
```

## Crawler

Le crawler s'exécute comme cela:
```python
> scrapy runspider crawler.py
```

Pour enregistrer les résultats du crawler:
```python
> scrapy runspider crawler.py -O quotes.json
```

Tout les objets retenus lors du crawling sont stockés dans le fichier `quotes.json`, que l'indexer utilise comme source de données.

## Indexer

L'indexer s'exécute ainsi:
```bash
> python indexer.py
```

Cet indexer prend la liste d'objets du fichier `quotes.json`, et les ajoute à l'index de l'instance d'ElasticSearch (Docker).

# Requêtes

Effectuer une requête sur l'index d'ElasticSearch se fait comme ceci:
```bash
> python -m queries --field <field> --text <text>
```

où:
- `field` est le champ sur lequel on souhaite faire la requête. Dans notre cas il peut être "title", "description" ou "author",
- `text` est la chaine de caractère que l'on recherche.

Voici quelques exemples de requêtes:
```bash
> python -m queries --field title --text "tyranny expert"
> python -m queries --field description --text "russia"
> python -m queries --field author --text "sara boboltz"
```