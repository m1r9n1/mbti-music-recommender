# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

I gave the agent a task to create a dataset of songs based on the MBTI traits.

**Prompts used:**

You are an MBTI expert. I want to make a music recommender that recommends music based on someones selected personality trait (MBTI). Create a dataset of 80 songs based on the 16 MBTI traits. Use the following attributes:

id

title

artist
genre

traits (pipe-seperated psychological trait keywords)

description (short one sentence summary of the song's theme) 

>
**What did the agent generate or change?**

The agent created a new file, `data/mbti_songs.csv`, containing 80 songs, five for each of the 16 MBTI types. Each row has the columns `id, title, artist, genre, traits, description`.

Before creating the file, the agent noticed that the existing `data/songs.csv` was used by `src/recommender.py` and `tests/test_recommender.py`, and it asked whether to:

- Overwrite `data/songs.csv` with the new MBTI schema, or
- Add the new data as a separate file instead.

I chose the second option, so the agent added `data/mbti_songs.csv` as a standalone file and left the existing mood/energy-based dataset and recommender code untouched.

**What did you verify or fix manually?**

The agent's first draft of the dataset was not balanced across the 16 MBTI types. It left out ESTJ entirely and gave INTP only one song, while INFP and ENTJ ended up with seven songs each and a few other types had six. I asked the agent to check the distribution. It counted the songs per type, then updated the `traits` and `description` fields on nine songs, moving the extras from INFP, ENTJ, ENFJ, INTJ, ISFP, ESFP, and ISTJ over to ESTJ and INTP. That brought every type to exactly five songs, for 80 songs total. I double-checked the final counts myself before accepting the file.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->
