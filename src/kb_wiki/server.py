import os
import threading
from pathlib import Path
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from watchfiles import watch
from kb_wiki.compiler import compile_docs

app = FastAPI(title="kb-wiki Server")

# Global paths initialized by CLI
DOCS_DIR = Path()
DIST_DIR = Path()
TEMPLATES_DIR = Path()
STATIC_SRC_DIR = Path()


def start_watcher():
    """Runs a background watcher thread to automatically compile on file change."""

    def watch_loop():
        print(
            f"Watcher started: monitoring {DOCS_DIR}, {TEMPLATES_DIR}, {STATIC_SRC_DIR} for changes..."
        )
        # Watch the docs, templates, and static source folders
        for _ in watch(str(DOCS_DIR), str(TEMPLATES_DIR), str(STATIC_SRC_DIR)):
            print("\nChange detected! Recompiling wiki site...")
            try:
                compile_docs(DOCS_DIR, DIST_DIR, TEMPLATES_DIR, STATIC_SRC_DIR)
            except Exception as e:
                print(f"Auto-compilation error: {e}")

    watcher_thread = threading.Thread(target=watch_loop, daemon=True)
    watcher_thread.start()


def setup_server(
    docs_dir: Path,
    dist_dir: Path,
    templates_dir: Path,
    static_src_dir: Path,
    dev_mode: bool = False,
):
    """Sets up folders, triggers initial compile, and mounts static files."""
    global DOCS_DIR, DIST_DIR, TEMPLATES_DIR, STATIC_SRC_DIR

    DOCS_DIR = docs_dir
    DIST_DIR = dist_dir
    TEMPLATES_DIR = templates_dir
    STATIC_SRC_DIR = static_src_dir

    # 1. Perform initial static site compilation
    print("Performing initial compilation before launching server...")
    compile_docs(DOCS_DIR, DIST_DIR, TEMPLATES_DIR, STATIC_SRC_DIR)

    # 2. In dev mode, start the file system watcher
    if dev_mode:
        start_watcher()

    # 3. Mount the static distribution directory to serve files at root
    # html=True ensures index.html is served automatically for directory paths (e.g. '/' -> '/index.html')
    app.mount("/", StaticFiles(directory=str(dist_dir), html=True), name="static")
