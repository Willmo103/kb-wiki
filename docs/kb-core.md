# kb-core Library Reference

`kb-core` is the foundational utility package for the `kb` ecosystem. It centralizes environment paths, database initialization, notifications, HTML template rendering, and standard file manipulation helper functions.

---

## 1. Directory Structure

The package is structured as a standard Python package:

```
kb-core/
├── src/
│   └── kb_core/
│       ├── __init__.py
│       ├── config.py       # Configuration and DB connector
│       ├── notifier.py     # Gotify notifier integration
│       ├── renderer.py     # Jinja2 template renderer
│       ├── types.py        # Core entity types
│       ├── utils.py        # Shared file and image utilities
│       ├── skip_dirs.py    # Directory exclusions list
│       ├── skip_exts.py    # Extensions to ignore
│       └── target_exts.py  # Allowed embed target extensions
├── build.py                # Automated sync/test/build script
└── pyproject.toml
```

---

## 2. Component Reference

### Config (`config.py`)
Configures system directories and instantiates the global SQLite database.
- **Root Directory**: Default path is `~/.kb` (user's home directory).
- **Database Connection**: Initializes a connection to `~/.kb/kb.db` via `sqlite-utils.Database`.
- **Config Folder**: Configurations for other apps are stored under `~/.kb/configs/` as JSON files.

```python
from kb_core.config import Config

config = Config()
db = config.get_db()
print(config.kb_root)  # E.g. C:\Users\Will\.kb
```

### Notifier (`notifier.py`)
Integrates with a local or remote **Gotify** notification server to send and query system events.
- **Environment Variables**:
  - `GOTIFY_URL`: Endpoint address.
  - `GOTIFY_TOKEN`: Application authentication token.
- **Methods**:
  - `send_notification(title, message, priority=5)`: POSTs an alert to Gotify.
  - `get_notifications(limit=10)`: Fetches notification history.

```python
from kb_core.notifier import Gotify

notifier = Gotify(token="your_token", url="http://gotify.local")
notifier.send_notification("Alert Title", "Task completed successfully!")
```

### Renderer (`renderer.py`)
A wrapper around the `jinja2` template engine used to compile and output HTML files to static folders.
- **Methods**:
  - `render_template_to_string(template_name, **kwargs)`: Renders HTML strings.
  - `render_template_to_static(template_name, output_rel_path, **kwargs)`: Renders and saves files to a preconfigured static directory.

```python
from kb_core.renderer import Renderer
from pathlib import Path

renderer = Renderer(templates_root=Path("templates"), static_root=Path("dist"))
renderer.render_template_to_static("layout.html", "index.html", title="Wiki Page")
```

### Types (`types.py`)
Defines the core `RootTypes` supported by the knowledge base ecosystem:
- `IMAGE`: Images and graphical documents.
- `VAULT`: General notes and documents.
- `REPO`: Local code repositories.
- `CLONED`: Cloned git remotes.
- `DOCUMENT`: PDFs and ebooks.

---

## 3. Package Utilities (`utils.py`)

A set of reusable helper functions used for path scanning and image processing:

| Function | Description |
|---|---|
| `is_embeddable_file(path)` | Checks if a file extension is in `target_exts.py`. |
| `read_file_text(path)` | Safely reads a file with UTF-8 encoding, falling back to windows-1252. |
| `human_size(bytes)` | Converts raw byte counts into human-readable strings (e.g. `2.4 MB`). |
| `get_uuid(content)` | Generates a unique UUIDv4 string based on input content hashing. |
| `hash_content(content)` | Generates a SHA-256 hex string for a given text or bytes block. |
| `should_ignore_path(path)` | Checks directories and file extensions against standard ignores lists. |
| `build_tree_string(path)` | Generates an ASCII folder tree string for terminal display. |
| `generate_thumbnail(img_bytes, max_size=(128, 128))` | Resizes image bytes and returns base64 thumbnail bytes. |
| `extract_exif(img_bytes)` | Extracts exif metadata tags (aperture, ISO, date taken) from image bytes. |
