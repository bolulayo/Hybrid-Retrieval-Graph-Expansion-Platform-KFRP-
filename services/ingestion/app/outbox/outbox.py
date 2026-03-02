import json
import uuid
from datetime import datetime, timezone
from sqlalchemy import text

def record_event(db, aggregate_type: str, aggregate_id, event_type: str, payload: dict):
    event_id = uuid.uuid4()
    db.execute(
        text("""
            INSERT INTO outbox_events (id, aggregate_type, aggregate_id, event_type, payload)
            VALUES (:id, :atype, :aid, :etype, CAST(:payload AS jsonb))
        """),
        {
            "id": str(event_id),
            "atype": aggregate_type,
            "aid": str(aggregate_id),
            "etype": event_type,
            "payload": json.dumps(payload),
        },
    )
    return event_id

def mark_published(db, event_id):
    db.execute(
        text("""UPDATE outbox_events SET published_at = :ts WHERE id = :id"""),
        {"ts": datetime.now(timezone.utc), "id": str(event_id)},
    )