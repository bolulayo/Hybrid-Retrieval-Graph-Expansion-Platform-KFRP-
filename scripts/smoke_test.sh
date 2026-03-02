#!/usr/bin/env bash
set -euo pipefail

curl -s -X POST http://localhost:8080/v1/ingest \
  -H "Content-Type: application/json" \
  -d @examples/requests/ingest.sample.json

echo ""

curl -s -X POST http://localhost:8080/v1/query \
  -H "Content-Type: application/json" \
  -d @examples/requests/query.sample.json

echo ""
