# kb-repo Overview

`kb-repo` is a specialized local repository indexer and directory watcher. It automatically walks configured code directories, catalogs Git repositories, indexes file metadata and contents, and runs a file watcher daemon to keep the database representation synchronized in real-time.

---

## Key Configurations

`kb-repo` looks for its package-specific configuration inside:
- **Location**: `~/.kb/configs/kb-repo.json`
- **Format**:
  ```json
  {
    "scan_paths": [
      "C:/Users/Will/Desktop/will_mono"
    ]
  }
  ```
The CLI exposes path management commands (`add`, `remove`, `list-paths`) to modify this scan path array.

---

## Database Architecture

All repository data is written to the centralized SQLite database at `~/.kb/kb.db`. The tables are initialized and modified using `sqlite-utils`.

```
                  +-----------------------------+
                  |         repo_paths          | (Tracks root repository folders)
                  +--------------+--------------+
                                 | 1
                                 |
                                 | 1..*
                  +--------------v--------------+
                  |         repo_files          | (Stores file metadata & size)
                  +--------------+--------------+
                                 | 1
                                 |
                                 | 1 (foreign key)
                  +--------------v--------------+
                  |     repo_file_contents      | (Houses FTS5 full-text content)
                  +--------------+--------------+
                                 |
     +---------------------------+---------------------------+
     | (Triggers on hash update)                             | (Triggers on file delete)
     v                                                       v
+----+-----------------------+                         +-----+-----------------------+
|    content_versions        |                         |   Removes stale versions    |
|  (Incremental history)     |                         +-----------------------------+
+----------------------------+
```

### 1. Database Tables

#### `repo_paths`
Registers directories recognized as root Git repositories (containing `.git`).
- **Primary Key**: `path`
- **Fields**:
  - `uuid` (TEXT): Unique ID of the repository path.
  - `name` (TEXT): Base directory name.
  - `path` (TEXT): Absolute canonical system directory path.
  - `created` (TEXT): Local ISO creation timestamp.
  - `modified` (TEXT): Local ISO modified timestamp.
  - `tree` (TEXT): Cached visual representation of the repository directory tree.
  - `last_scanned` (TEXT): Timestamp of last index pass.

#### `repo_files`
Logs metadata of all files discovered inside tracked repositories, matching exclusion filters (skips `.git`, build directories, dependency directories like `.venv` and `node_modules`, and binary extension filters).
- **Primary Key**: `(repo_path, file_path)`
- **Foreign Key**: `repo_path` references `repo_paths(path)`
- **Fields**:
  - `uuid` (TEXT): Unique ID of the file entry.
  - `repo_path` (TEXT): Root path of the repository containing the file.
  - `file_path` (TEXT): Canonical absolute file path.
  - `relative_path` (TEXT): Path relative to repository root.
  - `file_name` (TEXT): File name with extension.
  - `extension` (TEXT): File extension (e.g. `.py`, `.md`).
  - `size` (INTEGER): File size in bytes.
  - `created` (TEXT): Creation timestamp.
  - `modified` (TEXT): Modified timestamp.
  - `mode` (TEXT): String permission mode (octal representation).
  - `last_scanned` (TEXT): Last metadata check.

#### `repo_file_contents`
Stores full-text file contents. Full-text search (FTS5) is enabled directly on the `content` field.
- **Primary Key**: `(repo_path, file_path)`
- **Foreign Key**: `repo_path` references `repo_paths(path)`
- **Fields**:
  - `uuid` (TEXT): Unique ID.
  - `repo_path` (TEXT): Repository root.
  - `file_path` (TEXT): Full file path.
  - `content` (TEXT): Full raw file text content.
  - `content_hash` (TEXT): MD5/SHA256 fingerprint of the text content.
  - `version` (INTEGER): Current content version number.

#### `content_versions`
Stores historical file content checkpoints. populating version revisions incrementally.
- **Primary Key**: `(source, file_path, version)`
- **Fields**:
  - `source` (TEXT): Repository path source.
  - `file_path` (TEXT): File path.
  - `content` (TEXT): Historical file content.
  - `content_hash` (TEXT): Content fingerprint.
  - `version` (INTEGER): Incremental revision number.

#### `repo_file_descriptions`
- **Primary Key**: `content_hash`
- **Fields**: `content_hash`, `description`, `repo_path`, `file_path`.

#### `repo_descriptions`
- **Primary Key**: `repo_path`
- **Fields**: `repo_uuid`, `repo_path`, `description`.

#### `repo_tags` / `repo_file_tags`
- Tracks labels and custom tags assigned to files.

#### `repo_file_neighbors`
- **Primary Key**: `(source_content_hash, target_content_hash)`
- **Fields**: `similarity_score` (FLOAT), `rank` (INTEGER) for content relationship maps.

---

### 2. Database Triggers

`kb-repo` configures triggers directly on `repo_file_contents`:
- **`copy_repo_file_to_versions_table_on_hash_change`**: Runs `AFTER UPDATE OF content_hash`. If the new hash differs from the old hash, the trigger copies the old row contents to the `content_versions` table, incrementing the revision sequence.
- **`delete_repo_file_versions_on_file_delete`**: Runs `AFTER DELETE` on `repo_file_contents` to clear associated history versions.

---

### 3. Database Views

The package defines several views for quick querying:
- **`repos`**: Lists tracked repositories, aggregated with total files indexed.
- **`repo_master`**: Joins paths, metadata files, contents, and optional file summaries.
- **`empty_repo_files`**: Selects all indexed files with `size = 0`.
- **`large_repo_files`**: Lists files with size greater than 100KB, sorted descending.
- **`repo_scripts`**: Filters files ending in shell scripting extensions (`.ps1`, `.bat`, `.cmd`, `.sh`), excluding markdown mappings.
- **`python_scripts`**: Identifies PEP-723 inline python scripts using content match.
