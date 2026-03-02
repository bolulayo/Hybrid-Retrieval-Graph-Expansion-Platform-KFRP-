import re
from dataclasses import dataclass
from typing import Dict, List, Tuple

@dataclass
class NormalizedEntity:
    name: str
    type: str

def normalize_whitespace(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()

def simple_entity_extract(text: str) -> List[NormalizedEntity]:
    """Toy entity extractor for demo.
    Extracts capitalized words as ORG/PERSON heuristics.
    Replace with a real NER model in production.
    """
    ents = []
    for m in re.finditer(r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)\b", text):
        val = normalize_whitespace(m.group(1))
        if len(val) >= 3:
            etype = "ORG" if "Inc" in val or "Corp" in val else "PERSON"
            ents.append(NormalizedEntity(name=val, type=etype))
    # de-dupe while preserving order
    seen = set()
    out = []
    for e in ents:
        k = (e.name.lower(), e.type)
        if k not in seen:
            seen.add(k)
            out.append(e)
    return out

def chunk_text(text: str, max_len: int = 450) -> List[str]:
    text = normalize_whitespace(text)
    if len(text) <= max_len:
        return [text]
    chunks = []
    start = 0
    while start < len(text):
        end = min(len(text), start + max_len)
        chunks.append(text[start:end])
        start = end
    return chunks
