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
  - For my design, each song in the system carries the following features: id, title, artist, genre, mood, energy, tempo_bpm, valence, danceability, and acousticness. The recommender is built around the listener's taste, using four required preferences (favorite_genre, favorite_mood, target_energy, and likes_acoustic) plus three optional ones (target_tempo, favorite_valence, and favorite_danceability). It uses a Scoring Rule and a Ranking Rule to figure out how well a song fits. The Scoring Rule gives a song points for a genre match and a bigger bump for a mood match, then adds similarity points based on how close the song's energy, valence, tempo, and danceability are to the listener's targets, plus a small bonus if the listener likes acoustic songs and the song is highly acoustic. The Ranking Rule then sorts every scored song from best to worst and returns the top few to the listener.

  ```bash
  data/songs.csv
      │
      ▼
load_songs(csv_path)                     [recommender.py]
   - csv.DictReader over the file
   - cast numeric fields (energy, tempo_bpm, valence,
     danceability, acousticness) from str -> float
   - return List[Dict]  (one dict per song row)
      │
      ▼
main.py: user_prefs = {...}              (dict, hardcoded for now)
      │
      ▼
recommend_songs(user_prefs, songs, k=5)  [recommender.py]
      │
      ├─► for each song in songs:
      │        score_song(user_prefs, song)
      │            - apply the recipe (genre/mood/energy/valence/
      │              tempo/acoustic points from the finalized table)
      │            - build a reasons list as points are earned
      │            - return (score, reasons)
      │
      ├─► collect (song, score, "; ".join(reasons)) tuples
      │
      ├─► sort by score, descending
      │
      └─► return top k tuples
      │
      ▼
main.py: loop over recommendations
   - print title, score, explanation
```
  - Note: One thing I noticed is that the Scoring Rule only checks for an exact match on genre and mood, so a song like "indie pop" or "energetic" would get zero credit even if it's really close to what the listener wants, which means the system ends up favoring whatever exact labels are already in the catalog.
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

```
Loaded songs: 15

Top Recommendations
========================================

1. Sunrise City by Neon Echo  [Score: 6.38]
     - genre match (+2.0)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.96)
     - tempo similarity (+0.95)

2. Gym Hero by Max Pulse  [Score: 4.97]
     - genre match (+2.0)
     - energy similarity (+1.30)
     - valence similarity (+0.97)
     - tempo similarity (+0.70)

3. Busy Earnin' by Jungle  [Score: 4.42]
     - mood match (+1.0)
     - energy similarity (+1.50)
     - valence similarity (+0.97)
     - tempo similarity (+0.95)

4. Rooftop Lights by Indigo Parade  [Score: 4.33]
     - mood match (+1.0)
     - energy similarity (+1.44)
     - valence similarity (+0.99)
     - tempo similarity (+0.90)

5. Titi Me Pregunto by Bad Bunny  [Score: 4.07]
     - mood match (+1.0)
     - energy similarity (+1.38)
     - valence similarity (+0.94)
     - tempo similarity (+0.75)
```

---

## Experiments You Tried
```
Loaded songs: 25

Starter profile
========================================

1. Sunrise City by Neon Echo  [Score: 5.79]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.96)
     - tempo similarity (+0.95)
     - danceability similarity (+0.91)

2. Say So by Doja Cat  [Score: 5.62]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.99)
     - tempo similarity (+0.82)
     - danceability similarity (+0.84)

3. Busy Earnin' by Jungle  [Score: 5.27]
     - mood match (+1.0)
     - energy similarity (+1.50)
     - valence similarity (+0.97)
     - tempo similarity (+0.95)
     - danceability similarity (+0.85)

4. Rooftop Lights by Indigo Parade  [Score: 5.21]
     - mood match (+1.0)
     - energy similarity (+1.44)
     - valence similarity (+0.99)
     - tempo similarity (+0.90)
     - danceability similarity (+0.88)

5. Titi Me Pregunto by Bad Bunny  [Score: 4.87]
     - mood match (+1.0)
     - energy similarity (+1.38)
     - valence similarity (+0.94)
     - tempo similarity (+0.75)
     - danceability similarity (+0.80)


A: Pop/happy tie test (Sunrise City vs. Say So)
========================================

1. Sunrise City by Neon Echo  [Score: 4.84]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.96)
     - danceability similarity (+0.91)

2. Say So by Doja Cat  [Score: 4.80]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.99)
     - danceability similarity (+0.84)

3. Busy Earnin' by Jungle  [Score: 4.32]
     - mood match (+1.0)
     - energy similarity (+1.50)
     - valence similarity (+0.97)
     - danceability similarity (+0.85)

4. Rooftop Lights by Indigo Parade  [Score: 4.31]
     - mood match (+1.0)
     - energy similarity (+1.44)
     - valence similarity (+0.99)
     - danceability similarity (+0.88)

5. Felices los 4 by Maluma  [Score: 4.27]
     - mood match (+1.0)
     - energy similarity (+1.47)
     - valence similarity (+0.97)
     - danceability similarity (+0.83)


B: Rock/intense cluster density
========================================

1. Storm Runner by Voltline  [Score: 3.89]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.44)
     - tempo similarity (+0.95)

2. Kings and Queens by 30 Seconds to Mars  [Score: 3.67]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.43)
     - tempo similarity (+0.75)

3. Crazy Train by Ozzy Osbourne  [Score: 3.67]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)
     - tempo similarity (+0.70)

4. Thunderstruck by AC/DC  [Score: 3.58]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.50)
     - tempo similarity (+0.57)

5. Gym Hero by Max Pulse  [Score: 3.02]
     - mood match (+1.0)
     - energy similarity (+1.47)
     - tempo similarity (+0.55)


C: 'latin pop' substring collision
========================================

1. Sunrise City by Neon Echo  [Score: 2.97]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)

2. Say So by Doja Cat  [Score: 2.97]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.47)

3. Busy Earnin' by Jungle  [Score: 2.50]
     - mood match (+1.0)
     - energy similarity (+1.50)

4. Felices los 4 by Maluma  [Score: 2.47]
     - mood match (+1.0)
     - energy similarity (+1.47)

5. Rooftop Lights by Indigo Parade  [Score: 2.44]
     - mood match (+1.0)
     - energy similarity (+1.44)


D: Mood isolation within one genre (hip hop)
========================================

1. No Role Modelz by J. Cole  [Score: 3.88]
     - genre match (+0.5)
     - mood match (+1.0)
     - energy similarity (+1.42)
     - tempo similarity (+0.95)

2. Night Drive Loop by Neon Echo  [Score: 2.83]
     - mood match (+1.0)
     - energy similarity (+1.12)
     - tempo similarity (+0.70)

3. The Worst by Jhene Aiko  [Score: 2.70]
     - mood match (+1.0)
     - energy similarity (+1.32)
     - tempo similarity (+0.38)

4. California Love by 2Pac  [Score: 2.42]
     - genre match (+0.5)
     - energy similarity (+0.98)
     - tempo similarity (+0.95)

5. Yonaguni by Bad Bunny  [Score: 2.33]
     - energy similarity (+1.38)
     - tempo similarity (+0.95)
```
For my experiments, I mainly tried to break my own scoring logic before trusting it. I built a few adversarial profiles on purpose: a pop and happy tie between two songs, a rock and intense cluster where several songs land close in score, a genre string test with "latin pop" that could accidentally match "pop" if I was not careful, and a hip hop profile meant to isolate mood from genre. Running these against my catalog is how I actually found the things worth changing.

- **Genre weight, 2.0 to 0.5:** At 2.0, genre acted like a hard filter, so a matching song almost always won no matter how well a non-matching song fit everything else. At 0.5, genre became more of a light nudge instead. "Titi Me Pregunto" by Bad Bunny is a good example, since it missed the top 5 entirely at weight 2.0 but jumped into 5th at 0.5 on energy, valence, and danceability alone. That is the vibe matched behavior I wanted, since it can expose someone to a new genre instead of just recycling what they already said they like.
- **Genre string matching, "latin pop" vs "pop":** genre matching is exact string equality after lowercasing, so I wanted to confirm "latin pop" would not accidentally get treated as a match for "pop" just because one contains the other. Running favorite_genre equal to "pop" correctly gave Maluma's song zero genre points, and flipping it to favorite_genre equal to "latin pop" correctly sent that same song to 1st place. The matching logic held up fine, it is just easy to misread a result like that without checking which profile produced it.
- **Adding an artist repeat penalty:** I noticed an artist with two or three good songs could take up multiple slots in one top 5 list, which works against exposing the listener to new things. I added a soft penalty, ARTIST_REPEAT_PENALTY = 1.0, subtracted each time another song from an already picked artist shows up. I tested this with LoRoom, AC/DC, 30 Seconds to Mars, Doja Cat, Bad Bunny, and Jhene Aiko, each having a second song in the running. The penalty does not hard block repeats, so a strong enough second song can still make the list.

---

## Limitations and Risks

This recommender only works on a small, unevenly distributed catalog, and it has no sense of lyrics, language, or popularity, so it can end up favoring whichever genre, mood, or trait happens to be most common in the data. See `model_card.md` for a deeper look at where that shows up.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this showed me that a recommender is really just a set of weighted rules applied to whatever data it happens to have, not some deeper understanding of taste. Building the scoring rule made it clear how easily a system like this can turn into a source of bias too. It is not doing anything malicious, it is just reflecting whatever imbalance already exists in its catalog or leaning too hard on whichever feature has the highest weight, and a listener with less common taste ends up with a worse experience without the system ever meaning for that to happen.
