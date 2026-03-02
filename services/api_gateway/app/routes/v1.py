import os
import httpx
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional

INGESTION_URL = os.getenv("INGESTION_URL", "http://localhost:8001")
RETRIEVAL_URL = os.getenv("RETRIEVAL_URL", "http://localhost:8002")

router = APIRouter()

class IngestDocument(BaseModel):
    external_id: str
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class IngestRequest(BaseModel):
    idempotency_key: str = Field(..., description="Used to safely retry without duplicates")
    source: str
    document: IngestDocument

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    expand_graph: bool = True
    filters: Optional[Dict[str, Any]] = None

@router.post("/ingest")
async def ingest(req: IngestRequest):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{INGESTION_URL}/ingest", json=req.model_dump())
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()

@router.post("/query")
async def query(req: QueryRequest):
    async with httpx.AsyncClient(timeout=30) as client:
        r = await client.post(f"{RETRIEVAL_URL}/query", json=req.model_dump())
    if r.status_code >= 400:
        raise HTTPException(status_code=r.status_code, detail=r.text)
    return r.json()
