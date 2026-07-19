"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

PROFILES = [
    (
        "Starter profile",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
            "target_tempo": 120,
            "favorite_valence": 0.8,
            "favorite_danceability": 0.7,
        },
    ),
    (
        "A: Pop/happy tie test (Sunrise City vs. Say So)",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
            "favorite_valence": 0.8,
            "favorite_danceability": 0.7,
        },
    ),
    (
        "B: Rock/intense cluster density",
        {
            "favorite_genre": "rock",
            "favorite_mood": "intense",
            "target_energy": 0.95,
            "likes_acoustic": True,
            "target_tempo": 150,
        },
    ),
    (
        "C: 'latin pop' substring collision",
        {
            "favorite_genre": "pop",
            "favorite_mood": "happy",
            "target_energy": 0.8,
            "likes_acoustic": False,
        },
    ),
    (
        "D: Mood isolation within one genre (hip hop)",
        {
            "favorite_genre": "hip hop",
            "favorite_mood": "moody",
            "target_energy": 0.5,
            "likes_acoustic": False,
            "target_tempo": 98,
        },
    ),
]

def main() -> None:
    songs = load_songs("data/songs.csv")
    print(f"Loaded songs: {len(songs)}")

    for label, user_prefs in PROFILES:
        recommendations = recommend_songs(user_prefs, songs, k=5)

        print(f"\n{label}")
        print("=" * 40)
        for rank, (song, score, explanation) in enumerate(recommendations, start=1):
            print(f"\n{rank}. {song['title']} by {song['artist']}  [Score: {score:.2f}]")
            for reason in explanation.split("; "):
                print(f"     - {reason}")
        print()


if __name__ == "__main__":
    main()
