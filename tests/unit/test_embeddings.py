import math

from morning_paper.embeddings import cosine_similarity, max_similarity
from morning_paper.embeddings.embedder import VoyageEmbedder, get_embedder


def test_cosine_identical_is_one():
    assert math.isclose(cosine_similarity([1.0, 2.0, 3.0], [1.0, 2.0, 3.0]), 1.0)


def test_cosine_orthogonal_is_zero():
    assert math.isclose(cosine_similarity([1.0, 0.0], [0.0, 1.0]), 0.0)


def test_cosine_opposite_is_minus_one():
    assert math.isclose(cosine_similarity([1.0, 0.0], [-1.0, 0.0]), -1.0)


def test_cosine_empty_or_zero_is_zero():
    assert cosine_similarity([], [1.0]) == 0.0
    assert cosine_similarity([0.0, 0.0], [1.0, 1.0]) == 0.0


def test_max_similarity_picks_best_reference():
    v = [1.0, 0.0]
    refs = [[0.0, 1.0], [1.0, 0.0]]
    assert math.isclose(max_similarity(v, refs), 1.0)


def test_max_similarity_no_refs_is_zero():
    assert max_similarity([1.0, 0.0], []) == 0.0


class _FakeVoyage:
    def embed(self, texts, *, model="m"):
        return [[float(len(t))] for t in texts]


def test_voyage_embedder_delegates():
    emb = VoyageEmbedder(_FakeVoyage(), model="m")
    assert emb.embed(["a", "bb"]) == [[1.0], [2.0]]
    assert emb.embed([]) == []


def test_get_embedder_none_without_key(monkeypatch):
    import morning_paper.config as config

    class _S:
        class secrets:
            voyage_api_key = None

        class file:
            class embeddings:
                provider = "voyage"
                model = "voyage-3.5"

    monkeypatch.setattr(config, "get_settings", lambda: _S())
    assert get_embedder() is None
