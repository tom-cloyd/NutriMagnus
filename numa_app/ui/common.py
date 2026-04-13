import os
import subprocess
import tempfile

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

def _open_in_editor(text: str = "") -> str:
    """
    Open `text` in the user's configured editor and return the edited result.
    Editor is resolved in order: state._editor_command → $VISUAL → $EDITOR → nano → vi.
    Returns the original text unchanged if the editor cannot be launched.
    """
    cmd = str(getattr(state, "_editor_command", "") or "").strip()
    if not cmd:
        cmd = os.environ.get("VISUAL") or os.environ.get("EDITOR") or ""
    if not cmd:
        # last-resort fallbacks
        for fallback in ("nano", "vi"):
            if subprocess.run(["which", fallback], capture_output=True).returncode == 0:
                cmd = fallback
                break
    if not cmd:
        state.console.print(
            f"  [{state.T['warning']}]No editor found. Set one under Settings → Editor command.[/{state.T['warning']}]"
        )
        return text

    suffix = ".txt"
    try:
        with tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False) as tf:
            tf.write(text)
            tf_path = tf.name
        # Split to handle commands like "code --wait"
        cmd_parts = cmd.split() + [tf_path]
        subprocess.run(cmd_parts, check=False)
        with open(tf_path, encoding="utf-8") as f:
            result = f.read()
    except Exception as exc:
        state.console.print(
            f"  [{state.T['warning']}]Editor error: {exc}[/{state.T['warning']}]"
        )
        return text
    finally:
        try:
            os.unlink(tf_path)
        except OSError:
            pass
    return result


def _prompt_with_options(
    prompt_label: str,
    options: list[tuple[str, str]],
    *,
    default: str = "",
) -> str:
    """Show explicit option lines above a prompt, then collect a choice."""
    state.console.print()
    state.console.print("  Options:")
    for key, desc in options:
        state.console.print(f"    {key:<5} {desc}", highlight=False)
    state.console.print()
    from .prompts import _prompt
    return _prompt(prompt_label, default=default).strip().lower()
