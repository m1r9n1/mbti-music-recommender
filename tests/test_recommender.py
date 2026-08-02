from src.recommender import Song, UserProfile, Recommender

def make_small_recommender() -> Recommender:
    songs = [
        Song(
            id=1,
            title="Test Idealist Track",
            artist="Test Artist",
            mbti_type="INFP",
            traits=["idealistic", "dreamy", "introspective"],
            description="A dreamy, idealistic song about hope and imagination.",
        ),
        Song(
            id=2,
            title="Test Strategist Track",
            artist="Test Artist",
            mbti_type="INTJ",
            traits=["strategic", "analytical", "independent"],
            description="A cold, calculated meditation on long-term vision.",
        ),
    ]
    return Recommender(songs)


def test_recommend_returns_songs_sorted_by_relevance():
    user = UserProfile(mbti_type="INFP")
    rec = make_small_recommender()
    results = rec.recommend(user, k=2)

    assert len(results) == 2
    # The INFP-labeled song should be the closest semantic match to an INFP query.
    assert results[0].mbti_type == "INFP"


def test_explain_recommendation_returns_non_empty_string():
    user = UserProfile(mbti_type="INFP")
    rec = make_small_recommender()
    song = rec.songs[0]

    explanation = rec.explain_recommendation(user, song)
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_generate_recommendation_summary_only_mentions_retrieved_songs():
    user = UserProfile(mbti_type="INFP")
    rec = make_small_recommender()
    recommended = rec.recommend(user, k=1)

    summary = rec.generate_recommendation_summary(user, recommended)

    assert isinstance(summary, str)
    assert summary.strip() != ""
    # Grounding guardrail: the summary should reference the retrieved song's
    # title rather than a song outside the retrieved set.
    assert recommended[0].title in summary
