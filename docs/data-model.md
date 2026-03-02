# Data model

## Canonical domain model (Postgres)
- **Document**: a normalized document representing a source record or collection of chunks.
- **Chunk**: text chunk with embedding + metadata.
- **Entity**: extracted entity (normalized string + type).
- **Relation**: relationship between entities with confidence + provenance.
- **SourceRecord**: original identifiers and raw source metadata.
- **NormalizedField**: field-level normalization outputs (e.g., dates, names, addresses).

## Graph model (Neo4j)
Nodes:
- `(:Entity {id, name, type})`
- `(:Document {id, source, title})`

Edges:
- `(Entity)-[:RELATION {type, confidence}]->(Entity)`
- `(Document)-[:MENTIONS]->(Entity)`
- `(Entity)-[:EVIDENCED_BY]->(Document)`

## Why split stores?
- Postgres excels at transactional write integrity, FTS, and embeddings with pgvector.
- Neo4j provides expressive graph traversals for expansion and provenance.
