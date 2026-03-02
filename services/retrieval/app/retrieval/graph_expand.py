from neo4j import GraphDatabase

CYPHER = """
MATCH (d:Document {id:$doc_id})-[:MENTIONS]->(e:Entity)
OPTIONAL MATCH (e)-[r:RELATION]->(e2:Entity)
RETURN e.id AS entity_id, e.name AS entity_name, e.type AS entity_type,
       collect(DISTINCT {to_id: e2.id, to_name: e2.name, rel_type: r.type, confidence: r.confidence}) AS related
"""

def expand_via_graph(uri: str, user: str, password: str, doc_id: str):
    driver = GraphDatabase.driver(uri, auth=(user, password))
    with driver.session() as session:
        res = session.run(CYPHER, doc_id=doc_id).data()
    driver.close()
    # Normalize empty related entries
    for row in res:
        row["related"] = [x for x in row.get("related", []) if x.get("to_id")]
    return res
