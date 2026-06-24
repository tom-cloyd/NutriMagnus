"""
prompts.py — _prompt() and input primitives: Cancelled, ReturnToMain, _ask_float/int/date.
Docs: README-numa-documentation.md, Architecture: "numa_app/ui/prompts.py — input primitives"
"""
import os as _os
import readline
import select as _select
import sys
import termios
import tty
from datetime import date, datetime
from pathlib import Path
from typing import Any

from .. import state


class Cancelled(Exception):
    """Raised when the user presses Ctrl+C or Escape at any prompt."""


class ReturnToMain(Exception):
    """Raised when the user chooses 'm' to jump directly back to the main menu."""


_NO_DEFAULT = object()

# ── Input history (Up/Down arrow recall at prompts) ─────────────────────────
_input_history: list[str] = []
_HISTORY_FILE = Path.home() / ".numa_history"


def _load_input_history() -> None:
    if _HISTORY_FILE.exists():
        try:
            entries = _HISTORY_FILE.read_text().splitlines()
            # Skip single-char entries — they are navigation keys (b/m/q/y/n), never
            # useful to recall, and pollute history so up-arrow retrieves them instead
            # of real search terms.
            _input_history.extend(e for e in entries if len(e) > 1)
            if len(_input_history) > 1000:
                del _input_history[:-1000]
        except OSError:
            pass


def _append_input_history(entry: str) -> None:
    if len(entry) <= 1:
        return  # single-char nav keys (b/m/q/y/n) are not worth recalling
    if _input_history and _input_history[-1] == entry:
        return  # skip consecutive duplicates
    _input_history.append(entry)
    try:
        with open(_HISTORY_FILE, "a") as fh:
            fh.write(entry + "\n")
    except OSError:
        pass


def _read_escape_seq() -> str:
    """Read the bytes that follow an ESC character.
    Returns the sequence string (usually '[A'–'[D' for arrow keys), or '' if
    nothing arrives within the timeout (bare ESC key press).
    Drains any extended bytes beyond the first two so they never leak into the
    next prompt (e.g. ESC[1;5D sent by some terminals for ctrl+arrow).

    Uses os.read() directly on the file descriptor to bypass Python's IO
    buffering layers entirely — avoids race conditions with TextIOWrapper and
    BufferedReader internal buffers."""
    fd = sys.stdin.fileno()
    r, _, _ = _select.select([fd], [], [], 0.15)
    if not r:
        return ""
    try:
        chunk = _os.read(fd, 16)
    except OSError:
        return ""
    # Drain any remaining extended sequence bytes (e.g. ESC[1;5D for ctrl+arrow)
    while True:
        r2, _, _ = _select.select([fd], [], [], 0.02)
        if not r2:
            break
        try:
            _os.read(fd, 16)
        except OSError:
            break
    return chunk[:2].decode("ascii", errors="replace")


def _show_help(ref: str) -> None:
    """Display a user-manual section for ref. Silently no-ops if manual not available."""
    try:
        import manual as _manual
        _manual.show(ref)
    except Exception:
        state.console.print(f"  [grey62]Help not available.[/grey62]")


def _hint(n: int) -> str:
    """Quick-select hint for a numbered result list of n items (n should be ≤ 9)."""
    if n > 1:
        return f"#1–{n} to pick · Enter to choose · Esc=cancel"
    return "Enter to select · Esc=cancel"


def _prompt(prompt_text: str, *, default: Any = _NO_DEFAULT, choices: list[str] | None = None, prefill: bool = False, free_text: bool = False, two_line: bool = False, slash_max: int = 0, allow_empty: bool = False) -> str:
    """Unified input primitive. choices=list enables single-keypress mode (only listed chars accepted).
    free_text=True uses readline so arrow-keys/editing work. prefill=True pre-populates with default.
    two_line=True (requires prefill=True) prints the label on its own line and the editable value below.
    slash_max=N enables #1–N quick-select in the free-text loop (type # then a digit to pick instantly).
    allow_empty=True lets a prefill prompt return "" when the user clears the field entirely.
    Raises Cancelled on Ctrl+C / Escape. Never use bare input() — always use this.
    In interactive (tty) mode, any input starting with ? performs a manual lookup and re-prompts."""
    while True:
        result = _prompt_once(prompt_text, default=default, choices=choices, prefill=prefill, free_text=free_text, two_line=two_line, slash_max=slash_max, allow_empty=allow_empty)
        if not sys.stdin.isatty() or choices or not result.startswith("?"):
            return result
        _show_help(result[1:].strip() or "help")


def _prompt_once(prompt_text: str, *, default: Any = _NO_DEFAULT, choices: list[str] | None = None, prefill: bool = False, free_text: bool = False, two_line: bool = False, slash_max: int = 0, allow_empty: bool = False) -> str:
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
        _prefill_text = str(default)

        def _hook() -> None:
            readline.insert_text(_prefill_text)
            readline.redisplay()

        readline.set_pre_input_hook(_hook)
        if two_line:
            state.console.print(f"  {prompt_text}:", highlight=False)
            _input_prompt = "  "
        else:
            # Pass the prompt directly to input() so readline knows the exact
            # column position — pre-printing then calling input("") lets backspace
            # erase the label once the prefilled text is cleared.
            import re as _re
            _input_prompt = _re.sub(r'\[/?[^\]]*\]', '', str(prompt_text)) + ": "
        try:
            result = input(_input_prompt)
        except (KeyboardInterrupt, EOFError):
            sys.stdout.write("\n")
            sys.stdout.flush()
            raise Cancelled
        finally:
            readline.set_pre_input_hook(None)
        stripped = result.strip()
        return stripped if (stripped or allow_empty) else default

    hint_parts = []
    if choices:
        hint_parts.append(f"[{state.T['choice']}]({'|'.join(choices)})[/{state.T['choice']}]")
    if default is not _NO_DEFAULT and default not in ("", None):
        hint_parts.append(
            f"([{state.T['default_hint']}]{default}[/{state.T['default_hint']}])"
        )
    hint = (" " + " ".join(hint_parts)) if hint_parts else ""
    if two_line:
        state.console.print(f"  {prompt_text}{hint}:", highlight=False)
        sys.stdout.write("  ")
    else:
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
                    ch = _os.read(fd, 1).decode("ascii", errors="replace")
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
            # Flush any stale input bytes (e.g. Ctrl+C echo, key-repeat) that
            # arrived during single-keypress mode so they don't leak into the
            # next prompt and cause phantom rapid-looping.
            termios.tcflush(fd, termios.TCIFLUSH)
            termios.tcsetattr(fd, termios.TCSADRAIN, old)

    buf: list[str] = []
    hist_idx = len(_input_history)  # one past end = current (unsaved) input
    hist_saved: list[str] = []
    try:
        tty.setcbreak(fd)
        while True:
            try:
                ch = _os.read(fd, 1).decode("ascii", errors="replace")
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
                    if hist_idx > 0:
                        if hist_idx == len(_input_history):
                            hist_saved = buf[:]
                        hist_idx -= 1
                        sys.stdout.write("\b \b" * len(buf))
                        buf = list(_input_history[hist_idx])
                        sys.stdout.write("".join(buf))
                        sys.stdout.flush()
                elif seq == "[B":  # down arrow — go forward in history
                    if hist_idx < len(_input_history):
                        hist_idx += 1
                        sys.stdout.write("\b \b" * len(buf))
                        buf = hist_saved[:] if hist_idx == len(_input_history) else list(_input_history[hist_idx])
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
            if ch == "#" and slash_max > 0:
                sys.stdout.write("#")
                sys.stdout.flush()
                try:
                    ch2 = _os.read(fd, 1).decode("ascii", errors="replace")
                except KeyboardInterrupt:
                    state.console.print()
                    raise Cancelled
                if ch2 in ("\x03", "\x04"):
                    state.console.print()
                    raise Cancelled
                if ch2 == "\x1b":
                    # Restore: erase the "#" and drain any trailing escape bytes
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                    _read_escape_seq()
                    continue
                if ch2.isdigit() and 1 <= int(ch2) <= slash_max:
                    sys.stdout.write(ch2)
                    sys.stdout.flush()
                    state.console.print()
                    return f"#{ch2}"
                # Not a valid quick-pick: keep "#" in buf and handle ch2 normally
                buf.append("#")
                if ch2 in ("\r", "\n"):
                    state.console.print()
                    break
                if ch2 in ("\x7f", "\x08"):
                    buf.pop()
                    sys.stdout.write("\b \b")
                    sys.stdout.flush()
                elif ch2.isprintable():
                    buf.append(ch2)
                    sys.stdout.write(ch2)
                    sys.stdout.flush()
                continue
            if ch.isprintable():
                buf.append(ch)
                sys.stdout.write(ch)
                sys.stdout.flush()
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)

    result = "".join(buf).strip()
    if not choices:
        _append_input_history(result)
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
