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


def main() -> None:
    songs = load_songs(SONGS_CSV)

    # Starter example profile
    user_prefs = {"genre": "pop", "mood": "happy", "energy": 0.8}

    recommendations = recommend_songs(user_prefs, songs, k=5)

    profile = (
        f"genre={user_prefs['genre']}, "
        f"mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}"
    )
    header = f" Top {len(recommendations)} recommendations "

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


if __name__ == "__main__":
    main()
