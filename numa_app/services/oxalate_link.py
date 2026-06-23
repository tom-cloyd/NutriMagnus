"""oxalate_link.py — prompt user to link a food to an oxalate reference record.

Called after displaying food analysis when the active profile has use_oxalate_data=True.
Silently returns if oxalate data is disabled, already resolved, or oxalate.db is missing.
"""

from __future__ import annotations

import oxalate as _ox
import db as _db
import profile as _profile
from .. import state
from ..ui.prompts import Cancelled, ReturnToMain, _prompt
from ..ui.common import section_title, table_footer


def maybe_show_oxalate(fdc_id: int, food_name: str) -> None:
    """Check oxalate status for fdc_id and display or prompt as appropriate.

    - Does nothing if the active profile has use_oxalate_data=False.
    - Does nothing if oxalate.db is not present.
    - If a confirmed link exists, displays the oxalate value.
    - If no_match was previously confirmed, does nothing.
    - Otherwise, searches for similar records and prompts the user to link or skip.
    """
    prof = _profile.load_profile()
    if not prof or not prof.use_oxalate_data:
        return
    if not _ox.is_available():
        return

    # Check for existing link
    with _db.get_db() as conn:
        link = _db.oxalate_link_get(conn, fdc_id)

    if link:
        if link["no_match"]:
            return  # user previously said no oxalate record applies
        if link["oxalate_food_id"] is not None:
            # Display the confirmed match
            with _ox.get_oxalate_db() as ox_conn:
                row = _ox.get_by_id(ox_conn, link["oxalate_food_id"])
            if row:
                _display_oxalate(food_name, row)
            return

    # No link yet — search for candidates
    try:
        with _ox.get_oxalate_db() as ox_conn:
            candidates = _ox.search_similar(ox_conn, food_name, top_n=5)
    except FileNotFoundError:
        return

    if not candidates:
        state.console.print(
            f"\n  [grey62]Oxalate: no reference data found for this food.[/grey62]"
        )
        with _db.get_db() as conn:
            _db.oxalate_link_save(conn, fdc_id, oxalate_food_id=None, no_match=True)
        return

    # Show candidates and prompt
    state.console.print(
        f"\n  [{state.T['hi']}]Oxalate data[/{state.T['hi']}]  "
        f"[grey62]Link this food to an oxalate reference record.[/grey62]"
    )
    for i, (score, row) in enumerate(candidates, 1):
        pct = f"{score:.0%}"
        state.console.print(
            f"  [{state.T['accent']}]{i}[/{state.T['accent']}]  "
            f"{row['food_name']}  [grey62]({pct} match)[/grey62]  "
            + _ox.format_oxalate(row),
            highlight=False,
        )
    state.console.print(
        f"  [grey62]n — none of these apply  "
        f"s — skip for now (will ask again)[/grey62]"
    )

    while True:
        try:
            raw = _prompt(
                f"Link [bold]{food_name}[/bold] to oxalate record"
                f"  [grey62](1–{len(candidates)} / n / s)[/grey62]"
            ).strip().lower()
        except Cancelled:
            return

        if raw == "s" or raw == "":
            return  # skip — no link saved, will ask again
        if raw == "n":
            with _db.get_db() as conn:
                _db.oxalate_link_save(conn, fdc_id, oxalate_food_id=None, no_match=True)
            state.console.print(
                f"  [grey62]Noted — will not ask about oxalate for this food again.[/grey62]"
            )
            return
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)

        try:
            idx = int(raw) - 1
            if not (0 <= idx < len(candidates)):
                raise ValueError
        except ValueError:
            state.console.print(
                f"[{state.T['warning']}]Enter a number 1–{len(candidates)}, n, or s.[/{state.T['warning']}]"
            )
            continue

        score, row = candidates[idx]
        state.console.print(
            f"\n  Selected: [bold]{row['food_name']}[/bold]  "
            + _ox.format_oxalate(row),
            highlight=False,
        )
        if row["serving_size"] and row["oxalate_mg_per_100g"] is None:
            state.console.print(
                f"  [{state.T['warning']}]Note:[/{state.T['warning']}]  Oxalate value is per "
                f"[bold]{row['serving_size']}[/bold], not per 100 g. "
                f"Volume-to-weight conversion may be needed for recipe scaling.",
                highlight=False,
            )

        try:
            confirm = _prompt(
                f"Use this record for [bold]{food_name}[/bold]?  [grey62](y / n)[/grey62]",
                choices=["y", "n"],
                default="y",
            ).strip().lower()
        except Cancelled:
            continue  # let user pick again

        if confirm == "y":
            with _db.get_db() as conn:
                _db.oxalate_link_save(
                    conn, fdc_id, oxalate_food_id=row["id"], no_match=False
                )
            state.console.print(
                f"  [{state.T['success']}]✓[/{state.T['success']}]  "
                f"Oxalate link saved for [bold]{food_name}[/bold]."
            )
            _display_oxalate(food_name, row)
            return
        # user said no — loop back and let them pick again


def _display_oxalate(food_name: str, row: object) -> None:
    """Print the confirmed oxalate record in a consistent format."""
    cat_label = _ox.category_label(row["category"])
    serving_note = f"  [grey62](per {row['serving_size']})[/grey62]" if row["serving_size"] else ""

    state.console.print(
        f"\n  [{state.T['hi']}]Oxalate:[/{state.T['hi']}]  "
        f"[bold]{row['food_name']}[/bold]  —  "
        f"{row['oxalate_mg_per_serving']:.1f} mg{serving_note}",
        highlight=False,
    )
    if row["oxalate_mg_per_100g"] is not None:
        state.console.print(
            f"  [grey62]Per 100 g: {row['oxalate_mg_per_100g']:.0f} mg[/grey62]  "
            f"  Category: [{state.T['accent']}]{cat_label}[/{state.T['accent']}]",
            highlight=False,
        )
    else:
        state.console.print(
            f"  Category: [{state.T['accent']}]{cat_label}[/{state.T['accent']}]  "
            f"[grey62](100g value not available — serving is volumetric)[/grey62]",
            highlight=False,
        )
    if row["directly_measured"]:
        state.console.print(f"  [grey62]* Directly measured value[/grey62]")
