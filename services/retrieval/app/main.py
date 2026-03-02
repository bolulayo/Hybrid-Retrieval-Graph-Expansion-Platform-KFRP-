import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict, Optional
from .db import SessionLocal
from .retrieval.hybrid import hybrid_search
from .retrieval.graph_expand import expand_via_graph

NEO4J_URI = os.getenv("NEO4J_URI")
NEO4J_USER = os.getenv("NEO4J_USER")
NEO4J_PASSWORD = os.getenv("NEO4J_PASSWORD")

app = FastAPI(title="KFRP Retrieval Service", version="1.0.0")

class QueryRequest(BaseModel):
    query: str
    top_k: int = 5
    expand_graph: bool = True
    filters: Optional[Dict[str, Any]] = None

@app.post("/query")
def query(req: QueryRequest):
    db = SessionLocal()
    try:
        hits = hybrid_search(db, req.query, req.top_k)
        if req.expand_graph:
            for h in hits:
                h["graph"] = expand_via_graph(NEO4J_URI, NEO4J_USER, NEO4J_PASSWORD, str(h["document_id"]))
        return {"query": req.query, "top_k": req.top_k, "results": hits}
    finally:
        db.close()
