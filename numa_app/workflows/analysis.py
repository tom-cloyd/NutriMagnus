"""
analysis.py — Analysis menu: dispatches to preset analyses (daily summary, food use in meals).
Docs: README-numa-documentation.md, Menu Structure: "4. Analysis"
"""
from .. import state
from ..ui.common import _safe_call, _show_menu
from ..ui.prompts import Cancelled, _prompt
from .food_use import _do_food_use_analysis
from .summary import _menu_daily_summary


def _menu_analysis() -> bool:
    """Analysis submenu. Returns True to go back, False to quit."""
    while True:
        _show_menu("Analysis", [
            ("1", "Daily summary - DCP and goals"),
            ("2", "Food use in meals"),
            ("m", "Return to main menu"),
            ("q", "Quit"),
        ])
        try:
            choice = _prompt("Choice").strip().lower()
        except Cancelled:
            state.console.print("[grey62]Cancelled.[/grey62]")
            return True

        if choice == "1":
            if not _menu_daily_summary():
                return False
        elif choice == "2":
            _safe_call(_do_food_use_analysis)
        elif choice == "m":
            return True
        elif choice == "q":
            return False
        else:
            state.console.print(f"[{state.T['warning']}]Please enter a valid option.[/{state.T['warning']}]")
