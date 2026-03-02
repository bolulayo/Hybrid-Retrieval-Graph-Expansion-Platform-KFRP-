from app.normalization.normalize import normalize_whitespace, chunk_text, simple_entity_extract

def test_normalize_whitespace():
    assert normalize_whitespace("a   b\n c") == "a b c"

def test_chunk_text():
    chunks = chunk_text("x" * 1000, max_len=200)
    assert len(chunks) == 5

def test_entity_extract():
    ents = simple_entity_extract("Alice met Bob at Acme Corp in Dallas.")
    assert any(e.name == "Alice" for e in ents)
