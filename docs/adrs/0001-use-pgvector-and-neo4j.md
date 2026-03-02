# ADR 0001: Use Postgres (pgvector + FTS) and Neo4j for retrieval

Date: 2026-02-24

## Context
We need hybrid retrieval (keyword + semantic) and relationship reasoning.

## Decision
- Store chunks + embeddings + FTS in Postgres (pgvector + tsvector).
- Store entity graph + provenance in Neo4j.

## Alternatives considered
- All-in-one vector DB with graph features (rejected: limited graph traversal for our needs).
- Pure graph retrieval (rejected: weak text ranking without additional indexing).
- Elasticsearch + Neo4j (rejected for demo: heavier ops and extra moving parts).

## Consequences
- Two stores increase operational complexity but allow best-of-breed retrieval + graph expansion.
