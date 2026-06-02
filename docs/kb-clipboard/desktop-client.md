# kb-clipboard Desktop UI Client

The Desktop interface is packaged inside a standalone **Electron** app container, bypassing the need for a web api server by connecting directly to the SQLite database.

---

## Technical Architecture

- **Runtime**: Electron + Node.js.
- **Frontend Stack**: React, Vite, Tailwind CSS, Lucide Icons.
- **Database Driver**: Native `sqlite3` driver compiled for Electron's active ABI.
- **Theme**: Earth-toned, retro-solarized light layout with an optional dark theme.
- **Communication Bridge (`preload.js`)**: Exposes context-bridged IPC endpoints to query database rows securely and execute python command subprocesses (e.g. starting/stopping the daemon).

---

## Core Features

- **Clipboard Log Table**: Shows a paginated, filterable grid of all copied items.
- **Content Previews**:
  - *Text*: Standard preview with a one-click copy button.
  - *Links*: Inspects and formats URLs as clickable links.
  - *Images/Screenshots*: Renders base64-encoded thumbnails directly in the UI drawer.
  - *Files*: Lists copied file paths and sizes.
- **Toggle Favorites**: Users can bookmark clipboard history rows to prevent them from being cleaned up or rotated out of the history log.
- **Cleanup / Purge**: Allows deleting specific entries or purging history except for marked favorites.
- **System Tray Integration**: Adds a system tray icon with quick-actions (e.g. copy last item, launch client, stop service).
