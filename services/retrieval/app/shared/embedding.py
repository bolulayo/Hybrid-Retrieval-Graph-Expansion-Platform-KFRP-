import hashlib
from typing import List

def toy_embed(text: str, dim: int = 8) -> List[float]:
    """Deterministic toy embedding for demo (no external model).
    Converts text -> dim floats in [0,1). Replace with real embeddings in production.
    """
    h = hashlib.sha256(text.encode("utf-8")).digest()
    vals = []
    for i in range(dim):
        # take 4 bytes -> int
        chunk = h[i*4:(i+1)*4]
        n = int.from_bytes(chunk, "big")
        vals.append((n % 10_000) / 10_000.0)
    return vals
