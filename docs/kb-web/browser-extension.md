# kb-web Chrome Ingestion Extension

The Chrome extension enables instant page archiving with a single click.

---

## Extension Structure

Found under `browser_extension/`:
- **`manifest.json`**: Configures a Manifest V3 extension, requesting permissions for `activeTab`, `storage`, and `scripting`.
- **`options.html` / `options.js`**: Setup interface to configure the target server URL (default: `http://localhost:8000`) and the `KB_API_KEY` authorization token.
- **`background.js`**: Listens for action button clicks, injects a script to extract the page's raw HTML, handles page payload formatting, and dispatches the payload to the server's `POST /api/ingest` route.

---

## Setup & Loading

1. Open Google Chrome.
2. Navigate to `chrome://extensions/`.
3. Enable **Developer mode** (top right toggle).
4. Click **Load unpacked** (top left).
5. Select the `browser_extension` directory inside the `kb-web` repo.
6. Open the extension options page and enter your `kb-web` server URL and API key.
7. Click the extension icon on any page to test. It will turn green if successful, or display an error message on failure.
