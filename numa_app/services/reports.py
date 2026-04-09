import pathlib

from rich.markdown import Markdown

import export as _export
from .. import state
from ..ui.prompts import Cancelled, _prompt

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
        state.console.print(f"  [dim]{_AUTO_SAVE_DIR.resolve()}[/dim]")
        for i, p in enumerate(existing, 1):
            state.console.print(f"  [dim]  {i}. {p.name}[/dim]")
        try:
            ans = _prompt(
                "Choice  [dim](1-N=view selected report · new=save new · Enter=skip)[/dim]",
                default="",
            ).strip().lower()
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
    _export.write_report(auto_path, _export.build_report(report_title, sections, "md"))
    state.console.print(f"  [dim]Report auto-saved → {auto_path.resolve()}[/dim]")

    try:
        ans = _prompt(
            "Choice  [dim](txt=export text · md=export markdown · html=export html · Enter=skip)[/dim]",
            default="",
        ).strip().lower()
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
    content = _export.build_report(report_title, sections, ans)
    _export.write_report(path, content)
    state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}] Saved: {path.resolve()}")
