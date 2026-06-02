# kb-web Overview

`kb-web` is the web portal and browser ingestion bridge for the `kb` ecosystem. It enables manual bookmarking, automated webpage content scraping, history version snapshotting, and direct browser integration via a Chrome MV3 Extension.

---

## Core Capabilities

- **FastAPI Ingestion Server**: A centralized REST API receiving scrapes from browser hooks, curl inputs, or automated pipelines.
- **Chrome Extension Integration**: Post raw HTML, URL, and title from any active browser tab.
- **Snapshot Versioning**: If a previously-scraped URL is ingested again, `kb-web` does not overwrite the old entry. Instead, it saves the previous content in a `page_versions` history table, enabling page comparison and tracking site modifications over time.
- **AI Summary Dashboard**: Connects to Ollama to automatically summarize pages, extract key entities, and suggest categorizations or wiki pages.
- **Settings & Config Management**: Provides a dashboard to modify API keys, Ollama connection endpoints, custom summarization prompts, and Gotify alerts.
