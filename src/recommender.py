import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

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

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file into a list of dicts with numeric fields converted."""
    int_fields = ("id", "tempo_bpm")
    float_fields = ("energy", "valence", "danceability", "acousticness")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            song = dict(row)
            for field in int_fields:
                song[field] = int(song[field])
            for field in float_fields:
                song[field] = float(song[field])
            songs.append(song)

    print(f"Loaded songs: {len(songs)}")
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score one song against the user's preferences and return (score, reasons)."""
    # --- Algorithm Recipe weights (tweak these to match your Phase 2 recipe) ---
    GENRE_POINTS = 2.0   # awarded when the genre matches exactly
    MOOD_POINTS = 1.5    # awarded when the mood matches exactly
    ENERGY_WEIGHT = 2.0  # max points for a perfect energy match

    score = 0.0
    reasons: List[str] = []

    # 1. Genre match: full points for an exact match.
    if user_prefs.get("genre") and user_prefs["genre"] == song.get("genre"):
        score += GENRE_POINTS
        reasons.append(f"genre match (+{GENRE_POINTS})")

    # 2. Mood match: full points for an exact match.
    if user_prefs.get("mood") and user_prefs["mood"] == song.get("mood"):
        score += MOOD_POINTS
        reasons.append(f"mood match (+{MOOD_POINTS})")

    # 3. Energy: a numerical feature (0.0 - 1.0). The closer the song's
    #    energy is to the user's target, the more points it earns.
    if "energy" in user_prefs and "energy" in song:
        distance = abs(user_prefs["energy"] - song["energy"])  # 0.0 = perfect
        energy_points = (1 - distance) * ENERGY_WEIGHT
        score += energy_points
        reasons.append(f"energy close to target (+{energy_points:.2f})")

    return (score, reasons)

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """Score and rank all songs, returning the top k as (song, score, explanation) tuples."""
    # 1. Score every song in the catalog. score_song() acts as the "judge":
    #    each song gets a numeric score plus the reasons behind it. A list
    #    comprehension is the Pythonic way to map every song -> its result.
    scored = [
        (song, *score_song(user_prefs, song))  # -> (song, score, reasons)
        for song in songs
    ]

    # 2. Rank highest-to-lowest. sorted() returns a NEW list, leaving the
    #    original `songs` untouched. key = the score (index 1 of each tuple),
    #    reverse=True so the best matches come first.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)

    # 3. Keep only the top k, and turn each reasons list into a single
    #    human-readable explanation string to match the return contract.
    return [
        (song, score, ", ".join(reasons) if reasons else "no strong matches")
        for song, score, reasons in ranked[:k]
    ]
