# kb-rss Overview

`kb-rss` is an AI-curated RSS feed ingestion, analysis, and curation utility. It operates a background feed watcher, records articles to the database, monitors user interaction history, and generates a personalized daily reading digest utilizing an Ollama agent.

---

## System Architecture

The application contains three core subsystems:
1. **Feed Watcher (`watcher.py`)**:
   - Loops every 5 minutes in the background to poll XML feed endpoints.
   - Parses items using `feedparser`, extracts titles, link urls, authors, publication dates, and summary contents.
   - Avoids duplicates by verifying the unique URL hash.
2. **Taste Curation Agent (`agent.py`)**:
   - Tracks user interactions: liked articles, clicked posts, star status, and comments.
   - Summarizes these interactions into a user profile markdown file `~/.kb/agent_user_tastes.md`.
   - Compiles the 50 most recent articles and asks Ollama to recommend the top 5-10 articles, providing a 1-sentence curation explanation for each.
   - Generates a `daily_digest` report, saves it to the database, and triggers a Gotify notification.
3. **Electron Client UI**:
   - A retro cream layout with a pinned layout (sidebar remains locked during scrolling).
   - Allows users to read feeds, click to open original sites, like/star articles, write custom comments, and edit their Interests Profile directly.
   - Features a reader view mode which fetches the article's full HTML, cleans the document, extracts a preview image, and saves it for offline reading.
