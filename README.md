# 🎵 Music Recommender Simulation

## Project Summary


My version is called MoodMatch 1.0. You give it a favorite genre, mood, and energy level, and it scores all 18 songs in the catalog and returns the top 5 with a reason for each pick. Genre matches earn +2.0, mood matches earn +1.5, and energy earns up to +2.0 based on how close a song is to your target. I also tested normal and edge-case listeners and ran a "Weight Shift" experiment to see how much the energy number controls the results.

---

## How The System Works


- Each song is categorized by genre and mood with numeric features that include energy, tempo_bpm, valence, danceability, and acousticness
- UserProfile stores the user's preferred value for each feature and a set of weights for how much each feature matters
- The recommender computes a score by comparing each song to the UserProfile: 
  - Categorical (genre, mood): earns a bonus when it matches exactly
  - Numeric: earns a closeness score that rewards how near the song's value is to the user's preference
  - Each result is multiplied by its weight with genre as the highest, then mood, then the vibe features
  - All the points are summed into one total score per song
- All songs are ranked by total score from highest to lowest and the top matches are returned as recommendations

Real recommenders like Spotify and YouTube do the same thing at scale. They use audio features (genre, mood, tempo) plus your listening history as the input for your preferences, then rank the whole catalog and return the top picks.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

Below is the terminal output produced by running `python -m src.main`, showing the user profile and the top recommendations with song titles, scores, and reasons:

```
Loaded songs: 18

User profile: genre=pop, mood=happy, energy=0.8
================== Top 5 recommendations ===================

1. Sunrise City  by  Neon Echo
   Score:   5.46
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+1.96)
------------------------------------------------------------
2. Gym Hero  by  Max Pulse
   Score:   3.74
   Reasons: genre match (+2.0), energy close to target (+1.74)
------------------------------------------------------------
3. Rooftop Lights  by  Indigo Parade
   Score:   3.42
   Reasons: mood match (+1.5), energy close to target (+1.92)
------------------------------------------------------------
4. Concrete Kingdom  by  Rome Vega
   Score:   2.00
   Reasons: energy close to target (+2.00)
------------------------------------------------------------
5. Night Drive Loop  by  Neon Echo
   Score:   1.90
   Reasons: energy close to target (+1.90)
------------------------------------------------------------
```


**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

- I raised energy to 4.0 and dropped genre to 1.0. Energy took over the score and genre barely mattered.
- I tested 3 normal listeners and 5 edge cases. Clear tastes got clean lists, but mood turned out to be a weak signal.

---

## Limitations and Risks

- Tiny 18-song catalog, and most genres have only one song.
- Energy dominates the score, so extreme-energy users match poorly.
- Exact-match only, and it ignores tempo, valence, and other features.

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Recommenders turn songs and users into numbers, score how closely they line up, and treat the highest total as a prediction of what you'll like. There's no real understanding of the music, and the weights I picked quietly decided the whole ranking. That's where unfairness sneaks in: when energy dominated, extreme-energy listeners scored low everywhere while average users always matched. The same kinds of feature and weight choices shape what millions of people hear on real apps.



