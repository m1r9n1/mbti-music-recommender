# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**VibeExplorer 1.0**  

---

## 2. Intended Use  

VibeExplorer 1.0 is a classroom project. It is not built for real users. It shows how a simple recommender scores and ranks songs based on a listener's vibe. The scoring is meant to be easy to see and understand, not hidden.

My goal is discovery, not repetition. I do not want the system to just hand back mainstream songs a listener already knows. I want it to find new artists and songs that still match their vibe.

The system assumes the listener can describe their taste in simple terms, like a favorite genre, a favorite mood, and a target energy. It does not learn from listening history. It only works from what the listener tells it directly.

---

## 3. How the Model Works  

Each song has traits: genre, mood, energy, tempo, valence, danceability, and acousticness. The listener gives a favorite genre, a favorite mood, a target energy, and whether they like acoustic songs. Tempo, valence, and danceability targets are optional.

Every song gets a score. A genre match earns a few points. A mood match earns a few more. Energy, valence, tempo, and danceability each earn points based on how close they are to the listener's target. A song does not need a perfect match to score well. Acoustic songs get a small bonus if the listener likes acoustic music. Once every song has a score, the list is sorted best to worst. The top few are shown to the listener, with a short reason list explaining the score.

I made two changes to the starter logic. First, I added a penalty for repeat artists, so one artist cannot fill most of the top five. Second, I lowered the genre weight. At a high weight, genre acted like a hard filter and always won. A lower weight lets other traits compete. Both changes push the system toward new artists and genres instead of the same safe picks.

---

## 4. Data  

The catalog has 25 songs. It started with 10 songs, and I added 15 more. I added genres like hip hop, reggaeton, r&b, funk, and latin pop, since the starter set did not have them.

There are 12 genres, but they are not balanced. Rock has 6 songs and pop has 4. Ambient, jazz, synthwave, indie pop, funk, and latin pop each have only 1. Mood is uneven too. Happy and intense each have 7 songs and chill has 5. Relaxed, focused, and energetic each have only 1.

This leaves some tastes thin. If a listener's favorite genre or mood only has one song, they do not get much real variety. The dataset also has nothing about lyrics, language, or popularity, so the recommender cannot use any of that.

---

## 5. Strengths  

The similarity scoring works well. In the starter profile test, Sunrise City ranked first because it was close on every target. Songs that were only a little off on energy or tempo still landed near the top instead of getting cut. A song does not need to be perfect to score well, which matches how I think about music.

The artist repeat penalty also works well. I tested profiles that favored artists with more than one strong song, like LoRoom or AC/DC. The second song still showed up when it scored well, but it did not take over the list.

---

## 6. Limitations and Bias 

Genre and mood are not balanced in the catalog. Rock has 6 songs and pop has 4, while genres like ambient, jazz, and funk only have 1 each. Moods like relaxed, focused, and energetic also only have 1 song each. If a listener likes one of those thin genres or moods, they do not get much real choice.

Energy has the highest weight of any trait, so it can take over the score. Two songs with very different genres and moods can score close together just because their energy is similar. That can push results toward energy matching instead of the genre or mood the listener actually asked for.

---

## 7. Evaluation  

I tried to break the scoring instead of just trusting it. I tested a pop and happy profile with a close tie between two songs, a rock and intense profile with several songs bunched close in score, a genre test with "latin pop" against "pop" to check for false matches, and a hip hop profile to test mood against genre.

For each test, I checked if the top result matched the stated genre and mood, if close matches still ranked well instead of getting cut, and if one artist took over the list.

The genre test was the most useful. I thought "latin pop" might get mistaken for "pop," but it did not. Both directions matched correctly. The rock test also confirmed the artist penalty works, since AC/DC and 30 Seconds to Mars both had strong songs, but neither one took over the list.

---

## 8. Future Work  

The next feature I want to add is letting the listener like a song. Right now the profile is set once and never changes. The recommender never learns from what the listener actually likes. If a listener likes a song, its traits could pull similar songs into rotation, alongside their original preferences. That would let the system pick up on taste that is more specific than a genre and mood field, and it would keep adjusting instead of showing the same list every time.

---

## 9. Personal Reflection  

This project taught me a lot about how big recommenders like Spotify work under the hood. I use Spotify myself, so I kept comparing my own experience as a listener to what I was building.

The most interesting thing I found was how much one weight, like energy, can shape the whole list without the listener ever knowing it. That changed how I think about Spotify picks that have felt slightly off before. It is probably not that the system does not get my taste. It is that some trait I never see is weighted more than the ones I actually care about.

This also changed how I think about recommendation apps in general. A scoring rule can look fine and still be unfair if the data behind it is unbalanced. What feels like an app just "getting me" is really a set of weights and a dataset working together, and both can quietly favor some listeners over others.
