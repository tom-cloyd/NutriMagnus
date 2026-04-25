"""
annotations.py — food annotation entry: GI estimates, DIAAS estimates, prep context.
Docs: README-numa-documentation.md
"""
import db as _db
from .. import state
from ..ui.common import _prompt_with_options, section_title
from ..ui.prompts import Cancelled, ReturnToMain, _prompt


def _prompt_gi_value(
    food_name: str, current: float | None
) -> tuple[float | None, int | None]:
    """Prompt user for a GI estimate.
    Returns (value, no_prompt_flag):
      (float, None)  — value entered
      (None, None)   — skip / Enter (ask again next time)
      (None, 1)      — never ask again
    Raises Cancelled on b, ReturnToMain on m, SystemExit on q.
    """
    current_hint = f" [dim](current: {current:.0f})[/dim]" if current is not None else ""
    state.console.print(
        f"\n  [dim]Glycemic index: how quickly this food raises blood sugar.[/dim]\n"
        f"  [dim]Scale 0–100  (glucose = 100).  Low < 55 · medium 55–69 · high ≥ 70.[/dim]"
    )
    while True:
        raw = _prompt(
            f"GI for [bold]{food_name}[/bold]{current_hint}"
            f"  [dim](0–100, Enter/s=skip, x=never ask, b=back)[/dim]"
        ).strip().lower()
        if raw == "b":
            raise Cancelled
        if raw in ("", "s"):
            return None, None
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)
        if raw == "x":
            return None, 1
        try:
            val = float(raw)
            if 0.0 <= val <= 100.0:
                return val, None
            state.console.print(f"[{state.T['warning']}]GI must be 0–100.[/{state.T['warning']}]")
        except ValueError:
            state.console.print(
                f"[{state.T['warning']}]Enter a number (0–100), s to skip, or x to never ask.[/{state.T['warning']}]"
            )


def _prompt_diaas_value(
    food_name: str, current: float | None
) -> tuple[float | None, int | None]:
    """Same pattern as _prompt_gi_value but for DIAAS (0.0–1.5+)."""
    current_hint = f" [dim](current: {current:.2f})[/dim]" if current is not None else ""
    state.console.print(
        f"\n  [dim]DIAAS: Digestible Indispensable Amino Acid Score — protein quality.[/dim]\n"
        f"  [dim]Scale 0–1.0+  (1.0 = complete).  Whole grains typically 0.4–0.6.[/dim]"
    )
    while True:
        raw = _prompt(
            f"DIAAS for [bold]{food_name}[/bold]{current_hint}"
            f"  [dim](0.0–1.5, Enter/s=skip, x=never ask, b=back)[/dim]"
        ).strip().lower()
        if raw == "b":
            raise Cancelled
        if raw in ("", "s"):
            return None, None
        if raw == "m":
            raise ReturnToMain()
        if raw == "q":
            raise SystemExit(0)
        if raw == "x":
            return None, 1
        try:
            val = float(raw)
            if 0.0 <= val <= 2.0:
                return val, None
            state.console.print(f"[{state.T['warning']}]DIAAS should be 0–2.0.[/{state.T['warning']}]")
        except ValueError:
            state.console.print(
                f"[{state.T['warning']}]Enter a decimal (0.0–1.5), s to skip, or x to never ask.[/{state.T['warning']}]"
            )


def _show_annotation_status(
    gi: float | None,
    gi_no_prompt: int,
    diaas: float | None,
    diaas_no_prompt: int,
    prep: str | None,
) -> None:
    s = state.T["success"]

    def _field(label: str, display: str | None, no_prompt: int) -> str:
        if display is not None:
            return f"[{s}]{label}: {display}[/{s}]"
        if no_prompt:
            return f"[dim]{label}: — (prompts off)[/dim]"
        return f"[dim]{label}: not set[/dim]"

    gi_str    = _field("GI",    f"{gi:.0f}"    if gi    is not None else None, gi_no_prompt)
    diaas_str = _field("DIAAS", f"{diaas:.2f}" if diaas is not None else None, diaas_no_prompt)
    prep_str  = f"[dim]Prep: {prep}[/dim]" if prep else "[dim]Prep: not set[/dim]"
    state.console.print(f"  {gi_str}   {diaas_str}   {prep_str}\n")


def annotate_food_interactive(fdc_id: int, food_name: str) -> None:
    """Full annotation UI for a cached food: edit GI, DIAAS, prep context."""
    while True:
        with _db.get_db() as conn:
            ann = _db.get_food_annotation(conn, fdc_id)

        gi          = ann["gi_estimate"]    if ann else None
        gi_nop      = ann["gi_no_prompt"]   if ann else 0
        diaas       = ann["diaas_estimate"] if ann else None
        diaas_nop   = ann["diaas_no_prompt"] if ann else 0
        prep        = ann["prep_context"]   if ann else None

        section_title(f"Annotate: {food_name}")
        _show_annotation_status(gi, gi_nop, diaas, diaas_nop, prep)

        def _val_hint(val, fmt) -> str:
            return f"  [dim](currently: {fmt(val)})[/dim]" if val is not None else ""

        options: list[tuple[str, str]] = [
            ("1", f"Set GI estimate{_val_hint(gi, lambda v: f'{v:.0f}')}"),
            ("2", f"Set DIAAS estimate{_val_hint(diaas, lambda v: f'{v:.2f}')}"),
            ("3", f"Set prep context{_val_hint(prep, lambda v: v)}"),
        ]
        if gi_nop or diaas_nop:
            options.append(("r", "Re-enable prompts  [dim](clear 'never ask' flags)[/dim]"))
        if ann is not None:
            options.append(("c", "Clear all annotations for this food"))

        try:
            action = _prompt_with_options("Action", options, default="1")
        except Cancelled:
            return

        if not action or action == "b":
            return
        if action == "m":
            raise ReturnToMain()
        if action == "q":
            raise SystemExit(0)

        if action == "1":
            try:
                val, no_prompt = _prompt_gi_value(food_name, gi)
            except Cancelled:
                continue
            with _db.get_db() as conn:
                _db.upsert_food_annotation(conn, fdc_id, gi_estimate=val, gi_no_prompt=no_prompt)
            if val is not None:
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  GI set to {val:.0f}.")
            elif no_prompt:
                state.console.print("  [dim]Will not prompt for GI for this food again.[/dim]")

        elif action == "2":
            try:
                val, no_prompt = _prompt_diaas_value(food_name, diaas)
            except Cancelled:
                continue
            with _db.get_db() as conn:
                _db.upsert_food_annotation(conn, fdc_id, diaas_estimate=val, diaas_no_prompt=no_prompt)
            if val is not None:
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  DIAAS set to {val:.2f}.")
            elif no_prompt:
                state.console.print("  [dim]Will not prompt for DIAAS for this food again.[/dim]")

        elif action == "3":
            try:
                raw = _prompt(
                    f"Prep context for [bold]{food_name}[/bold]  [dim](Enter/b=back)[/dim]",
                    default=prep or "", prefill=bool(prep),
                ).strip()
            except Cancelled:
                continue
            if raw.lower() == "b" or (not raw and not prep):
                continue
            if raw.lower() == "m":
                raise ReturnToMain()
            if raw.lower() == "q":
                raise SystemExit(0)
            with _db.get_db() as conn:
                _db.upsert_food_annotation(conn, fdc_id, prep_context=raw or None)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Prep context saved.")

        elif action == "r":
            with _db.get_db() as conn:
                _db.upsert_food_annotation(conn, fdc_id, gi_no_prompt=0, diaas_no_prompt=0)
            state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Prompts re-enabled.")

        elif action == "c":
            try:
                confirm = _prompt(
                    f"Clear all annotations for [bold]{food_name}[/bold]?  [dim](y/N)[/dim]",
                    choices=["y", "n"], default="n",
                )
            except Cancelled:
                continue
            if confirm == "y":
                with _db.get_db() as conn:
                    conn.execute("DELETE FROM food_annotations WHERE fdc_id = ?", (fdc_id,))
                state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  Annotations cleared.")
                return


def maybe_prompt_gi(fdc_id: int, food_name: str) -> float | None:
    """Inline: return existing GI estimate, or prompt if missing and not suppressed.
    Returns the value (saved or pre-existing), or None if unavailable / skipped.
    Raises Cancelled / ReturnToMain / SystemExit if the user navigates away."""
    with _db.get_db() as conn:
        ann = _db.get_food_annotation(conn, fdc_id)
    if ann is not None and ann["gi_estimate"] is not None:
        return float(ann["gi_estimate"])
    if ann is not None and ann["gi_no_prompt"]:
        return None

    state.console.print(f"\n  [dim]No GI estimate on file for [bold]{food_name}[/bold].[/dim]")
    val, no_prompt = _prompt_gi_value(food_name, None)
    with _db.get_db() as conn:
        _db.upsert_food_annotation(conn, fdc_id, gi_estimate=val, gi_no_prompt=no_prompt)
    if val is not None:
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  GI {val:.0f} saved.")
    elif no_prompt:
        state.console.print("  [dim]GI prompts disabled for this food.[/dim]")
    return val


def maybe_prompt_diaas(fdc_id: int, food_name: str) -> float | None:
    """Inline: return existing DIAAS estimate, or prompt if missing and not suppressed.
    Returns the value (saved or pre-existing), or None if unavailable / skipped.
    Raises Cancelled / ReturnToMain / SystemExit if the user navigates away."""
    with _db.get_db() as conn:
        ann = _db.get_food_annotation(conn, fdc_id)
    if ann is not None and ann["diaas_estimate"] is not None:
        return float(ann["diaas_estimate"])
    if ann is not None and ann["diaas_no_prompt"]:
        return None

    state.console.print(f"\n  [dim]No DIAAS estimate on file for [bold]{food_name}[/bold].[/dim]")
    val, no_prompt = _prompt_diaas_value(food_name, None)
    with _db.get_db() as conn:
        _db.upsert_food_annotation(conn, fdc_id, diaas_estimate=val, diaas_no_prompt=no_prompt)
    if val is not None:
        state.console.print(f"  [{state.T['success']}]✓[/{state.T['success']}]  DIAAS {val:.2f} saved.")
    elif no_prompt:
        state.console.print("  [dim]DIAAS prompts disabled for this food.[/dim]")
    return val
