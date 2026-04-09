from .. import state
from .prompts import Cancelled

def _show_menu(title: str, items: list[tuple[str, str]]) -> None:
    """Render a numbered/lettered menu with a title."""
    state.console.print(f"\n[{state.T['accent']}]{title}[/{state.T['accent']}]")
    state.console.rule()
    for key, label in items:
        if key.isdigit():
            state.console.print(f"  [{state.T['accent']}]{key}.[/{state.T['accent']}] {label}", highlight=False)
        else:
            state.console.print(f"  [dim]{key}.[/dim] {label}", highlight=False)
    state.console.print()


def _safe_call(fn, *args):
    try:
        fn(*args)
    except SystemExit as e:
        if e.code == 0:
            raise
    except Cancelled:
        state.console.print("[dim]Cancelled.[/dim]")
