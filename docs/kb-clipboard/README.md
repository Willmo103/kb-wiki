# kb-clipboard Overview

`kb-clipboard` is a background clipboard manager that monitors the operating system clipboard, detects copied text, file paths, and images, and registers them in the central SQLite database. It includes a native desktop application interface to browse, filter, and export logged items.

---

## Architecture

The system consists of two distinct layers:
1. **Background Watcher Service (Python)**:
   - A lightweight daemon script that runs in the background.
   - Monitors the Windows clipboard loop via Win32 API.
   - Logs text (detecting and highlighting URLs), files, and direct images/screenshots (extracting sizes, creating 64x64 thumbnails, and hashing content).
   - Stores clipboard contents directly into the `kb-core` SQLite database.
2. **Desktop UI Client (Electron + React)**:
   - Built using Vite, Tailwind CSS, and Lucide React.
   - Queries the SQLite database directly to render history.
   - Allows users to preview copied images, search texts, toggle favorite flags, delete items, and copy files or text back to the system clipboard.

```
+------------------+                   +--------------------+
|  Windows OS      |                   | Electron Desktop   |
|  Clipboard Host  |                   | Client UI (React)  |
+--------+---------+                   +---------+----------+
         |                                       |
         | (win32 API poll)                      | (direct query)
         v                                       v
+------------------+                   +--------------------+
| Python Watcher   |                   | SQLite Database    |
| Service (Daemon) +------------------>+ ~/.kb/kb.db        |
+------------------+   (insert log)    +--------------------+
```

---

## Suppression of Self-Copies

To prevent infinite loops (where copy actions performed within the Electron application itself get captured and saved by the background watcher):
- The Electron Client writes the hash of the copied item to `~/.kb/clip_skip.txt`.
- The background watcher checks this file before writing to the database.
- If a match is found, the watcher ignores the copy event and removes the entry from `clip_skip.txt`.
