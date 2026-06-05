# kb-vault Overview

`kb-vault` is a specialized Obsidian markdown vault scanner and compiler designed to integrate note-taking bases with your local knowledge network. It recursively walks configured paths to locate directories containing a `.obsidian/` folder, cataloging note hierarchy and indexing markdown content for full-text search.

---

## Key Configurations

`kb-vault` looks for its package-specific configuration inside:
- **Location**: `~/.kb/configs/kb-vault.json`
- **Format**:
  ```json
  {
    "scan_paths": [
      "C:/Users/Will/Documents/PersonalVault"
    ]
  }
  ```
The CLI exposes commands (`add`, `remove`, `list-paths`) to easily configure this list of search roots.

---

## Database Architecture

All Obsidian vault data resides within the central SQLite database at `~/.kb/kb.db`. Tables and views are managed using `sqlite-utils`.

```
                  +-----------------------------+
                  |         vault_paths         | (Tracks registered Obsidian vaults)
                  +--------------+--------------+
                                 | 1
                                 |
                                 | 1..*
                  +--------------v--------------+
                  |         vault_files         | (Stores metadata for .md notes)
                  +--------------+--------------+
                                 | 1
                                 |
                                 | 1 (foreign key)
                  +--------------v--------------+
                  |     vault_file_contents     | (Houses FTS5 markdown text)
                  +--------------+--------------+
                                 |
     +---------------------------+---------------------------+
     | (Triggers on hash update)                             | (Pre-processed note clean)
     v                                                       v
+----+-----------------------+                         +-----+-----------------------+
|    content_versions        |                         |      cleaned_markdown       |
|  (Incremental history)     |                         | (Stripped markdown representation)|
+----------------------------+                         +-----------------------------+
```

### 1. Database Tables

#### `vault_paths`
Registers paths discovered to contain Obsidian configurations (`.obsidian/`).
- **Primary Key**: `path`
- **Fields**:
  - `uuid` (TEXT): Unique ID of the vault location.
  - `name` (TEXT): Vault folder name.
  - `path` (TEXT): Absolute canonical system path to the vault.
  - `created` (TEXT): Local ISO creation timestamp.
  - `modified` (TEXT): Local ISO modified timestamp.
  - `tree` (TEXT): Cached visual representation of the vault note folder tree.
  - `last_scanned` (TEXT): Timestamp of last indexing pass.

#### `vault_files`
Logs metadata of all markdown (`.md`) files found in registered vaults (skips Obsidian internal configs, templates, and dotfolders).
- **Primary Key**: `(vault_path, file_path)`
- **Foreign Key**: `vault_path` references `vault_paths(path)`
- **Fields**:
  - `uuid` (TEXT): Unique ID.
  - `vault_path` (TEXT): Root path of the vault.
  - `file_path` (TEXT): Canonical absolute note file path.
  - `file_name` (TEXT): File name with extension.
  - `extension` (TEXT): File extension (always `.md`).
  - `relative_path` (TEXT): Relative path inside the vault.
  - `size` (INTEGER): File size in bytes.
  - `created` (TEXT): Creation timestamp.
  - `modified` (TEXT): Modified timestamp.
  - `mode` (TEXT): File permission mode string.
  - `last_scanned` (TEXT): Timestamp of last metadata indexing check.

#### `vault_file_contents`
Stores the full markdown content of indexed notes. Full-text search (FTS5) is enabled directly on the `content` field.
- **Primary Key**: `(vault_path, file_path)`
- **Foreign Key**: `vault_path` references `vault_paths(path)`
- **Fields**:
  - `uuid` (TEXT): Unique ID.
  - `vault_path` (TEXT): Root vault path.
  - `file_path` (TEXT): Absolute path.
  - `content` (TEXT): Raw markdown note text content.
  - `content_hash` (TEXT): MD5/SHA256 fingerprint of the markdown text.
  - `version` (INTEGER): Current content version number.

#### `content_versions`
Tracks historical checkpoints of note revisions, incrementing the version counter sequentially.
- **Primary Key**: `(source, file_path, version)`
- **Fields**:
  - `source` (TEXT): Vault path source.
  - `file_path` (TEXT): Absolute note path.
  - `content` (TEXT): Historical markdown content.
  - `content_hash` (TEXT): Content fingerprint.
  - `version` (INTEGER): Incremental revision index.

#### `cleaned_markdown`
Contains a pre-processed/stripped version of the note content, formatting backlinks, clean blocks, and removing formatting noise.
- **Primary Key**: `content_hash`
- **Fields**:
  - `content_hash` (TEXT): Content fingerprint of the raw note.
  - `vault_path` (TEXT): Vault path.
  - `file_path` (TEXT): Note file path.
  - `cleaned_content` (TEXT): Preprocessed plain-text note representation.

#### `vault_file_descriptions` / `vault_descriptions`
- Stores visual summaries and metadata annotations for vaults and specific notes.

#### `vault_tags` / `vault_file_tags`
- Stores note-level tags and frontmatter taxonomies.

#### `vault_file_neighbors`
- **Primary Key**: `(source_content_hash, target_content_hash)`
- **Fields**: `similarity_score` (FLOAT), `rank` (INTEGER) for note relationship links.

---

### 2. Database Triggers

`kb-vault` registers triggers directly on `vault_file_contents`:
- **`copy_vault_file_to_versions_table_on_hash_change`**: Runs `AFTER UPDATE OF content_hash`. If a note's text content is updated, it copies the previous record state to the `content_versions` table.
- **`delete_vault_file_versions_on_file_delete`**: Runs `AFTER DELETE` on `vault_file_contents` to clear associated note version histories.

---

### 3. Database Views

Quick query views created by the schema builder:
- **`vaults`**: Aggregated list of registered vaults and their total file counts.
- **`vault_master`**: Comprehensive joined overview of paths, metadata, contents, and descriptions.
- **`empty_vault_files`**: Filters notes with `size = 0`.
- **`large_vault_files`**: Lists notes with size exceeding 100KB, sorted descending.
- **`valid_vault_files`**: Identifies notes with sizes between 0 and 100KB suitable for prompt insertion and search.
