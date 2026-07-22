# 🎵 Music Recommender Simulation

## Project Summary

In this project you will build and explain a small music recommender system.

Your goal is to:

- Represent songs and a user "taste profile" as data
- Design a scoring rule that turns that data into recommendations
- Evaluate what your system gets right and wrong
- Reflect on how this mirrors real world AI recommenders

Replace this paragraph with your own summary of what your version does.

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.
- Each song is categorized by genre and mood with numeric features that include energy, tempo_bpm, valence, danceability, and acousticness
- UserProfile stores the user's preferred value for each feature and a set of weights for how much each feature matters
- The recommender computes a score by comparing each song to the UserProfile: 
  - Categorical (genre, mood): earns a bonus when it matches exactly
  - Numeric: earns a closeness score that rewards how near the song's value is to the user's preference
  - Each result is multiplied by its weight with genre as the highest, then mood, then the vibe features
  - All the points are summed into one total score per song
- All songs are ranked by total score from highest to lowest and the top matches are returned as recommendations



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

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



