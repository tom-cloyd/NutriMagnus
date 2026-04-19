"""
prompts.py — _prompt() and input primitives: Cancelled, ReturnToMain, _ask_float/int/date.
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/prompts.py — input primitives"
"""
import readline
import sys
import termios
import tty
from datetime import date, datetime
from typing import Any

from .. import state


class Cancelled(Exception):
    """Raised when the user presses Ctrl+C or Escape at any prompt."""


class ReturnToMain(Exception):
    """Raised when the user chooses 'm' to jump directly back to the main menu."""


_NO_DEFAULT = object()


def _prompt(prompt_text: str, *, default: Any = _NO_DEFAULT, choices: list[str] | None = None, prefill: bool = False, free_text: bool = False) -> str:
    """Unified input primitive. choices=list enables single-keypress mode (only listed chars accepted).
    free_text=True uses readline so arrow-keys/editing work. prefill=True pre-populates with default.
    Raises Cancelled on Ctrl+C / Escape. Never use bare input() — always use this."""
    if not sys.stdin.isatty():
        from rich.prompt import Prompt
        kw: dict = {} if default is _NO_DEFAULT else {"default": default}
        if choices:
            kw["choices"] = choices
        try:
            return Prompt.ask(prompt_text, **kw, console=state.console)
        except KeyboardInterrupt:
            sys.stdout.write("\n")
            sys.stdout.flush()
            raise Cancelled

    # free_text=True: use readline-based input so arrow keys, cursor movement,
    # and editing work properly.  Also used by the prefill path.
    if free_text and not choices:
        _default_str = str(default) if default is not _NO_DEFAULT and default not in (None,) else ""
        if _default_str:
            hint = (
                f" (Press enter to keep"
                f" [{state.T['default_hint']}]{_default_str}[/{state.T['default_hint']}])"
            )
        else:
            hint = ""
        state.console.print(f"{prompt_text}{hint}: ", end="", highlight=False)
        sys.stdout.flush()
        try:
            result = input("")
        except (KeyboardInterrupt, EOFError):
            state.console.print()
            raise Cancelled
        result = result.strip()
        return result if result else _default_str

    if prefill and default is not _NO_DEFAULT and default not in ("", None) and not choices:
        state.console.print(f"{prompt_text}: ", end="", highlight=False)
        sys.stdout.flush()
        _prefill_text = str(default)

        def _hook() -> None:
            readline.insert_text(_prefill_text)
            readline.redisplay()

        readline.set_pre_input_hook(_hook)
        try:
            result = input("")
        except (KeyboardInterrupt, EOFError):
            state.console.print()
            raise Cancelled
        finally:
            readline.set_pre_input_hook(None)
        return result.strip() or default

    hint_parts = []
    if choices:
        hint_parts.append(f"[{state.T['choice']}]({'|'.join(choices)})[/{state.T['choice']}]")
    if default is not _NO_DEFAULT and default not in ("", None):
        hint_parts.append(
            f"(Press enter to keep [{state.T['default_hint']}]{default}[/{state.T['default_hint']}])"
        )
    hint = (" " + " ".join(hint_parts)) if hint_parts else ""
    state.console.print(f"{prompt_text}{hint}: ", end="", highlight=False)
    sys.stdout.flush()

    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)

    # When choices are given, use single-keypress mode: only accept a valid
    # choice character or Enter (to select the default).  All other input is
    # silently ignored so the user cannot accidentally submit garbage text.
    if choices:
        choices_lower = [c.lower() for c in choices]
        try:
            tty.setcbreak(fd)
            while True:
                try:
                    ch = sys.stdin.read(1)
                except KeyboardInterrupt:
                    state.console.print()
                    raise Cancelled
                if ch in ("\x03", "\x04"):
                    state.console.print()
                    raise Cancelled
                if ch == "\x1b":
                    import select as _sel
                    r, _, _ = _sel.select([sys.stdin], [], [], 0.05)
                    if r:
                        sys.stdin.read(2)
                    else:
                        state.console.print()
                        raise Cancelled
                    continue
                if ch in ("\r", "\n"):
                    # Empty Enter → use default if available, else keep waiting.
                    if default is not _NO_DEFAULT and default not in (None,):
                        state.console.print()
                        return str(default)
                    continue
                ch_low = ch.lower()
                if ch_low in choices_lower:
                    sys.stdout.write(ch_low)
                    sys.stdout.flush()
                    state.console.print()
                    return ch_low
                # Invalid character: ignore silently.
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    buf: list[str] = []
    try:
        tty.setcbreak(fd)
        while True:
            try:
                ch = sys.stdin.read(1)
            except KeyboardInterrupt:
                state.console.print()
                raise Cancelled
            if ch in ("\x03", "\x04"):
                state.console.print()
                raise Cancelled
            if ch == "\x1b":
                import select as _sel
                r, _, _ = _sel.select([sys.stdin], [], [], 0.05)
                if r:
                    sys.stdin.read(2)
                else:
                    state.console.print()
                    raise Cancelled
                continue
            if ch in ("\r", "\n"):
                state.console.print()
                break
            if ch in ("\x7f", "\x08"):
                if buf:
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                continue
            if ch.isprintable():
                buf.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    result = "".join(buf).strip()
    if result == "" and default is not _NO_DEFAULT and default not in (None,):
        return str(default)
    return result


def _ask_float(prompt_text: str, *, default: float | None = None) -> float | None:
    """Prompt for a float; returns None on empty/b (back). Raises ReturnToMain on m, SystemExit on q."""
    d = str(default) if default is not None else _NO_DEFAULT
    raw = _prompt(f"{prompt_text}  (b=back, m=main, q=quit)", default=d).strip().lower()
    if not raw or raw == "b":
        return None
    if raw == "m":
        raise ReturnToMain()
    if raw == "q":
        raise SystemExit(0)
    try:
        return float(raw)
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Not a number — try again.[/{state.T['warning']}]")
        return None


def _ask_int(prompt_text: str, *, default: int | None = None) -> int | None:
    """Prompt for an int; returns None on empty/b (back). Raises ReturnToMain on m, SystemExit on q."""
    d = str(default) if default is not None else _NO_DEFAULT
    raw = _prompt(f"{prompt_text}  (b=back, m=main, q=quit)", default=d).strip().lower()
    if not raw or raw == "b":
        return None
    if raw == "m":
        raise ReturnToMain()
    if raw == "q":
        raise SystemExit(0)
    try:
        return int(raw)
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Not an integer — try again.[/{state.T['warning']}]")
        return None


def _ask_date(prompt_text: str, *, default: str | None = None) -> str | None:
    """Prompt for a YYYY-MM-DD date string; returns None on invalid input (caller should retry)."""
    today = date.today().isoformat()
    raw = _prompt(prompt_text, default=default or today).strip()
    if not raw:
        return today
    try:
        datetime.strptime(raw, "%Y-%m-%d")
        return raw
    except ValueError:
        state.console.print(f"[{state.T['warning']}]Use YYYY-MM-DD format.[/{state.T['warning']}]")
        return None
