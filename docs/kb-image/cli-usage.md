# kb-image CLI Reference

The `kb-image` CLI is built using Typer and offers commands for importing assets, running the tagging daemon, and launching the Electron desktop application.

---

## Commands List

### `import`
Imports images into the database. You can supply a single file, a local directory (which scans recursively), or a web image URL.
- **Usage**:
  ```bash
  uv run kb-image import [-f FILE] [-d DIRECTORY] [-u URL]
  ```
- **Options**:
  - `-f, --file`: Path to a single image file.
  - `-d, --dir`: Path to an image directory to scan recursively.
  - `-u, --url`: Download and ingest a web image URL.

### `tag`
Iterates through all database image rows that currently have no descriptions or tags and runs them through the Ollama pipeline to populate description text and tag arrays.
- **Usage**:
  ```bash
  uv run kb-image tag
  ```

### `serve`
Launches the standalone Electron explorer UI.
- **Usage**:
  ```bash
  uv run kb-image serve
  ```
