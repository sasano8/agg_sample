from neo4j import GraphDatabase
from py2neo import Graph


def commit(tx):
    return tx.commit()

def init(tx):
    # ユニーク制約
    query = "CREATE CONSTRAINT unique_model_id ON (x:Model) ASSERT x.id IS UNIQUE"
    tx.append(query)

def delete_all(tx):
    delete_models(tx)

def add_models(tx, models):
    for model in models:
        tx.append("CREATE (person:Model name: $name) RETURN person", name=model["id"])

def delete_models(tx):
    query = """MATCH (n)
    DETACH DELETE n
    """
    tx.append(query)


# neo4j 単体のアダプタの使用は面倒なのでラッパー（py2neo）を使用
graph = Graph()

with graph.begin() as tx:
    add_models(tx, ["Alice", "Bob", "Carol"])
