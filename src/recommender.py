import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, asdict

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool
    target_tempo: Optional[float] = None
    favorite_valence: Optional[float] = None

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        user_prefs = asdict(user)
        song_dicts = [asdict(song) for song in self.songs]
        scored = recommend_songs(user_prefs, song_dicts, k=k)
        songs_by_id = {song.id: song for song in self.songs}
        return [songs_by_id[song_dict["id"]] for song_dict, _, _ in scored]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        _, reasons = score_song(asdict(user), asdict(song))
        return "; ".join(reasons) if reasons else "No matching preferences."

def load_songs(csv_path: str) -> List[Dict]:
    """Loads songs from a CSV file, casting numeric fields from str to float/int."""
    int_fields = {"id"}
    float_fields = {"energy", "tempo_bpm", "valence", "danceability", "acousticness"}

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

GENRE_MATCH_POINTS = 0.5
MOOD_MATCH_POINTS = 1.0
ENERGY_WEIGHT = 1.5
VALENCE_WEIGHT = 1.0
TEMPO_WEIGHT = 1.0
DANCEABILITY_WEIGHT = 1.0
TEMPO_SCALE = 40.0  # bpm difference beyond this earns zero tempo points
ACOUSTIC_BONUS = 0.5
ACOUSTIC_THRESHOLD = 0.6
ARTIST_REPEAT_PENALTY = 1.0  # subtracted per already-selected song from the same artist

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Scores a song against user preferences, returning (score, reasons)."""
    score = 0.0
    reasons = []

    if song["genre"].lower() == user_prefs["favorite_genre"].lower():
        score += GENRE_MATCH_POINTS
        reasons.append(f"genre match (+{GENRE_MATCH_POINTS})")

    if song["mood"].lower() == user_prefs["favorite_mood"].lower():
        score += MOOD_MATCH_POINTS
        reasons.append(f"mood match (+{MOOD_MATCH_POINTS})")

    energy_points = ENERGY_WEIGHT * max(0.0, 1 - abs(song["energy"] - user_prefs["target_energy"]))
    if energy_points > 0:
        score += energy_points
        reasons.append(f"energy similarity (+{energy_points:.2f})")

    favorite_valence = user_prefs.get("favorite_valence")
    if favorite_valence is not None:
        valence_points = VALENCE_WEIGHT * max(0.0, 1 - abs(song["valence"] - favorite_valence))
        if valence_points > 0:
            score += valence_points
            reasons.append(f"valence similarity (+{valence_points:.2f})")

    target_tempo = user_prefs.get("target_tempo")
    if target_tempo is not None:
        tempo_diff = abs(song["tempo_bpm"] - target_tempo)
        tempo_points = TEMPO_WEIGHT * max(0.0, 1 - tempo_diff / TEMPO_SCALE)
        if tempo_points > 0:
            score += tempo_points
            reasons.append(f"tempo similarity (+{tempo_points:.2f})")

    favorite_danceability = user_prefs.get("favorite_danceability")
    if favorite_danceability is not None:
        danceability_points = DANCEABILITY_WEIGHT * max(0.0, 1 - abs(song["danceability"] - favorite_danceability))
        if danceability_points > 0:
            score += danceability_points
            reasons.append(f"danceability similarity (+{danceability_points:.2f})")

    if user_prefs.get("likes_acoustic") and song["acousticness"] >= ACOUSTIC_THRESHOLD:
        score += ACOUSTIC_BONUS
        reasons.append(f"acoustic bonus (+{ACOUSTIC_BONUS})")

    return round(score, 2), reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Scores every song, then greedily picks the top k, applying a soft penalty
    for each additional song already selected from the same artist so listeners
    are more likely to be exposed to new artists rather than repeats."""
    remaining = [
        (song, score, reasons)
        for song in songs
        for score, reasons in [score_song(user_prefs, song)]
    ]

    selected = []
    artist_counts: Dict[str, int] = {}
    for _ in range(min(k, len(remaining))):
        best_index = 0
        best_effective_score = float("-inf")
        for index, (song, score, _reasons) in enumerate(remaining):
            repeat_count = artist_counts.get(song["artist"], 0)
            effective_score = score - ARTIST_REPEAT_PENALTY * repeat_count
            if effective_score > best_effective_score:
                best_effective_score = effective_score
                best_index = index

        song, score, reasons = remaining.pop(best_index)
        artist_counts[song["artist"]] = artist_counts.get(song["artist"], 0) + 1
        selected.append((song, score, "; ".join(reasons)))

    return selected
