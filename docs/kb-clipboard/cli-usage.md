# kb-clipboard CLI Command Reference

`kb-clipboard` exposes a Typer-based command-line interface. Commands can be run using `uv run kb-clipboard <command>` (or `kb-clipboard` if installed globally).

---

## Commands List

### `watch`
Runs the clipboard watcher daemon in the foreground. Useful for debugging and viewing log streams in real-time.
- **Usage**:
  ```bash
  uv run kb-clipboard watch [--interval 0.2]
  ```
- **Options**:
  - `--interval`: Polling interval in seconds (default is `0.2`).

### `start`
Spawns the clipboard watcher in the background. Under Windows, it sets the process flags to run as a windowless, detached process (via `pythonw.exe`). It writes the active Process ID to `~/.kb/clipboard_watcher.pid`.
- **Usage**:
  ```bash
  uv run kb-clipboard start
  ```

### `stop`
Safely terminates the background clipboard watcher process. Reads the process ID from `~/.kb/clipboard_watcher.pid`, kills the process (using `ctypes` on Windows), and deletes the PID file.
- **Usage**:
  ```bash
  uv run kb-clipboard stop
  ```

### `status`
Checks if the background watcher process is active. It reads the PID file and uses Windows kernel checks to verify if the process exists and is active.
- **Usage**:
  ```bash
  uv run kb-clipboard status
  ```

### `serve`
Launches the standalone Electron desktop interface.
- **Usage**:
  ```bash
  uv run kb-clipboard serve [--dev]
  ```
- **Options**:
  - `--dev`: Runs the Electron client in development mode, pointing to a running Vite local server (usually `http://localhost:3000`).
