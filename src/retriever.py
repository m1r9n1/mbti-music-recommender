"""Embedding-based retrieval over the MBTI song catalog (data/mbti_songs.csv).

Embeddings come from a local sentence-transformers model, so retrieval
runs offline with no API key and no rate limits."""

import csv
import logging
from typing import Dict, List, Tuple

import numpy as np
from sentence_transformers import SentenceTransformer

logger = logging.getLogger(__name__)

DEFAULT_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
REQUIRED_COLUMNS = {"id", "title", "artist", "traits", "description"}


def load_mbti_songs(csv_path: str) -> List[Dict]:
    """Loads the MBTI song catalog. Each row's `traits` field is
    pipe-separated as MBTI_TYPE|trait1|trait2|..., which this splits into
    `mbti_type` and a `traits` list."""
    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = REQUIRED_COLUMNS - set(reader.fieldnames or [])
        if missing:
            raise ValueError(
                f"{csv_path} is missing required column(s): {', '.join(sorted(missing))}"
            )
        for row in reader:
            row["id"] = int(row["id"])
            parts = row["traits"].split("|")
            row["mbti_type"] = parts[0]
            row["traits"] = parts[1:]
            songs.append(row)

    if not songs:
        raise ValueError(f"{csv_path} contains no songs")

    logger.info("Loaded %d songs from %s", len(songs), csv_path)
    return songs


def _embedding_text(song: Dict) -> str:
    """Builds the text used for embedding a song: its trait tags plus description."""
    return ", ".join(song["traits"]) + ". " + song["description"]


class SongRetriever:
    """Embeds songs' trait tags/descriptions via a local sentence-transformers
    model and retrieves nearest matches for a query string via cosine
    similarity."""

    def __init__(self, songs: List[Dict], model_name: str = DEFAULT_MODEL_NAME):
        if not songs:
            raise ValueError("SongRetriever requires a non-empty song list")
        self.songs = songs
        self.model_name = model_name
        logger.info("Loading embedding model %s", model_name)
        self.model = SentenceTransformer(model_name)
        texts = [_embedding_text(song) for song in songs]
        self.embeddings = self._embed(texts)
        logger.info("Embedded %d songs", len(songs))

    def _embed(self, texts: List[str]) -> np.ndarray:
        """Embeds a batch of texts locally and normalizes each vector so
        cosine similarity is a plain dot product."""
        return self.model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)

    def retrieve(self, query_text: str, k: int = 5) -> List[Tuple[Dict, float]]:
        """Returns the top-k (song, similarity_score) pairs for a query string."""
        query_embedding = self._embed([query_text])[0]
        scores = self.embeddings @ query_embedding
        top_indices = np.argsort(-scores)[:k]
        return [(self.songs[i], float(scores[i])) for i in top_indices]
