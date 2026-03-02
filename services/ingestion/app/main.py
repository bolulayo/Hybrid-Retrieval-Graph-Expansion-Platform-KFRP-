import uuid
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Any, Dict, Optional
from sqlalchemy import text
from .db import SessionLocal
from .shared.embedding import toy_embed
from .normalization.normalize import chunk_text, simple_entity_extract
from .outbox.outbox import record_event
from .graph import driver, upsert_document, upsert_entity, link_mentions

app = FastAPI(title="KFRP Ingestion Service", version="1.0.0")

class IngestDocument(BaseModel):
    external_id: str
    title: str
    content: str
    metadata: Optional[Dict[str, Any]] = None

class IngestRequest(BaseModel):
    idempotency_key: str = Field(..., description="Used to safely retry without duplicates")
    source: str
    document: IngestDocument

@app.post("/ingest")
def ingest(req: IngestRequest):
    # Idempotency demo: if same (source, external_id) exists, return existing document id
    db = SessionLocal()
    try:
        row = db.execute(
            text("""SELECT id FROM documents WHERE source=:s AND external_id=:e"""),
            {"s": req.source, "e": req.document.external_id},
        ).fetchone()
        if row:
            return {"status": "ok", "document_id": str(row[0]), "idempotent": True}

        doc_id = uuid.uuid4()
        db.execute(
            text("""
                INSERT INTO documents (id, source, external_id, title)
                VALUES (:id, :s, :e, :t)
            """),
            {"id": str(doc_id), "s": req.source, "e": req.document.external_id, "t": req.document.title},
        )

        chunks = chunk_text(req.document.content)
        for i, c in enumerate(chunks):
            emb = toy_embed(c)
            chunk_id = uuid.uuid4()
            db.execute(
                text("""
                    INSERT INTO chunks (id, document_id, chunk_index, content, embedding)
                    VALUES (:id, :doc, :idx, :content, :embedding)
                """),
                {"id": str(chunk_id), "doc": str(doc_id), "idx": i, "content": c, "embedding": emb},
            )

        # Graph upsert: Document + Entities + Mentions
        entities = simple_entity_extract(req.document.content)
        with driver.session() as session:
            session.execute_write(upsert_document, str(doc_id), req.source, req.document.title)
            for e in entities:
                ent_id = str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{e.type}:{e.name.lower()}"))
                session.execute_write(upsert_entity, ent_id, e.name, e.type)
                session.execute_write(link_mentions, str(doc_id), ent_id)

        # Outbox event
        record_event(db, "Document", doc_id, "DocumentIngested", {
            "document_id": str(doc_id),
            "source": req.source,
            "external_id": req.document.external_id,
            "title": req.document.title,
            "entity_count": len(entities),
            "chunk_count": len(chunks),
        })

        db.commit()
        return {"status": "ok", "document_id": str(doc_id), "idempotent": False, "entity_count": len(entities), "chunk_count": len(chunks)}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        db.close()
