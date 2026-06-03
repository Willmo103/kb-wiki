# 📰 kb-rss: Your Local AI-Curated Newspaper

`kb-rss` is designed to fight information overload. Instead of wading through hundreds of dry blog feeds every morning, `kb-rss` acts as your personal editor. It collects raw articles in the background, monitors what you enjoy reading, and uses a local Ollama agent to curate a personalized daily digest complete with 1-sentence reasons why each article is worth your time.

---

## How It Works Together

The application runs three core subsystems to curate your reading:
1. **The Watcher (`watcher.py`)**:
   - A quiet background loop that checks your feed list every 5 minutes.
   - Extracts titles, authors, descriptions, and timestamps, and hashes the URLs to make sure duplicates never make it into your database.
2. **Your Local Curation Agent (`agent.py`)**:
   - Watches your interactions. When you like an article, star it for later, write a comment, or just click to read, the agent takes notes.
   - It drafts a profile of your current tastes (`~/.kb/agent_user_tastes.md`).
   - Every day, it reviews the latest 50 articles, matches them against your taste profile, selects the top 5-10 recommendations, and drafts a markdown morning report for you, prompting a Gotify push alert when it's ready.
3. **The Electron Cozy Reader View**:
   - An elegant retro cream interface with a pinned navigation sidebar (designed to stay out of the way when you scroll).
   - Features a **Reader View** parser: it scrapes the full HTML, cleans the styling clutter, extracts a preview image, and saves it directly to your SQLite database so you can read it offline and keep a permanent copy before the page goes down.

