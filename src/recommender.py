import logging
import os
from typing import Dict, List, Tuple
from dataclasses import dataclass, field, asdict

from dotenv import load_dotenv
from google import genai
from google.genai import errors as genai_errors

from src.mbti_traits import build_query_text
from src.retriever import SongRetriever, load_mbti_songs

load_dotenv()

logger = logging.getLogger(__name__)

GENERATION_MODEL_NAME = "gemini-flash-latest"


def _resolve_api_key(api_key: str = None) -> str:
    """Returns the Gemini API key to use, raising a clear, actionable error
    instead of a bare KeyError if none is configured. Only generation needs
    this now — retrieval runs on a local sentence-transformers model."""
    api_key = api_key or os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not set. Create a .env file in the project "
            "root with GEMINI_API_KEY=your-key-here (see .env.example), or "
            "get a free-tier key at https://aistudio.google.com/apikey."
        )
    return api_key

# Added to a song's cosine similarity score when ranking, if its own
# mbti_type exactly matches the queried type. Cosine similarity is bounded
# in [-1, 1], so this is a soft weight, not a hard guarantee: a strong
# enough semantic match from a *different* type can still outrank a weak
# same-type match, the same way GENRE_MATCH_POINTS/MOOD_MATCH_POINTS used
# to nudge (not force) the old scoring recommender's ranking.
EXACT_TYPE_MATCH_BONUS = 0.5

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    mbti_type: str
    traits: List[str] = field(default_factory=list)
    description: str = ""

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    mbti_type: str

class Recommender:
    """
    OOP implementation of the recommendation logic, backed by
    SongRetriever's RAG-style embedding retrieval (see src/retriever.py).
    """
    def __init__(self, songs: List[Song], api_key: str = None):
        self.songs = songs
        self.retriever = SongRetriever([asdict(song) for song in songs])
        self.client = genai.Client(api_key=_resolve_api_key(api_key))
        self._results_cache = {}

    def _retrieve_all(self, mbti_type: str) -> List[Tuple[Dict, float]]:
        """Returns every song ranked against an MBTI type's query text,
        cached per type so recommend() and explain_recommendation() share
        one retrieval instead of each re-embedding the query and
        re-scoring the whole catalog.

        SongRetriever.retrieve() is type-blind: it ranks purely by semantic
        similarity, so a song labeled for a different MBTI type can
        outrank an exact match if its text happens to embed closer to the
        query. EXACT_TYPE_MATCH_BONUS re-ranks by score plus that bonus for
        exact matches, so the queried type is favored without discarding
        semantic similarity as the underlying signal. The cached (and
        returned) scores stay the raw similarity, so explain_recommendation
        still reports the true semantic score, not the boosted one."""
        if mbti_type not in self._results_cache:
            query_text = build_query_text(mbti_type)
            results = self.retriever.retrieve(query_text, k=len(self.songs))
            results.sort(
                key=lambda pair: pair[1] + (EXACT_TYPE_MATCH_BONUS if pair[0]["mbti_type"] == mbti_type else 0.0),
                reverse=True,
            )
            self._results_cache[mbti_type] = results
        return self._results_cache[mbti_type]

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        results = self._retrieve_all(user.mbti_type)[:k]
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[song_dict["id"]] for song_dict, _score in results]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        scores_by_id = {song_dict["id"]: score for song_dict, score in self._retrieve_all(user.mbti_type)}
        return f"semantic similarity to {user.mbti_type} traits: {scores_by_id[song.id]:.2f}"

    def generate_recommendation_summary(self, user: UserProfile, songs: List[Song]) -> str:
        """Uses Gemini to write a personalized recommendation summary that is
        grounded strictly in the given (already-retrieved) songs — the
        prompt explicitly forbids referencing any song outside this list,
        so the response can't hallucinate titles/artists that were never
        retrieved. Falls back to a plain, non-generated summary if the
        Gemini call fails, so a live API error never crashes the CLI."""
        song_context = "\n".join(
            f'- "{song.title}" by {song.artist} (MBTI type: {song.mbti_type}, '
            f'traits: {", ".join(song.traits)}): {song.description}'
            for song in songs
        )
        prompt = (
            f"A listener has the MBTI personality type {user.mbti_type}. "
            f"Here are songs retrieved for them, each with its trait tags and description:\n\n"
            f"{song_context}\n\n"
            f"Write a short (3-5 sentence) personalized recommendation summary explaining "
            f"why these songs fit a {user.mbti_type} listener. "
            f"Only reference the songs listed above by title and artist — do not mention, "
            f"imply, or invent any other song, artist, or album."
        )
        try:
            response = self.client.models.generate_content(
                model=GENERATION_MODEL_NAME, contents=prompt
            )
            return response.text.strip()
        except genai_errors.APIError:
            logger.exception("Gemini generation failed; falling back to a plain summary")
            titles = ", ".join(f'"{song.title}" by {song.artist}' for song in songs)
            return f"Recommended for {user.mbti_type}: {titles}."

def load_songs(csv_path: str) -> List[Song]:
    """Loads songs from an MBTI song catalog CSV (see retriever.load_mbti_songs)
    into Song dataclass instances."""
    rows = load_mbti_songs(csv_path)
    return [
        Song(
            id=row["id"],
            title=row["title"],
            artist=row["artist"],
            mbti_type=row["mbti_type"],
            traits=row["traits"],
            description=row["description"],
        )
        for row in rows
    ]
