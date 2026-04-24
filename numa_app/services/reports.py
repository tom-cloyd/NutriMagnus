"""
reports.py — auto-save and user-export of nutrition reports (Markdown, txt, HTML).
Docs: README-numa-documentation.md, Project Structure
"""
import pathlib

from rich.markdown import Markdown

import export as _export
from .. import state
from ..ui.prompts import Cancelled, _prompt
from ..ui.common import _prompt_with_options

_AUTO_SAVE_DIR = pathlib.Path("~/.numa/reports").expanduser()
_USER_EXPORT_DIR = pathlib.Path("~/.numa/user-requested-nutrition-reports").expanduser()

def _find_existing_reports(report_title: str) -> list[pathlib.Path]:
    """Return saved reports matching report_title, newest first."""
    prefix = _export.safe_title(report_title)
    matches = sorted(_AUTO_SAVE_DIR.glob(f"{prefix}_*.md"), reverse=True)
    return matches


def _offer_export(report_title: str, sections: list[dict]) -> None:
    """Check for existing reports, auto-save, and offer an additional export copy."""
    existing = _find_existing_reports(report_title)
    if existing:
        state.console.print("\n  [dim]Previous reports:[/dim]")
        state.console.print(f"  [thistle1]{_AUTO_SAVE_DIR.resolve()}[/thistle1]")
        for i, p in enumerate(existing, 1):
            state.console.print(f"  [dim]  {i}. [/dim][thistle1]{p.name}[/thistle1]")
        try:
            ans = _prompt_with_options(
                "Report option",
                [
                    ("1-N", "View selected report"),
                    ("new", "Save a new report"),
                    ("Enter", "Skip and return"),
                ],
                default="",
            )
        except Cancelled:
            return
        if ans.isdigit():
            idx = int(ans) - 1
            if 0 <= idx < len(existing):
                state.console.print()
                state.console.print(Markdown(existing[idx].read_text(encoding="utf-8")))
            return
        if ans != "new":
            return

    # Auto-save
    auto_name = _export.default_filename(report_title, "md")
    auto_path = _AUTO_SAVE_DIR / auto_name
    _export.write_report(auto_path, _export.build_report(report_title, sections, "md", diet_pref=state._diet_pref))
    state.console.print(f"  [dim]Report auto-saved →[/dim] [thistle1]{auto_path.resolve()}[/thistle1]")

    try:
        ans = _prompt_with_options(
            "Export option",
            [
                ("txt", "Export as plain text"),
                ("md", "Export as markdown"),
                ("html", "Export as HTML"),
                ("Enter", "Skip"),
            ],
            default="",
        )
    except Cancelled:
        return
    if ans not in ("txt", "md", "html"):
        return
    default = _export.default_filename(report_title, ans)
    try:
        fname = _prompt(
            f"Filename  [dim](Enter=use {default})[/dim]",
            default=default,
        ).strip()
    except Cancelled:
        return
    if not fname:
        fname = default
    path = _USER_EXPORT_DIR / pathlib.Path(fname).name
    content = _export.build_report(report_title, sections, ans, diet_pref=state._diet_pref)
    _export.write_report(path, content)
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {path.resolve()}")
