# kb-wiki Maintenance Guide for AI Agents

Welcome, Agent! This file outlines the architecture, standards, and procedures for maintaining and updating the `kb-wiki` documentation website. Read this guide to understand how to keep this site synchronized with the `kb` ecosystem.

---

## 1. How to Determine if the kb Stack Has Changed

To determine if documentation needs to be updated, scan the other sibling directories inside the `remotes/` folder (e.g., `../kb-core`, `../kb-clipboard`, `../kb-rss`, etc.):

1. **Git Commit History**: Run `git -C ../kb-<package> log -n 5` to inspect recent commit descriptions and see if there are code adjustments since the last documentation updates.
2. **Version Bump Verification**: Check `pyproject.toml` or `package.json` in sibling folders. If the package version has been incremented, review the code diffs for new features.
3. **Database Schema Diffing**: If schema files (e.g., `db.py` files) have changed, verify if columns or tables were added, modified, or deleted.
4. **CLI Updates**: Scan `cli.py` files to see if any new Typer commands, options, or flags were registered.

---

## 2. Document Layout & Structure

Documentation source files reside in the `docs/` folder:

- **Single-file libraries**: Libraries that do not require multi-page guides (like `kb-core`) reside directly under `docs/` as a single markdown file (e.g. `docs/kb-core.md`).
- **Standard packages**: Each application (like `kb-rss` or `kb-clipboard`) must have its own subdirectory under `docs/` containing:
  - `README.md`: Serving as the index and architecture overview page (compiled as `index.html` inside the folder).
  - Sub-topic guides: Individual markdown files detailing specific aspects, e.g., `cli-usage.md`, `desktop-client.md`, `ai-agent.md`, etc.

The compiler (`src/kb_wiki/compiler.py`) automatically maps these files to user-friendly titles in the sidebar using a `TITLE_MAPPING` dictionary. When adding a new file, ensure you add its mapping entry.

---

## 3. What Each Wiki Page Should Include

Every package documentation structure must be thorough, user-facing, and developer-aligned, including:

- **Overview / Architecture**: A clear description of the component's role, system relationships, and data flows (utilize Mermaid diagrams where applicable).
- **Setup & Configuration**: List of dependencies, installation commands, required environment variables, and config schemas (stored in `~/.kb/configs/`).
- **CLI Command Reference**: Comprehensive documentation of CLI commands, options, flags, and usage examples.
- **Database Schema**: Full database column specifications for any tables managed by the application.
- **UI & Frontend**: Explanations of client features, desktop Electron packaging, and IPC context bridges.

---

## 4. Wiki Versioning

- The `kb-wiki` package has its own version tracked in `pyproject.toml`.
- Increment the patch version of `kb-wiki` whenever documentation files are updated or the compiler/server code is modified.
- Keep a high-level changelog at the bottom of the root `README.md` or in a dedicated section if significant features are modified.

---

## 5. User Style & Design Guidelines

When modifying HTML/CSS styles in `src/kb_wiki/templates/layout.html` or `src/kb_wiki/static/style.css`:
- **default theme**: `solarized-light` (cream-colored `#fdf6e3` background, warm grays, earthy browns, and soft shadows).
- **dark theme**: `retro-dark` (earthy browns `#2d241e`, deep tans, and warm grays).
- **highlights**: Accent orange (`#cb4b16`) and turquoise (`#2aa198`).
- **theme toggle**: Minimalist, unobtrusive, hidden in the header.
- **zoom compatibility**: The site should support zoomed-out scaling (comfortable at 70% zoom on wide screens) while remaining responsive on mobile layouts.
- **sidebar**: Pinned left sidebar containing hierarchical collapsible modules with a live filter search box.

---

## 6. Procedure for Updating the Agent's Own Understanding

When executing updates to `kb-wiki`:
1. Check other repositories in the `remotes/` folder for changes.
2. Edit or add the appropriate Markdown files under `docs/`.
3. If new files or folders are introduced, register them in `src/kb_wiki/compiler.py` inside `TITLE_MAPPING` and `FOLDER_ORDER`.
4. Compile the site locally using `uv run kb-wiki build` and resolve any compiler syntax or rendering issues.
5. If you modify compilation behavior, sidebar rendering, or stylesheet definitions, update this `GEMINI.md` file to keep future agents aligned.
