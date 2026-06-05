# kb-vault CLI Command Reference

`kb-vault` exposes a Typer-based command-line interface. Run commands using:
```bash
uv run kb-vault <command>
```
If installed in your environment, you can run `kb-vault` directly.

---

## Commands List

### `add`
Adds a directory to the configured scan paths list.
- **Usage**:
  ```bash
  uv run kb-vault add <path_to_directory>
  ```
- **Description**: Validates that the path exists and is a directory, resolves it to its canonical form, and adds it to `~/.kb/configs/kb-vault.json`. The scanner will search this path recursively for folders containing `.obsidian/`.

### `remove`
Removes a directory from the configured scan paths list.
- **Usage**:
  ```bash
  uv run kb-vault remove <path_to_directory>
  ```

### `list-paths`
Displays all paths configured for Obsidian vault scanning.
- **Usage**:
  ```bash
  uv run kb-vault list-paths
  ```

### `scan`
Recursively scans the configured paths for Obsidian vaults, indices all markdown note files, processes contents, and populates database records.
- **Usage**:
  ```bash
  uv run kb-vault scan [--dry-run]
  ```
- **Options**:
  - `--dry-run`, `-d`: Runs the parser/indexer in simulation mode, outputting found vaults and notes without committing changes or content to the database.

### `list`
Prints a tabular list of all Obsidian vaults currently indexed in the database, including the count of markdown notes indexed for each.
- **Usage**:
  ```bash
  uv run kb-vault list
  ```
