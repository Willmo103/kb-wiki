# kb-web Server & Ingestion API Reference

`kb-web` is built on top of the **FastAPI** web framework and uses **Uvicorn** as the ASGI production web server.

---

## 1. API Endpoints

### Ingestion API
- **Endpoint**: `POST /api/ingest`
- **Headers**:
  - `X-API-Key`: Verifies the configured `KB_API_KEY` token.
- **Request Body**:
  ```json
  {
    "url": "https://example.com/page",
    "title": "Page Title",
    "html_content": "<html>...</html>",
    "tags": ["reference", "documentation"]
  }
  ```
- **Response**: Returns the database row ID and indicates if the page was treated as a new record or inserted as a new snapshot version in the `page_versions` table.

### Admin Dashboard / Feeds
- **Endpoint**: `GET /`
  Renders the primary solarized-light/retro-dark styled dashboard showing historical web bookmarks and ingestion streams.
- **Endpoint**: `POST /settings`
  Updates system settings including credentials, Gotify server details, and LLM prompt specifications.
- **Endpoint**: `POST /reprocess/{page_id}`
  Re-scrapes the target URL and triggers another round of LLM summaries.

---

## 2. Systemd Service Deployment

`kb-web` runs in production Linux environments as a systemd background service.
- **Service Configuration**: `kb-web.service`
  ```ini
  [Unit]
  Description=kb-web Ingestion Portal
  After=network.target

  [Service]
  User=will
  WorkingDirectory=/srv/kb-web
  ExecStart=/srv/kb-web/.venv/bin/kb-web serve
  EnvironmentFile=/srv/kb-web/.env
  Restart=always

  [Install]
  WantedBy=multi-user.target
  ```
- **Service Helpers** under `scripts/`:
  - `install_service.sh`: Automates dependency installation, copying files to `/etc/systemd/system`, and enabling the daemon.
  - `manage.sh`: Easy interface to start, stop, restart, or view systemd logs (`journalctl -u kb-web -f`).
