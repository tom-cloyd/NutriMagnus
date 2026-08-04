"""
manual_build.py — regenerate user-manual.html from user-manual.md when stale.
Used by the web app's /manual route. Docs: README-numa-documentation.md, Project Structure
"""
from pathlib import Path

_PROJECT_ROOT = Path(__file__).parent.parent.parent


def rebuild_manual_if_stale() -> None:
    """Silently regenerate user-manual.html if the markdown source is newer."""
    md   = _PROJECT_ROOT / "user-manual.md"
    html = _PROJECT_ROOT / "user-manual.html"
    if not md.exists():
        return
    if html.exists() and html.stat().st_mtime >= md.stat().st_mtime:
        return
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "build_manual", _PROJECT_ROOT / "scripts" / "build_manual.py"
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        mod.main()
    except Exception:
        pass
