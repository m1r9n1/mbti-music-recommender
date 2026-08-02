from src.retriever import load_mbti_songs, SongRetriever
from src.mbti_traits import build_query_text


def test_retrieve_returns_k_songs_sorted_by_score():
    """retrieve() returns exactly k songs, ordered from most to least similar."""
    songs = load_mbti_songs("data/mbti_songs.csv")
    retriever = SongRetriever(songs)

    results = retriever.retrieve(build_query_text("ESTP"), k=5)

    assert len(results) == 5
    scores = [score for _song, score in results]
    assert scores == sorted(scores, reverse=True)


def test_retrieve_surfaces_matching_type_in_top_results():
    """A song labeled for the queried MBTI type shows up in its own top results."""
    songs = load_mbti_songs("data/mbti_songs.csv")
    retriever = SongRetriever(songs)

    results = retriever.retrieve(build_query_text("ESTP"), k=5)

    assert any(song["mbti_type"] == "ESTP" for song, _score in results)
