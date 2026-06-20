from morning_paper.profile.builder import _build_interest_vectors


class _FakeEmbedder:
    def __init__(self):
        self.seen = None

    def embed(self, texts):
        self.seen = list(texts)
        return [[float(i)] for i, _ in enumerate(texts)]


def test_no_embedder_returns_empty():
    assert _build_interest_vectors({"a/b": 1.0}, {"E": 1.0}, None) == []


def test_embeds_top_phrases_topics_and_entities():
    emb = _FakeEmbedder()
    vecs = _build_interest_vectors(
        {"технологии/ИИ": 0.9, "спорт/велоспорт": 0.2},
        {"Anthropic": 0.8},
        emb,
    )
    # Topic paths flattened ("/" -> " "), entities appended; vector per phrase.
    assert emb.seen == ["технологии ИИ", "спорт велоспорт", "Anthropic"]
    assert len(vecs) == 3


def test_caps_phrase_count():
    emb = _FakeEmbedder()
    topics = {f"t/{i}": float(i) for i in range(20)}
    _build_interest_vectors(topics, {}, emb, max_phrases=5)
    assert len(emb.seen) == 5


def test_embedder_failure_returns_empty():
    class _Boom:
        def embed(self, texts):
            raise RuntimeError("down")

    assert _build_interest_vectors({"a/b": 1.0}, {}, _Boom()) == []
