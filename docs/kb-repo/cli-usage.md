# kb-repo CLI Command Reference

`kb-repo` exposes a Typer-based CLI wrapper. Run commands using:
```bash
uv run kb-repo <command>
```
If installed in your environment, you can run `kb-repo` directly.

---

## Commands List

### `add`
Adds a directory to the configured scan paths.
- **Usage**:
  ```bash
  uv run kb-repo add <path_to_directory>
  ```
- **Description**: Validates that the path exists and is a directory, resolves it to its canonical form, and adds it to `~/.kb/configs/kb-repo.json`.

### `remove`
Removes a directory from the configured scan paths.
- **Usage**:
  ```bash
  uv run kb-repo remove <path_to_directory>
  ```

### `list-paths`
Displays all paths configured for repository scanning.
- **Usage**:
  ```bash
  uv run kb-repo list-paths
  ```

### `scan`
Triggers a manual metadata and content sync across all configured scan paths.
- **Usage**:
  ```bash
  uv run kb-repo scan [--dry-run]
  ```
- **Options**:
  - `--dry-run`, `-d`: Runs the scanner in simulation mode, outputting found repositories and files without committing changes or content to the database.

### `list`
Prints a tabular list of all repositories currently tracked in the database, including the count of files indexed for each.
- **Usage**:
  ```bash
  uv run kb-repo list
  ```

---

## Background Daemon Watcher (`watch`)

`kb-repo` includes a background file-watcher process that monitors filesystem events (using the `watchfiles` package) and updates database content references automatically.

### `watch run`
Launches the watcher synchronously in the foreground.
- **Usage**:
  ```bash
  uv run kb-repo watch run
  ```
- **Description**: Excellent for troubleshooting, since logs are written to the terminal in real-time.

### `watch start`
Launches the file watcher as a detached background process (daemon).
- **Usage**:
  ```bash
  uv run kb-repo watch start
  ```
- **Description**: Spawns a windowless background daemon (using `pythonw.exe` on Windows). Writes the active background process ID (PID) to `~/.kb/repo_watcher.pid`.

### `watch stop`
Gracefully terminates the active background watcher daemon.
- **Usage**:
  ```bash
  uv run kb-repo watch stop
  ```
- **Description**: Reads the process ID from `repo_watcher.pid`, kills the process (safely terminating tasks under Windows/Unix), and deletes the PID file.

### `watch status`
Checks if the background watcher process is active.
- **Usage**:
  ```bash
  uv run kb-repo watch status
  ```
