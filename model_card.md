# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeExplorer 2.0**

This model card documents VibeExplorer 2.0, the MBTI/RAG-based recommender described starting in Section 2. Where a section refers to "VibeExplorer 1.0" or "the original system," it is describing the earlier scoring-based version this project extends.

---

## 2. Base Project and Its Original Scope

This project extends a starter assignment called the **Music Recommender
Simulation**. Sections 3–7 below (How the Model Works, Data, Strengths,
Limitations, Evaluation) describe that original system as I originally built
it, before the MBTI/RAG extension.

**Original goal.** Build and explain a small music recommender: represent
songs and a listener's taste profile as data, design a scoring rule that
turns that data into ranked recommendations, and evaluate what the system
gets right and wrong.

**Original capabilities.**

- **Song representation** — each song was a flat feature vector: `id`,
  `title`, `artist`, `genre`, `mood`, `energy`, `tempo_bpm`, `valence`,
  `danceability`, `acousticness`.
- **Listener representation** — a `UserProfile` with four required
  preferences (`favorite_genre`, `favorite_mood`, `target_energy`,
  `likes_acoustic`) and three optional ones (`target_tempo`,
  `favorite_valence`, `favorite_danceability`).
- **Scoring rule** — `score_song()` gave points for an exact genre match, a
  bigger bump for an exact mood match, and similarity points the closer a
  song's energy/valence/tempo/danceability were to the listener's targets,
  plus a small bonus for acoustic songs if the listener liked acoustic
  music.
- **Ranking rule** — `recommend_songs()` sorted every scored song from best
  to worst and returned the top `k`, applying a soft `ARTIST_REPEAT_PENALTY`
  so one artist couldn't fill most of the top 5.
- **Catalog** — a hand-curated `data/songs.csv` of 25 songs across 12
  unevenly-distributed genres (see Section 4 below).

**What this project changed.** The MBTI/RAG extension (documented in the
README and reflected in `src/retriever.py` / `src/recommender.py`) replaces
the hand-weighted scoring rule with embedding-based semantic retrieval keyed
to MBTI personality types, and adds an LLM-generated (Gemini) summary on top
of the ranked results, while keeping the same overall load → rank → explain
shape and the `Recommender`/`UserProfile`/`Song` interface tested in
`tests/test_recommender.py`. It also swapped the 25-song `data/songs.csv`
catalog for an 80-song `data/mbti_songs.csv` catalog (5 songs per MBTI
type) with MBTI-tagged trait keywords instead of genre/mood/energy fields.

---

## 2. Intended Use  

VibeExplorer 1.0 is a classroom project. It is not built for real users. It shows how a simple recommender scores and ranks songs based on a listener's vibe. The scoring is meant to be easy to see and understand, not hidden.

My goal is discovery, not repetition. I do not want the system to just hand back mainstream songs a listener already knows. I want it to find new artists and songs that still match their vibe.

The system assumes the listener can describe their taste in simple terms, like a favorite genre, a favorite mood, and a target energy. It does not learn from listening history. It only works from what the listener tells it directly.

---

## 4. How the Original Model Worked

Each song has traits: genre, mood, energy, tempo, valence, danceability, and acousticness. The listener gives a favorite genre, a favorite mood, a target energy, and whether they like acoustic songs. Tempo, valence, and danceability targets are optional.

Every song gets a score. A genre match earns a few points. A mood match earns a few more. Energy, valence, tempo, and danceability each earn points based on how close they are to the listener's target. A song does not need a perfect match to score well. Acoustic songs get a small bonus if the listener likes acoustic music. Once every song has a score, the list is sorted best to worst. The top few are shown to the listener, with a short reason list explaining the score.

I made two changes to the starter logic. First, I added a penalty for repeat artists, so one artist cannot fill most of the top five. Second, I lowered the genre weight. At a high weight, genre acted like a hard filter and always won. A lower weight lets other traits compete. Both changes push the system toward new artists and genres instead of the same safe picks.

---

## 5. Original Data

The catalog has 25 songs. It started with 10 songs, and I added 15 more. I added genres like hip hop, reggaeton, r&b, funk, and latin pop, since the starter set did not have them.

There are 12 genres, but they are not balanced. Rock has 6 songs and pop has 4. Ambient, jazz, synthwave, indie pop, funk, and latin pop each have only 1. Mood is uneven too. Happy and intense each have 7 songs and chill has 5. Relaxed, focused, and energetic each have only 1.

This leaves some tastes thin. If a listener's favorite genre or mood only has one song, they do not get much real variety. The dataset also has nothing about lyrics, language, or popularity, so the recommender cannot use any of that.

---

## 6. Strengths (Original System)

The similarity scoring works well. In the starter profile test, Sunrise City ranked first because it was close on every target. Songs that were only a little off on energy or tempo still landed near the top instead of getting cut. A song does not need to be perfect to score well, which matches how I think about music.

The artist repeat penalty also works well. I tested profiles that favored artists with more than one strong song, like LoRoom or AC/DC. The second song still showed up when it scored well, but it did not take over the list.

---

## 7. Limitations and Bias (Original System)

Genre and mood are not balanced in the catalog. Rock has 6 songs and pop has 4, while genres like ambient, jazz, and funk only have 1 each. Moods like relaxed, focused, and energetic also only have 1 song each. If a listener likes one of those thin genres or moods, they do not get much real choice.

Energy has the highest weight of any trait, so it can take over the score. Two songs with very different genres and moods can score close together just because their energy is similar. That can push results toward energy matching instead of the genre or mood the listener actually asked for.

---

## 8. Evaluation (Original System)

I tried to break the scoring instead of just trusting it. I tested a pop and happy profile with a close tie between two songs, a rock and intense profile with several songs bunched close in score, a genre test with "latin pop" against "pop" to check for false matches, and a hip hop profile to test mood against genre.

For each test, I checked if the top result matched the stated genre and mood, if close matches still ranked well instead of getting cut, and if one artist took over the list.

The genre test was the most useful. I thought "latin pop" might get mistaken for "pop," but it did not. Both directions matched correctly. The rock test also confirmed the artist penalty works, since AC/DC and 30 Seconds to Mars both had strong songs, but neither one took over the list.

---

## 9. Future Work  

The next feature I want to add is letting the listener like a song. Right now the profile is set once and never changes. The recommender never learns from what the listener actually likes. If a listener likes a song, its traits could pull similar songs into rotation, alongside their original preferences. That would let the system pick up on taste that is more specific than a genre and mood field, and it would keep adjusting instead of showing the same list every time.

---

## 10. Personal Reflection  

This project taught me a lot about how big recommenders like Spotify work under the hood. I use Spotify myself, so I kept comparing my own experience as a listener to what I was building.

The most interesting thing I found was how much one weight, like energy, can shape the whole list without the listener ever knowing it. That changed how I think about Spotify picks that have felt slightly off before. It is probably not that the system does not get my taste. It is that some trait I never see is weighted more than the ones I actually care about.

This also changed how I think about recommendation apps in general. A scoring rule can look fine and still be unfair if the data behind it is unbalanced. What feels like an app just "getting me" is really a set of weights and a dataset working together, and both can quietly favor some listeners over others.

---

## 11. Responsible AI Reflection

This section covers the current MBTI/RAG system described in the README, not the original scoring system above.

### What are the limitations or biases in your system?

The catalog only has 80 songs, 5 per MBTI type. That is not much variety, and a couple of thin or mislabeled songs can shape a whole type's results. The embedding model only reads trait tags and a description, not the actual audio, so two songs with very different energy or tempo could still look similar if their wording is close. There is a deeper bias too: MBTI itself is not fully backed by psychological research, so tying songs to a type risks treating a listener like a stereotype instead of an individual. Last, the Gemini summary is only grounded by the prompt, not by code, so it could in theory mention something the retrieved songs do not support, even though I did not see that happen in testing.

### Could your AI be misused, and how would you prevent that?

The input is just an MBTI type typed into a CLI prompt, so there is not much to misuse here directly. But the same pattern could be misused at a larger scale, like assuming someone's taste, mood, or other traits just from a personality label instead of who they actually are. To guard against that, the MBTI type is only ever typed in by the listener. Nothing is inferred or saved about them. The Gemini prompt is also kept narrow: it can only talk about the retrieved songs, not make broader claims about the listener.

### What surprised you while testing your AI's reliability?

The biggest surprise was that retrieval on its own does not respect labels at all. Before I added `EXACT_TYPE_MATCH_BONUS`, a song from the wrong MBTI type could outrank the correctly labeled song, just because its wording was closer to the query. I expected labels to matter more than they did. The second surprise was that Gemini stayed grounded in every manual test I ran (INFP, ENTP, ESTJ, and a few others), even though nothing in the code forces that. That was reassuring, but it is not a guarantee, since I only tested a handful of runs by hand.

### Describe your collaboration with AI during this project.

For timing purposes and learning, I used an AI coding agent for most of this project: building the catalog, the retrieval and recommender code, the logging and guardrails, and the docs. With back and forth converstations, I treated its output as a first draft to check, not something to accept as is.

**A helpful suggestion:** when retrieval turned out to ignore MBTI labels, the agent suggested keeping retrieval purely semantic and adding a small re-ranking bonus for exact type matches, instead of a hard filter. That fixed the labeling problem without losing good matches from other types. This is in the README's Design Decisions section.

**A flawed suggestion:** the agent's first draft of the 80-song catalog was unevenly distributed. It left out ESTJ entirely and gave a few types six or seven songs instead of five. I caught this by asking it to count songs per type, and it then rebalanced the catalog. This is documented in `ai_interactions.md`. It was a reminder that AI output can look complete while still being quietly wrong.
