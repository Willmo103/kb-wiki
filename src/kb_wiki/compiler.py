import os
import shutil
from pathlib import Path
import markdown
import jinja2

# Helper to map filenames to nice sidebar titles
TITLE_MAPPING = {
    "index.md": "Introduction",
    "kb-core.md": "kb-core (Core Library)",
    "README.md": "Overview",
    "cli-usage.md": "CLI Reference",
    "desktop-client.md": "Desktop UI Client",
    "ai-integration.md": "AI Vision Tagger",
    "ai-agent.md": "Taste Curation Agent",
    "server-api.md": "Server Ingestion API",
    "browser-extension.md": "Chrome Extension",
    "telemetry-server.md": "Telemetry Server Schema",
    "telemetry-collector.md": "Telemetry Collector Agent",
}

FOLDER_ORDER = [
    "kb-clipboard",
    "kb-image",
    "kb-rss",
    "kb-web",
    "kb-network",
    "kb-network-agent"
]

def get_title_for_file(filename: str) -> str:
    return TITLE_MAPPING.get(filename, filename.replace(".md", "").title())

def build_sidebar_nav(docs_dir: Path, active_rel_path: str) -> list:
    """
    Builds a hierarchical sidebar list.
    """
    sidebar = []
    
    # 1. Add top-level files: index.md and kb-core.md
    for filename in ["index.md", "kb-core.md"]:
        path = docs_dir / filename
        if path.exists():
            url = filename.replace(".md", ".html")
            sidebar.append({
                "is_folder": False,
                "title": get_title_for_file(filename),
                "url": url,
                "active": url == active_rel_path
            })
            
    # 2. Add folder modules in pre-defined order
    for folder in FOLDER_ORDER:
        folder_path = docs_dir / folder
        if folder_path.exists() and folder_path.is_dir():
            folder_items = []
            
            # Find all markdown files in folder
            md_files = list(folder_path.glob("*.md"))
            
            # Put README.md first
            md_files_sorted = []
            readme = folder_path / "README.md"
            if readme.exists():
                md_files_sorted.append(readme)
            for f in sorted(md_files):
                if f.name != "README.md":
                    md_files_sorted.append(f)
                    
            for f in md_files_sorted:
                rel_url = f"{folder}/" + f.name.replace(".md", ".html")
                if f.name == "README.md":
                    rel_url = f"{folder}/index.html"
                    
                folder_items.append({
                    "title": get_title_for_file(f.name),
                    "url": rel_url,
                    "active": rel_url == active_rel_path
                })
                
            sidebar.append({
                "is_folder": True,
                "folder_name": folder,
                "folder_items": folder_items
            })
            
    return sidebar

def compile_docs(docs_dir: Path, dist_dir: Path, templates_dir: Path, static_src_dir: Path):
    """
    Scans docs_dir, parses Markdown to HTML, and writes output to dist_dir.
    """
    # 1. Recreate clean dist directory
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    dist_dir.mkdir(parents=True, exist_ok=True)
    
    # 2. Copy static files
    dist_static_dir = dist_dir / "static"
    dist_static_dir.mkdir(parents=True, exist_ok=True)
    if static_src_dir.exists() and static_src_dir.is_dir():
        for item in static_src_dir.iterdir():
            if item.is_file():
                shutil.copy(item, dist_static_dir / item.name)
                
    # 3. Setup Jinja2 environment
    jinja_env = jinja2.Environment(
        loader=jinja2.FileSystemLoader(str(templates_dir)),
        autoescape=True
    )
    try:
        template = jinja_env.get_template("layout.html")
    except Exception as e:
        print(f"Error loading template layout.html: {e}")
        return
        
    # Setup markdown parser
    md = markdown.Markdown(extensions=["fenced_code", "tables", "toc"])
    
    # 4. Gather all markdown files to process
    all_md_files = []
    for root, _, files in os.walk(docs_dir):
        for file in files:
            if file.endswith(".md"):
                all_md_files.append(Path(root) / file)
                
    # 5. Compile each file
    for md_path in all_md_files:
        # Determine relative path from docs_dir
        rel_to_docs = md_path.relative_to(docs_dir)
        
        # Determine output html relative path
        if rel_to_docs.name == "README.md":
            html_rel_path = rel_to_docs.parent / "index.html"
        else:
            html_rel_path = rel_to_docs.with_suffix(".html")
            
        html_rel_path_str = html_rel_path.as_posix()
        
        # Calculate relative path back to root (for style.css linking)
        depth = len(html_rel_path.parents) - 1
        relative_path_to_root = "../" * depth
        
        # Read and convert markdown
        try:
            markdown_content = md_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"Error reading {md_path}: {e}")
            continue
            
        # Parse title (use first h1 header if available, otherwise filename mapping)
        title = get_title_for_file(md_path.name)
        lines = markdown_content.splitlines()
        for line in lines[:3]:
            if line.startswith("# "):
                title = line[2:].strip()
                break
                
        html_content = md.convert(markdown_content)
        md.reset()  # Reset state between conversions
        
        # Build sidebar navigation
        sidebar_nav = build_sidebar_nav(docs_dir, html_rel_path_str)
        
        # Render page
        rendered_html = template.render(
            title=title,
            content=html_content,
            sidebar_nav=sidebar_nav,
            relative_path_to_root=relative_path_to_root
        )
        
        # Write file
        out_path = dist_dir / html_rel_path
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(rendered_html, encoding="utf-8")
        print(f"Compiled: {md_path} -> {out_path}")
        
    print("Static compilation completed successfully.")
