# ADR 0002: Service boundaries (Gateway, Ingestion, Retrieval)

Date: 2026-02-24

## Context
We want to show clear architectural thinking without creating an over-complicated microservice mesh.

## Decision
Create three small services:
- Gateway: stable API + versioning + routing
- Ingestion: normalization + write-side integrity + outbox
- Retrieval: read-side optimization + graph expansion

## Consequences
- Easy to demo end-to-end locally.
- Clear interview narrative around boundaries and tradeoffs.
