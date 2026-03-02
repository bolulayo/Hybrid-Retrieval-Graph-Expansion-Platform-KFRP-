import os
from neo4j import GraphDatabase

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))

def upsert_document(tx, doc_id: str, source: str, title: str):
    tx.run(
        """MERGE (d:Document {id: $id})
           SET d.source=$source, d.title=$title
        """,
        id=doc_id, source=source, title=title
    )

def upsert_entity(tx, ent_id: str, name: str, etype: str):
    tx.run(
        """MERGE (e:Entity {id: $id})
           SET e.name=$name, e.type=$type
        """,
        id=ent_id, name=name, type=etype
    )

def link_mentions(tx, doc_id: str, ent_id: str):
    tx.run(
        """MATCH (d:Document {id:$doc_id}), (e:Entity {id:$ent_id})
           MERGE (d)-[:MENTIONS]->(e)
           MERGE (e)-[:EVIDENCED_BY]->(d)
        """,
        doc_id=doc_id, ent_id=ent_id
    )
