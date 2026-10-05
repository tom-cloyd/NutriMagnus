"""
scripts/create_release.py publishes the starter-set manifest as a release
asset, under the name update_check.py looks for.
"""
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "scripts"))

import create_release  # noqa: E402
from numa_app.services import demo_data, update_check  # noqa: E402


def test_manifest_asset_is_uploaded_under_the_name_update_check_fetches() -> None:
    assert (update_check.STARTER_MANIFEST_ASSET, create_release.STARTER_MANIFEST_PATH, "application/json") \
        in create_release._ASSETS


def test_written_manifest_matches_the_bundled_starter_set(tmp_path, monkeypatch) -> None:
    out = tmp_path / "starter_manifest.json"
    monkeypatch.setattr(create_release, "STARTER_MANIFEST_PATH", out)
    create_release._write_starter_manifest()
    assert json.loads(out.read_text()) == demo_data.starter_manifest()


def test_broken_manual_links_stop_the_release_before_github(monkeypatch) -> None:
    """A failing link check returns 1 before anything is sent to GitHub."""
    monkeypatch.setenv("GITHUB_TOKEN", "x")
    monkeypatch.setattr(create_release, "_manual_links_ok", lambda: False)

    def _no_api(*a, **kw):
        raise AssertionError("GitHub API called despite broken links")

    monkeypatch.setattr(create_release, "_api_request", _no_api)
    monkeypatch.setattr(create_release, "_write_starter_manifest", _no_api)
    assert create_release.main() == 1


def test_release_notes_drop_html_comments_and_fit_github_limit() -> None:
    """Scope blocks are hidden comments that still count toward GitHub's
    125,000-character body limit; the 2026-10-05 release hit it."""
    body = create_release._release_notes()
    assert "<!--" not in body
    assert len(body) <= create_release._BODY_LIMIT


def test_oversized_notes_drop_oldest_dated_sections(monkeypatch) -> None:
    monkeypatch.setattr(create_release, "_BODY_LIMIT", 400)
    body = "#### Summary\n\n- a\n\n#### Oct 5 updates\n\n" + "x" * 50 \
        + "\n\n#### Oct 4 updates\n\n" + "y" * 300
    fitted = create_release._fit_body(body)
    assert len(fitted) <= 400
    assert "Oct 5 updates" in fitted and "Oct 4 updates" not in fitted
    assert fitted.endswith(create_release._TRIMMED_NOTE)
