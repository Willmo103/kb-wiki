# kb-rss Taste Curation Agent & Ollama

`kb-rss` integrates with local LLMs (typically `gemma4` or similar) to tailor article feeds to the user's explicit interests and inferred tastes.

---

## 1. Taste Profile Generation

The agent keeps track of user actions stored in the `rss_feed_entries` table:
- **Positive Signals**: Likes, Favorites (star status), Comments (input text), Clicks (clicked status).
- **Negative Signals**: Dislikes, Skip count, explicitly marked "Not Interested".

When `agent-run` triggers:
1. It compiles user interest notes from `~/.kb/user_interests.md`.
2. It fetches all liked/favorited entries and comments from the database.
3. It asks Ollama to review the logs and generate an updated taste profile:
   - **Output file**: Saves findings as a markdown document to `~/.kb/agent_user_tastes.md`.

---

## 2. Daily Digest Curation

The curation process runs on the 50 most recent unread feed items:
1. Load `~/.kb/agent_user_tastes.md` and active interests.
2. For each of the 50 entries, supply the Title, Category, and Summary description.
3. Feed this data to Ollama, asking it to pick the top 5 to 10 articles matching the taste profile.
4. **Prompt instructions**:
   > *"You are a digital archivist curating a feed for a reader. Based on their interest profile: [Tastes], pick the top 5-10 articles from the following list. For each selected article, provide a 1-sentence explanation of why it was selected."*
5. Save the curated selection and explanations to the `rss_daily_reports` table.
6. Push a summary alert to Gotify notifying the user that a new daily curation is ready for review.
