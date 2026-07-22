"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import os

try:
    # Works when run as a package: `python -m src.main`
    from src.recommender import load_songs, recommend_songs
except ModuleNotFoundError:
    # Works when run as a script/Run button: `python src/main.py`
    from recommender import load_songs, recommend_songs

# Project root is the folder that contains this src/ directory.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SONGS_CSV = os.path.join(PROJECT_ROOT, "data", "songs.csv")


# ---------------------------------------------------------------------------
# User preference profiles
#
# Each profile is a (name, prefs) pair. The scorer in recommender.py reads the
# "genre", "mood", and "energy" keys, so those are the levers we vary here.
# ---------------------------------------------------------------------------

# Three distinct "normal" taste profiles.
NORMAL_PROFILES = [
    ("High-Energy Pop",   {"genre": "pop",  "mood": "happy",   "energy": 0.9}),
    ("Chill Lofi",        {"genre": "lofi", "mood": "chill",   "energy": 0.35}),
    ("Deep Intense Rock", {"genre": "rock", "mood": "intense", "energy": 0.9}),
]

# Adversarial / edge-case profiles: designed to try to "trick" the scoring
# logic and surface unexpected results. See the comments on each one.
ADVERSARIAL_PROFILES = [
    # Conflicting signals: wants high energy but a sad/melancholy mood. There is
    # no high-energy sad song in the catalog, so genre/mood pull one way while
    # energy pulls the other.
    ("Conflicting: hyped but sad",
        {"genre": "pop", "mood": "melancholy", "energy": 0.95}),

    # Out-of-range energy (1.5 is above the 0.0-1.0 scale). The energy term is
    # (1 - distance) * WEIGHT with no clamp, so distance > 1 makes the energy
    # points go NEGATIVE — an input the recipe never anticipated.
    ("Out-of-range energy (1.5)",
        {"genre": "edm", "mood": "energetic", "energy": 1.5}),

    # Unknown categories: a genre and mood that exist in no song. Categorical
    # bonuses can never fire, so ranking collapses to energy distance alone.
    ("Nonexistent genre & mood",
        {"genre": "polka", "mood": "euphoric", "energy": 0.5}),

    # Empty profile: no keys at all. Every song scores 0.0 and "wins" purely by
    # catalog order — exposes that the system has no sensible default.
    ("Empty profile", {}),

    # Contradiction inside the catalog's own labels: asks for an acoustic-leaning
    # "classical/melancholy" feel but at max energy, which classical songs here
    # never have. Tests genre+mood match vs. a large energy penalty.
    ("Mismatched energy vs genre",
        {"genre": "classical", "mood": "melancholy", "energy": 1.0}),
]


def print_recommendations(name: str, user_prefs: dict, songs: list) -> None:
    """Run the recommender for one profile and print its top 5 results."""
    recommendations = recommend_songs(user_prefs, songs, k=5)

    profile = ", ".join(f"{key}={value}" for key, value in user_prefs.items())
    if not profile:
        profile = "(no preferences)"

    header = f" {name}: Top {len(recommendations)} recommendations "

    print()
    print(f"User profile: {profile}")
    print(header.center(60, "="))
    print()

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        title_line = f"{rank}. {song['title']}  by  {song['artist']}"
        print(title_line)
        print(f"   Score:   {score:.2f}")
        print(f"   Reasons: {explanation}")
        print("-" * 60)


def main() -> None:
    songs = load_songs(SONGS_CSV)

    print("\n########## NORMAL PROFILES ##########")
    for name, user_prefs in NORMAL_PROFILES:
        print_recommendations(name, user_prefs, songs)

    print("\n########## ADVERSARIAL / EDGE-CASE PROFILES ##########")
    for name, user_prefs in ADVERSARIAL_PROFILES:
        print_recommendations(name, user_prefs, songs)


if __name__ == "__main__":
    main()
