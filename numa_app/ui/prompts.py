"""
prompts.py — _prompt() and input primitives: Cancelled, ReturnToMain, _ask_float/int/date.
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/prompts.py — input primitives"
"""
import readline
import select as _select
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
_history: list[str] = []
_MAX_HISTORY = 100


def _read_escape_seq() -> str:
    """Read the bytes that follow an ESC character.
    Returns the sequence string (usually '[A'–'[D' for arrow keys), or '' if
    nothing arrives within the timeout (bare ESC key press).
    Drains any extended bytes beyond the first two so they never leak into the
    next prompt (e.g. ESC[1;5D sent by some terminals for ctrl+arrow)."""
    r, _, _ = _select.select([sys.stdin], [], [], 0.15)
    if not r:
        return ""
    seq = sys.stdin.read(2)
    while True:
        r2, _, _ = _select.select([sys.stdin], [], [], 0.02)
        if not r2:
            break
        sys.stdin.read(1)
    return seq


def _show_help(ref: str) -> None:
    """Display a user-manual section for ref. Silently no-ops if manual not available."""
    try:
        import manual as _manual
        _manual.show(ref)
    except Exception:
        state.console.print(f"  [dim]Help not available.[/dim]")


def _prompt(prompt_text: str, *, default: Any = _NO_DEFAULT, choices: list[str] | None = None, prefill: bool = False, free_text: bool = False, two_line: bool = False) -> str:
    """Unified input primitive. choices=list enables single-keypress mode (only listed chars accepted).
    free_text=True uses readline so arrow-keys/editing work. prefill=True pre-populates with default.
    two_line=True (requires prefill=True) prints the label on its own line and the editable value below.
    Raises Cancelled on Ctrl+C / Escape. Never use bare input() — always use this.
    In interactive (tty) mode, any input starting with ? performs a manual lookup and re-prompts."""
    while True:
        result = _prompt_once(prompt_text, default=default, choices=choices, prefill=prefill, free_text=free_text, two_line=two_line)
        if not sys.stdin.isatty() or choices or not result.startswith("?"):
            return result
        _show_help(result[1:].strip() or "help")


def _prompt_once(prompt_text: str, *, default: Any = _NO_DEFAULT, choices: list[str] | None = None, prefill: bool = False, free_text: bool = False, two_line: bool = False) -> str:
    """Single-shot input — called by _prompt(); do not call directly."""
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

    if prefill and default is not _NO_DEFAULT and default not in ("", None) and not choices:
        if two_line:
            state.console.print(f"  {prompt_text}:", highlight=False)
            # No separate indent print — input() owns the indent so readline
            # knows the prompt length and keeps cursor arithmetic correct.
        else:
            state.console.print(f"{prompt_text}: ", end="", highlight=False)
        sys.stdout.flush()
        _prefill_text = str(default)

        def _hook() -> None:
            readline.insert_text(_prefill_text)
            readline.redisplay()

        readline.set_pre_input_hook(_hook)
        _input_prompt = "  " if two_line else ""
        try:
            result = input(_input_prompt)
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
            # Discard any bytes that accumulated in the OS input queue before
            # this prompt was reached (e.g. from a Rich spinner or prior prompt).
            termios.tcflush(fd, termios.TCIFLUSH)
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
                    if not _read_escape_seq():
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

    global _history
    buf: list[str] = []
    hist_pos = len(_history)  # one past end = current (unsaved) input
    saved_buf: list[str] = []
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
                seq = _read_escape_seq()
                if not seq:
                    state.console.print()
                    raise Cancelled
                if seq == "[A":  # up arrow — go back in history
                    if hist_pos > 0:
                        if hist_pos == len(_history):
                            saved_buf = buf[:]
                        hist_pos -= 1
                        sys.stdout.write("\b \b" * len(buf))
                        buf = list(_history[hist_pos])
                        sys.stdout.write("".join(buf))
                        sys.stdout.flush()
                elif seq == "[B":  # down arrow — go forward in history
                    if hist_pos < len(_history):
                        hist_pos += 1
                        sys.stdout.write("\b \b" * len(buf))
                        buf = saved_buf[:] if hist_pos == len(_history) else list(_history[hist_pos])
                        sys.stdout.write("".join(buf))
                        sys.stdout.flush()
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
    if len(result) >= 3 and (_history and _history[-1] != result or not _history):
        _history.append(result)
        if len(_history) > _MAX_HISTORY:
            _history.pop(0)
    if result == "" and default is not _NO_DEFAULT and default not in (None,):
        return str(default)
    return result


def _ask_float(prompt_text: str, *, default: float | None = None) -> float | None:
    """Prompt for a float; returns None on empty/b (back). Raises ReturnToMain on m, SystemExit on q."""
    while True:
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


def _ask_int(prompt_text: str, *, default: int | None = None) -> int | None:
    """Prompt for an int; returns None on empty/b (back). Raises ReturnToMain on m, SystemExit on q."""
    while True:
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
