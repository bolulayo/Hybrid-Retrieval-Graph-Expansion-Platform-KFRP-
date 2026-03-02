from app.shared.embedding import toy_embed

def test_toy_embed_deterministic():
    a = toy_embed("hello")
    b = toy_embed("hello")
    assert a == b
    assert len(a) == 8
