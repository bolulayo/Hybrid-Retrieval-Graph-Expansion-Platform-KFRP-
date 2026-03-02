# Integration patterns used

## Idempotency keys
Ingestion endpoints accept an `idempotency_key` to protect against duplicate writes during retries.

## Outbox pattern
Write side records domain events in Postgres within the same transaction as state changes. A background dispatcher publishes events to a queue (Redis here for demo). This prevents "state written but event lost" failures.

## Contract-first APIs
Gateway and services use explicit request/response models (Pydantic) and keep JSON schemas in `/contracts/v1/`.

## Versioning
Public API is versioned under `/v1/*`. Internal services can evolve independently behind the gateway.
