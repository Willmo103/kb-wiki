from pathlib import Path
import typer
import uvicorn
from kb_wiki.compiler import compile_docs
from kb_wiki.server import setup_server

app = typer.Typer(help="kb-wiki - Static wiki compiler and live server for the kb stack")

@app.command()
def build(
    docs: Path = typer.Option(Path("docs"), help="Path to markdown docs directory"),
    dist: Path = typer.Option(Path("dist"), help="Path to output static site directory"),
):
    """Compiles the Markdown documentation into static HTML files."""
    package_dir = Path(__file__).resolve().parent
    templates_dir = package_dir / "templates"
    static_src_dir = package_dir / "static"
    
    if not docs.exists():
        typer.echo(f"Error: Docs directory '{docs}' does not exist.")
        raise typer.Exit(code=1)
        
    typer.echo(f"Compiling markdown documentation from '{docs}' -> '{dist}'...")
    try:
        compile_docs(docs, dist, templates_dir, static_src_dir)
        typer.echo("Build succeeded!")
    except Exception as e:
        import traceback
        traceback.print_exc()
        typer.echo(f"Build failed: {e}")
        raise typer.Exit(code=1)

@app.command()
def serve(
    docs: Path = typer.Option(Path("docs"), help="Path to markdown docs directory"),
    dist: Path = typer.Option(Path("dist"), help="Path to output static site directory"),
    host: str = typer.Option("127.0.0.1", help="Host address to run the server on"),
    port: int = typer.Option(8000, help="Port to run the server on"),
    dev: bool = typer.Option(False, "--dev", help="Enable developer mode (filesystem watcher & auto-rebuild)"),
):
    """Starts the FastAPI web server to host the static documentation site."""
    package_dir = Path(__file__).resolve().parent
    templates_dir = package_dir / "templates"
    static_src_dir = package_dir / "static"
    
    if not docs.exists():
        typer.echo(f"Error: Docs directory '{docs}' does not exist.")
        raise typer.Exit(code=1)
        
    try:
        setup_server(docs, dist, templates_dir, static_src_dir, dev_mode=dev)
        typer.echo(f"Serving documentation at http://{host}:{port}")
        uvicorn.run("kb_wiki.server:app", host=host, port=port, log_level="info")
    except Exception as e:
        typer.echo(f"Server error: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()
