# Architecture

## Problem statement
Build a retrieval platform that can ingest heterogeneous source records, normalize them into a canonical domain model, store rich relationships in a GraphDB, and serve low-latency hybrid retrieval via a stable API surface.

## Constraints & assumptions
- Demo-friendly: runnable locally via Docker Compose.
- Explicit boundaries: gateway, ingestion/normalization, retrieval.
- Reliability: safe retries, idempotency, and event recording.
- Observability: structured logs + request IDs.

## Components
- **API Gateway**: versioned endpoints, validation, fanout to internal services.
- **Ingestion**: accepts documents, normalizes, writes to Postgres + Neo4j, records events via outbox.
- **Retrieval**: hybrid retrieval (FTS + vector similarity), optional graph expansion to enrich context.
- **Stores**:
  - Postgres + pgvector: text chunks, embeddings, FTS index.
  - Neo4j: entities, relations, provenance edges.

## Why this architecture?
- Enables clear discussion of tradeoffs without being over-engineered.
- Mirrors real-world patterns (source systems → canonical model → multiple stores).
- Demonstrates retrieval + graph reasoning foundations.
