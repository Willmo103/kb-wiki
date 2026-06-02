# kb-rss CLI Reference

The CLI utility for `kb-rss` manages feed sources, categories, daemon states, and the AI agent execution.

---

## Commands List

### `watch`
Starts the feed ingestion loop in the foreground. Checks all configured feed links every 5 minutes.
- **Usage**:
  ```bash
  uv run kb-rss watch
  ```

### `poll-once`
Triggers a one-off update cycle across all registered feeds immediately.
- **Usage**:
  ```bash
  uv run kb-rss poll-once
  ```

### Daemon Control: `start` / `stop` / `status`
Manages the background watcher process. On Windows, `start` runs the watcher windowless and saves the PID to `~/.kb/rss_watcher.pid`.
- **Usage**:
  ```bash
  uv run kb-rss start
  uv run kb-rss stop
  uv run kb-rss status
  ```

### Feed Source Management
Manage feed endpoints inside the database:
- **Add**: `uv run kb-rss feed add <URL> --category <CATEGORY_NAME>`
- **Remove**: `uv run kb-rss feed remove <FEED_ID>`
- **List**: `uv run kb-rss feed list`

### Category Management
- **Add**: `uv run kb-rss category add <NAME>`
- **List**: `uv run kb-rss category list`

### `import-json`
Seeds the database feeds table using an input JSON file (e.g. `rss_feeds.json`).
- **Usage**:
  ```bash
  uv run kb-rss import-json <PATH_TO_JSON>
  ```

### `agent-run`
Manually triggers the tastes parser and compiles the daily AI curation digest.
- **Usage**:
  ```bash
  uv run kb-rss agent-run
  ```

### `serve`
Launches the compiled Electron client application.
- **Usage**:
  ```bash
  uv run kb-rss serve
  ```
