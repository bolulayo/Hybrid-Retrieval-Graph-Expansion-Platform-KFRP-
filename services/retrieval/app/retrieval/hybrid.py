from sqlalchemy import text
from ..shared.embedding import toy_embed

def to_pgvector(vec):
    # pgvector accepts: '[0.1,0.2,0.3]'
    return "[" + ",".join(f"{float(x):.4f}" for x in vec) + "]"

def hybrid_search(db, query: str, top_k: int = 5):
    """Hybrid retrieval: combine FTS rank + vector similarity (toy embedding) in Postgres."""
    q_emb = to_pgvector(toy_embed(query))

    rows = db.execute(
        text("""
            WITH candidates AS (
              SELECT
                c.id,
                c.document_id,
                c.chunk_index,
                c.content,
                ts_rank(c.tsv, plainto_tsquery('english', :q)) AS fts_rank,
                (c.embedding <-> (:q_emb)::vector) AS vec_dist
              FROM chunks c
              WHERE c.tsv @@ plainto_tsquery('english', :q)
              ORDER BY fts_rank DESC
              LIMIT 50
            )
            SELECT
              id, document_id, chunk_index, content,
              fts_rank,
              vec_dist,
              (fts_rank * 0.7) + ((1.0 - LEAST(vec_dist, 1.0)) * 0.3) AS score
            FROM candidates
            ORDER BY score DESC
            LIMIT :k
        """),
        {"q": query, "q_emb": q_emb, "k": top_k},
    ).mappings().all()

    if not rows:
        rows = db.execute(
            text("""
                SELECT id, document_id, chunk_index, content,
                       0.0 AS fts_rank,
                       (embedding <-> (:q_emb)::vector) AS vec_dist,
                       (1.0 - LEAST((embedding <-> (:q_emb)::vector), 1.0)) AS score
                FROM chunks
                ORDER BY vec_dist ASC
                LIMIT :k
            """),
            {"q_emb": q_emb, "k": top_k},
        ).mappings().all()

    return [dict(r) for r in rows]