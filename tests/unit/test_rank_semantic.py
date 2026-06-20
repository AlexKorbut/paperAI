"""Semantic + keyword ranking. Uses a deterministic fake embedder (no network)."""

from morning_paper.models import InterestProfile
from morning_paper.retrieval.feeds import Candidate
from morning_paper.retrieval.rank import rank_candidates


def _c(id: str, title: str, body: str = "") -> Candidate:
    return Candidate(id=id, title=title, body=body, url="", lang="en", source="t", published_at="")


class _KeywordEmbedder:
    """Maps text to a 2D vector by presence of two marker words, so cosine
    similarity to a known interest vector is fully deterministic."""

    def embed(self, texts):
        out = []
        for t in texts:
            low = t.lower()
            out.append([1.0 if "rocket" in low else 0.0, 1.0 if "market" in low else 0.0])
        return out


def test_semantic_ranks_by_interest_vector_when_keywords_absent():
    # Profile has NO topic/entity keyword overlap with the candidates, only an
    # interest vector pointing at the "rocket" axis. Semantic ranking must still
    # float the space story to the top.
    profile = InterestProfile(user_id="u", topics={}, entities={}, interest_vectors=[[1.0, 0.0]])
    space = _c("space", "A rocket launch from the coast")
    money = _c("money", "Stock market closes higher")

    ranked = rank_candidates(
        [money, space], profile, embedder=_KeywordEmbedder(), semantic_weight=1.0
    )
    assert ranked[0].id == "space"
    assert ranked[0].score > ranked[1].score


def test_keyword_only_without_embedder():
    profile = InterestProfile(user_id="u", topics={"market": 1.0}, entities={})
    space = _c("space", "A rocket launch")
    money = _c("money", "Stock market news")
    ranked = rank_candidates([space, money], profile, embedder=None)
    assert ranked[0].id == "money"


def test_no_interest_vectors_falls_back_to_keywords():
    # Embedder present but profile has no vectors -> semantic disabled, keywords win.
    profile = InterestProfile(user_id="u", topics={"market": 1.0}, entities={}, interest_vectors=[])
    space = _c("space", "A rocket launch")
    money = _c("money", "Stock market news")
    ranked = rank_candidates(
        [space, money], profile, embedder=_KeywordEmbedder(), semantic_weight=1.0
    )
    assert ranked[0].id == "money"


def test_embedder_failure_degrades_gracefully():
    class _Boom:
        def embed(self, texts):
            raise RuntimeError("embedding service down")

    profile = InterestProfile(user_id="u", topics={"market": 1.0}, entities={}, interest_vectors=[[1.0, 0.0]])
    space = _c("space", "A rocket launch")
    money = _c("money", "Stock market news")
    ranked = rank_candidates([space, money], profile, embedder=_Boom(), semantic_weight=1.0)
    # Falls back to keyword scoring (semantic_weight effectively 0).
    assert ranked[0].id == "money"


def test_top_n_limit():
    profile = InterestProfile(user_id="u", topics={}, entities={})
    cands = [_c(str(i), f"headline {i}") for i in range(10)]
    assert len(rank_candidates(cands, profile, top_n=3)) == 3
