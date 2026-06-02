# kb-wiki

Static wiki site compiler and host server for the **kb (Knowledge-Base) Stack**.

`kb-wiki` compiles a nested directory structure of Markdown documentation files into a unified, responsive, static HTML website featuring custom solarized-light/retro-dark earth-toned style themes, client-side live search, and a background watcher for auto-reloading during development.

---

## Installation & Setup

1. **Synchronize dependencies**:
   ```bash
   uv sync
   ```

2. **Verify Python version**:
   Requires Python `3.13` or greater (matching the core `kb-core` library requirement).

---

## CLI Usage

Run the following commands using `uv run kb-wiki`:

### Compile static site
Reads Markdown files from `docs/` and compiles them to `dist/`:
```bash
uv run kb-wiki build
```

### Serve wiki site
Starts the FastAPI-based web server to host the documentation:
```bash
uv run kb-wiki serve
```

### Run in Developer Mode
Automatically watches `docs/` and package layout templates for changes, recompiles the site immediately, and serves the latest changes:
```bash
uv run kb-wiki serve --dev
```

- **Options**:
  - `--docs`: Custom documentation directory (default: `docs`)
  - `--dist`: Custom output directory (default: `dist`)
  - `--host`: Bind host address (default: `127.0.0.1`)
  - `--port`: Listen port (default: `8000`)
  - `--dev`: Enable file system watcher auto-recompile
