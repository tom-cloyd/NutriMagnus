"""
Tests for numa_app/services/self_update.py — the home-page "Update Now"
self-replace of the packaged binary.
"""
import stat
import sys
import urllib.error

import pytest

from numa_app.services import self_update as _su


def _frozen_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "platform", "linux")


def test_is_available_false_when_not_frozen(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "frozen", False, raising=False)
    monkeypatch.setattr(sys, "platform", "linux")
    assert _su.is_available() is False


def test_is_available_false_off_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "frozen", True, raising=False)
    monkeypatch.setattr(sys, "platform", "win32")
    assert _su.is_available() is False


def test_is_available_true_when_frozen_linux(monkeypatch: pytest.MonkeyPatch) -> None:
    _frozen_linux(monkeypatch)
    assert _su.is_available() is True


def test_perform_update_refuses_when_unavailable(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(sys, "frozen", False, raising=False)
    result = _su.perform_update()
    assert result == {"ok": False, "error": "Self-update is only available for the packaged Linux install."}


def test_perform_update_replaces_binary_and_icon(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _frozen_linux(monkeypatch)
    fake_exe = tmp_path / "nutrimagnus"
    fake_exe.write_bytes(b"old binary content")
    fake_exe.chmod(0o755)
    monkeypatch.setattr(sys, "executable", str(fake_exe))

    icon_path = tmp_path / "icons" / "nutrimagnus.png"
    monkeypatch.setattr(_su, "_ICON_PATH", icon_path)

    new_binary = b"X" * _su._MIN_BINARY_BYTES
    calls = []

    def _fake_download(url, *, min_bytes=0):
        calls.append(url)
        if url.endswith("/nutrimagnus"):
            return new_binary
        return b"fake png bytes"

    monkeypatch.setattr(_su, "_download", _fake_download)

    result = _su.perform_update()
    assert result == {"ok": True}
    assert fake_exe.read_bytes() == new_binary
    assert stat.S_IMODE(fake_exe.stat().st_mode) & stat.S_IEXEC
    assert icon_path.read_bytes() == b"fake png bytes"
    assert calls == [
        f"{_su._LATEST_DOWNLOAD_BASE}/nutrimagnus",
        f"{_su._LATEST_DOWNLOAD_BASE}/nutrimagnus.png",
    ]


def test_perform_update_leaves_original_untouched_on_download_failure(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    _frozen_linux(monkeypatch)
    fake_exe = tmp_path / "nutrimagnus"
    fake_exe.write_bytes(b"old binary content")
    monkeypatch.setattr(sys, "executable", str(fake_exe))

    def _boom(url, *, min_bytes=0):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(_su, "_download", _boom)

    result = _su.perform_update()
    assert result["ok"] is False
    assert "Download failed" in result["error"]
    assert fake_exe.read_bytes() == b"old binary content"


def test_perform_update_icon_failure_does_not_fail_the_whole_update(
    monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """The binary swap is what matters; a broken icon fetch shouldn't be
    reported as an update failure once the binary is already replaced."""
    _frozen_linux(monkeypatch)
    fake_exe = tmp_path / "nutrimagnus"
    fake_exe.write_bytes(b"old binary content")
    monkeypatch.setattr(sys, "executable", str(fake_exe))
    monkeypatch.setattr(_su, "_ICON_PATH", tmp_path / "icons" / "nutrimagnus.png")

    new_binary = b"X" * _su._MIN_BINARY_BYTES

    def _fake_download(url, *, min_bytes=0):
        if url.endswith("/nutrimagnus"):
            return new_binary
        raise urllib.error.URLError("icon host unreachable")

    monkeypatch.setattr(_su, "_download", _fake_download)

    result = _su.perform_update()
    assert result == {"ok": True}
    assert fake_exe.read_bytes() == new_binary
