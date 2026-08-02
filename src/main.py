"""
Command line runner for the MBTI Music Recommender.

Loads the song catalog, retrieves semantically-matching songs for the
user's MBTI type (src/retriever.py), re-ranks and summarizes them via
Gemini (src/recommender.py), and prints the results.
"""

import logging
import sys

from src.mbti_traits import MBTI_TRAIT_KEYWORDS
from src.recommender import load_songs, Recommender, UserProfile

logger = logging.getLogger(__name__)

SONGS_CSV_PATH = "data/mbti_songs.csv"


def configure_logging() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        datefmt="%H:%M:%S",
    )


def prompt_for_mbti_type() -> str:
    mbti_type = input("Enter your MBTI type (e.g. INFP): ").strip().upper()
    while mbti_type not in MBTI_TRAIT_KEYWORDS:
        print(f"Unknown MBTI type: {mbti_type!r}. Valid types: {', '.join(sorted(MBTI_TRAIT_KEYWORDS))}")
        mbti_type = input("Enter your MBTI type (e.g. INFP): ").strip().upper()
    return mbti_type


def run() -> None:
    logger.info("Loading song catalog from %s", SONGS_CSV_PATH)
    songs = load_songs(SONGS_CSV_PATH)
    print(f"Loaded songs: {len(songs)}")

    mbti_type = prompt_for_mbti_type()
    user = UserProfile(mbti_type=mbti_type)

    logger.info("Building recommender (loading embedding model + Gemini client)")
    recommender = Recommender(songs)

    logger.info("Retrieving recommendations for %s", mbti_type)
    recommendations = recommender.recommend(user, k=5)

    logger.info("Generating summary via Gemini")
    summary = recommender.generate_recommendation_summary(user, recommendations)

    print(f"\nTop Recommendations for {mbti_type}")
    print("=" * 40)
    print(f"\n{summary}\n")
    for rank, song in enumerate(recommendations, start=1):
        explanation = recommender.explain_recommendation(user, song)
        print(f"\n{rank}. {song.title} by {song.artist}  [{explanation}]")
        print(f"     - MBTI type: {song.mbti_type}")
        print(f"     - {song.description}")


def main() -> None:
    configure_logging()
    try:
        run()
    except FileNotFoundError as e:
        logger.error("Could not find the song catalog: %s", e)
        print(
            f"\nError: could not find {SONGS_CSV_PATH!r}. "
            "Run this command from the project root so the data/ folder is reachable."
        )
        sys.exit(1)
    except RuntimeError as e:
        # Raised by Recommender._resolve_api_key when GEMINI_API_KEY is missing.
        logger.error("Configuration error: %s", e)
        print(f"\nError: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        print("\nCancelled.")
        sys.exit(130)


if __name__ == "__main__":
    main()
