# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  

- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  

Avoid code here. Pretend you are explaining the idea to a friend who does not program.

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

In my Weight Shift experiment I bumped energy up to 4.0 and dropped genre to 1.0, and I found that energy basically takes over the whole score. A song that's just 0.25 off from the user's target energy loses as many points as an exact genre match is worth, so genre barely matters anymore. This means users with extreme energy tastes (like an ambient or metal fan) get low scores everywhere, while mid-energy users always find matches. It also doesn't help that most genres only have one song, so a niche fan mostly gets songs at the right energy instead of songs they'd actually like.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected.

I tested eight listeners: three normal tastes (High-Energy Pop, Chill Lofi, Deep Intense Rock) and five edge cases (hyped but sad, out-of-range energy, nonexistent genre/mood, empty profile, and mismatched energy vs genre). For each one I checked whether the top songs actually fit what the listener asked for.

What surprised me most is how much the energy number matters. Energy is worth up to +2.0 points, the same as a genre match, so a song can rank high just by being close to the target energy even if the mood is wrong. That is why "Gym Hero" keeps showing up for the "Happy Pop" listener: Gym Hero is a pop song with energy 0.93 (almost exactly the 0.9 they asked for), so it earns 2 points for pop plus almost 2 for energy. Its mood is "intense," not "happy," but missing the mood only costs 1.5 points, which is not enough to push it down. Matching pop and energy is simply worth more than matching the happy mood, so a gym anthem beats gentler happy songs.

The other surprise was the empty profile: every song scores 0.00 and they just come back in file order, so it isn't really recommending anything.

Comparisons between each pair of profiles:

- High-Energy Pop vs Chill Lofi: opposite energy (0.9 vs 0.35), so no shared songs. Pop gets loud upbeat tracks, Lofi gets quiet mellow ones. Makes sense because energy pulls each list to a different end of the scale.
- High-Energy Pop vs Deep Intense Rock: same energy (0.9), different genre. The #1 pick differs (Sunrise City vs Storm Runner) because genre and mood decide the top spot, but the lists overlap lower down (Gym Hero, Neon Pulse, Storm Runner) because equal energy floats the same loud songs onto both.
- Chill Lofi vs Deep Intense Rock: the two most opposite listeners, nothing in common. This shows energy is the main thing separating results.
- High-Energy Pop vs hyped but sad: both want pop and high energy, but "sad" wants a melancholy mood no energetic song has. The top songs stay almost the same because pop plus energy carry them; the only sad match (a slow classical song) ranks low. Shows mood is a weak signal and gets ignored when the combo doesn't exist.
- High-Energy Pop vs out-of-range energy (1.5): the 1.5 is off the scale, so every song's energy points shrink and all scores drop. Genre and mood end up deciding the order because energy can't separate songs anymore. Shows the math doesn't guard against impossible inputs.
- Chill Lofi vs mismatched energy vs genre: the mismatched listener wants classical and melancholy but at max energy, and the only classical song is quiet. It still wins #1 because a genre match (2.0) plus mood match (1.5) beats the small energy bonus. This is the opposite of the usual pattern: two exact matches beat a big energy miss because that song is the only one that fits the labels.
- Nonexistent genre/mood vs empty profile: neither earns genre or mood points, but the polka listener still ranks by closeness to energy 0.5 and returns reasonable mid-energy songs, while the empty profile gives everything 0.00 and returns file order. Shows one falls back to energy, the other falls back to nothing.
- Hyped but sad vs mismatched energy vs genre: both ask for combos the catalog can't fully satisfy. The difference is whether a genre match exists: pop has energetic songs so pop wins and the sad mood is dropped; classical has only one quiet song so it wins on genre and mood even though the energy is wrong. The system leans on whichever signal actually has a matching song.

### Recommendation output per profile

Terminal output from running `python -m src.main`, showing each user profile and its top 5 recommendations with song titles, scores, and reasons.

#### Normal profiles

**High-Energy Pop** — `genre=pop, mood=happy, energy=0.9`

```
1. Sunrise City  by  Neon Echo
   Score:   5.34
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+1.84)
------------------------------------------------------------
2. Gym Hero  by  Max Pulse
   Score:   3.94
   Reasons: genre match (+2.0), energy close to target (+1.94)
------------------------------------------------------------
3. Rooftop Lights  by  Indigo Parade
   Score:   3.22
   Reasons: mood match (+1.5), energy close to target (+1.72)
------------------------------------------------------------
4. Storm Runner  by  Voltline
   Score:   1.98
   Reasons: energy close to target (+1.98)
------------------------------------------------------------
5. Neon Pulse  by  Circuit Kids
   Score:   1.90
   Reasons: energy close to target (+1.90)
------------------------------------------------------------
```

**Chill Lofi** — `genre=lofi, mood=chill, energy=0.35`

```
1. Library Rain  by  Paper Lanterns
   Score:   5.50
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+2.00)
------------------------------------------------------------
2. Midnight Coding  by  LoRoom
   Score:   5.36
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+1.86)
------------------------------------------------------------
3. Focus Flow  by  LoRoom
   Score:   3.90
   Reasons: genre match (+2.0), energy close to target (+1.90)
------------------------------------------------------------
4. Spacewalk Thoughts  by  Orbit Bloom
   Score:   3.36
   Reasons: mood match (+1.5), energy close to target (+1.86)
------------------------------------------------------------
5. Coffee Shop Stories  by  Slow Stereo
   Score:   1.96
   Reasons: energy close to target (+1.96)
------------------------------------------------------------
```

**Deep Intense Rock** — `genre=rock, mood=intense, energy=0.9`

```
1. Storm Runner  by  Voltline
   Score:   5.48
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+1.98)
------------------------------------------------------------
2. Gym Hero  by  Max Pulse
   Score:   3.44
   Reasons: mood match (+1.5), energy close to target (+1.94)
------------------------------------------------------------
3. Neon Pulse  by  Circuit Kids
   Score:   1.90
   Reasons: energy close to target (+1.90)
------------------------------------------------------------
4. Iron Verdict  by  Blacklight Forge
   Score:   1.86
   Reasons: energy close to target (+1.86)
------------------------------------------------------------
5. Sunrise City  by  Neon Echo
   Score:   1.84
   Reasons: energy close to target (+1.84)
------------------------------------------------------------
```

#### Adversarial / edge-case profiles

**Conflicting: hyped but sad** — `genre=pop, mood=melancholy, energy=0.95`

```
1. Gym Hero  by  Max Pulse
   Score:   3.96
   Reasons: genre match (+2.0), energy close to target (+1.96)
------------------------------------------------------------
2. Sunrise City  by  Neon Echo
   Score:   3.74
   Reasons: genre match (+2.0), energy close to target (+1.74)
------------------------------------------------------------
3. Moonlit Sonata Redux  by  Clara Beaumont
   Score:   2.20
   Reasons: mood match (+1.5), energy close to target (+0.70)
------------------------------------------------------------
4. Neon Pulse  by  Circuit Kids
   Score:   2.00
   Reasons: energy close to target (+2.00)
------------------------------------------------------------
5. Iron Verdict  by  Blacklight Forge
   Score:   1.96
   Reasons: energy close to target (+1.96)
------------------------------------------------------------
```

**Out-of-range energy (1.5)** — `genre=edm, mood=energetic, energy=1.5`

```
1. Neon Pulse  by  Circuit Kids
   Score:   4.40
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+0.90)
------------------------------------------------------------
2. Concrete Kingdom  by  Rome Vega
   Score:   2.10
   Reasons: mood match (+1.5), energy close to target (+0.60)
------------------------------------------------------------
3. Iron Verdict  by  Blacklight Forge
   Score:   0.94
   Reasons: energy close to target (+0.94)
------------------------------------------------------------
4. Gym Hero  by  Max Pulse
   Score:   0.86
   Reasons: energy close to target (+0.86)
------------------------------------------------------------
5. Storm Runner  by  Voltline
   Score:   0.82
   Reasons: energy close to target (+0.82)
------------------------------------------------------------
```

**Nonexistent genre & mood** — `genre=polka, mood=euphoric, energy=0.5`

```
1. Island Time  by  Sunny Coast Collective
   Score:   2.00
   Reasons: energy close to target (+2.00)
------------------------------------------------------------
2. Velvet Hours  by  Aria Soul
   Score:   1.96
   Reasons: energy close to target (+1.96)
------------------------------------------------------------
3. Dust and Diesel  by  Cole Hartley
   Score:   1.84
   Reasons: energy close to target (+1.84)
------------------------------------------------------------
4. Midnight Coding  by  LoRoom
   Score:   1.84
   Reasons: energy close to target (+1.84)
------------------------------------------------------------
5. Focus Flow  by  LoRoom
   Score:   1.80
   Reasons: energy close to target (+1.80)
------------------------------------------------------------
```

**Empty profile** — `(no preferences)`

```
1. Sunrise City  by  Neon Echo
   Score:   0.00
   Reasons: no strong matches
------------------------------------------------------------
2. Midnight Coding  by  LoRoom
   Score:   0.00
   Reasons: no strong matches
------------------------------------------------------------
3. Storm Runner  by  Voltline
   Score:   0.00
   Reasons: no strong matches
------------------------------------------------------------
4. Library Rain  by  Paper Lanterns
   Score:   0.00
   Reasons: no strong matches
------------------------------------------------------------
5. Gym Hero  by  Max Pulse
   Score:   0.00
   Reasons: no strong matches
------------------------------------------------------------
```

**Mismatched energy vs genre** — `genre=classical, mood=melancholy, energy=1.0`

```
1. Moonlit Sonata Redux  by  Clara Beaumont
   Score:   4.10
   Reasons: genre match (+2.0), mood match (+1.5), energy close to target (+0.60)
------------------------------------------------------------
2. Iron Verdict  by  Blacklight Forge
   Score:   1.94
   Reasons: energy close to target (+1.94)
------------------------------------------------------------
3. Neon Pulse  by  Circuit Kids
   Score:   1.90
   Reasons: energy close to target (+1.90)
------------------------------------------------------------
4. Gym Hero  by  Max Pulse
   Score:   1.86
   Reasons: energy close to target (+1.86)
------------------------------------------------------------
5. Storm Runner  by  Voltline
   Score:   1.82
   Reasons: energy close to target (+1.82)
------------------------------------------------------------
```

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
