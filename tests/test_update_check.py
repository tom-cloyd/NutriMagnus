"""
Tests for numa_app/services/update_check.py — the home-page "update
available" check against GitHub's latest-release API.
"""
import json
import urllib.error

import pytest

from numa_app.services import update_check as _uc

# Captured at import time, before conftest.py's autouse no_update_check
# fixture stubs _uc.check_for_update to a no-network no-op for every other
# test file — these tests are what actually exercises the real function.
_real_check_for_update = _uc.check_for_update


@pytest.fixture(autouse=True)
def _reset_cache(monkeypatch: pytest.MonkeyPatch):
    """Undo conftest's no_update_check stub and start with a clean cache,
    so tests in this file exercise the real check_for_update()."""
    monkeypatch.setattr(_uc, "check_for_update", _real_check_for_update)
    _uc._cache = None
    _uc._cache_checked_at = 0.0
    _uc._cache_for_version = None
    yield


def _fake_response(payload: dict):
    class _Resp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return json.dumps(payload).encode()

    return _Resp()


def test_tag_for_matches_create_release_format():
    assert _uc._tag_for("2026-08-31:0744") == "v2026-08-31-0744"


def test_newer_release_detected(monkeypatch):
    monkeypatch.setattr(
        _uc.urllib.request, "urlopen",
        lambda *a, **kw: _fake_response({"tag_name": "v2026-09-01-0000", "html_url": "https://example.com/x"}),
    )
    result = _uc.check_for_update("2026-08-31:0744")
    assert result == {"tag": "v2026-09-01-0000", "url": "https://example.com/x"}


def test_same_or_older_release_is_not_an_update(monkeypatch):
    monkeypatch.setattr(
        _uc.urllib.request, "urlopen",
        lambda *a, **kw: _fake_response({"tag_name": "v2026-08-31-0744", "html_url": "https://example.com/x"}),
    )
    assert _uc.check_for_update("2026-08-31:0744") is None

    monkeypatch.setattr(
        _uc.urllib.request, "urlopen",
        lambda *a, **kw: _fake_response({"tag_name": "v2026-08-01-0000", "html_url": "https://example.com/x"}),
    )
    _uc._cache_for_version = None  # force past the cache
    assert _uc.check_for_update("2026-08-31:0744") is None


def test_network_failure_returns_none_not_raises(monkeypatch):
    def _boom(*a, **kw):
        raise urllib.error.URLError("offline")

    monkeypatch.setattr(_uc.urllib.request, "urlopen", _boom)
    assert _uc.check_for_update("2026-08-31:0744") is None


def test_malformed_response_returns_none_not_raises(monkeypatch):
    class _BadResp:
        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def read(self):
            return b"not json"

    monkeypatch.setattr(_uc.urllib.request, "urlopen", lambda *a, **kw: _BadResp())
    assert _uc.check_for_update("2026-08-31:0744") is None


def test_result_is_cached_until_ttl_expires(monkeypatch):
    calls = []

    def _urlopen(*a, **kw):
        calls.append(1)
        return _fake_response({"tag_name": "v2026-09-01-0000", "html_url": "https://example.com/x"})

    monkeypatch.setattr(_uc.urllib.request, "urlopen", _urlopen)
    _uc.check_for_update("2026-08-31:0744")
    _uc.check_for_update("2026-08-31:0744")
    assert len(calls) == 1  # second call served from cache, no network hit
