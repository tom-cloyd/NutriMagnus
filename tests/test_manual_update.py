"""Tests for numa_app/services/manual_update.py — signed, independent manual updates."""
import base64
import hashlib
import json

import pytest
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

from numa_app.services import manual_update as mu


def _html(stamp):
    return f"<html><body><p><em>Updated {stamp}</em> / Reading time</p></body></html>".encode()


@pytest.fixture
def signer(monkeypatch, tmp_path):
    key = Ed25519PrivateKey.generate()
    pub = base64.b64encode(key.public_key().public_bytes(serialization.Encoding.Raw, serialization.PublicFormat.Raw)).decode()
    monkeypatch.setattr(mu, "_PUBLIC_KEY_B64", pub)
    monkeypatch.setenv("NUMA_DATA_DIR", str(tmp_path / "data"))
    mu._installed_cache = None
    mu.clear_cache()

    def make(stamp="2026-09-22:1000", requires="2026-09-21:0526", html=None, **over):
        html = html if html is not None else _html(stamp)
        m = {"format": 1, "manual_stamp": stamp, "sha256": hashlib.sha256(html).hexdigest(),
             "size": len(html), "requires_program": requires}
        m.update(over)
        mb = json.dumps(m).encode()
        return mb, base64.b64encode(key.sign(mb)), html
    make.key = key
    return make


def test_valid_bundle_verifies(signer):
    mb, sig, html = signer()
    assert mu.verify_bundle(mb, sig, html)["manual_stamp"] == "2026-09-22:1000"


def test_tampered_html_rejected(signer):
    mb, sig, html = signer()
    assert mu.verify_bundle(mb, sig, html + b"<script>x</script>") is None


def test_tampered_manifest_rejected(signer):
    mb, sig, html = signer()
    assert mu.verify_bundle(mb.replace(b"1000", b"2000"), sig, html) is None


def test_wrong_key_rejected(signer):
    mb, _, html = signer()
    other = Ed25519PrivateKey.generate()
    assert mu.verify_bundle(mb, base64.b64encode(other.sign(mb)), html) is None


def test_garbage_signature_rejected(signer):
    mb, _, html = signer()
    assert mu.verify_bundle(mb, b"not base64!!", html) is None


def test_html_stamp_must_match_manifest(signer):
    mb, sig, html = signer(html=_html("2026-01-01:0000"))
    assert mu.verify_bundle(mb, sig, html) is None


def test_bad_stamp_format_rejected(signer):
    mb, sig, html = signer(stamp="tomorrow", html=b"<em>Updated 2026-09-22:1000</em>")
    assert mu.verify_bundle(mb, sig, html) is None


def _install_files(signer, stamp):
    mb, sig, html = signer(stamp=stamp)
    d = mu.installed_dir()
    d.mkdir(parents=True)
    (d / mu.HTML_ASSET).write_bytes(html)
    (d / mu.MANIFEST_ASSET).write_bytes(mb)
    (d / mu.SIGNATURE_ASSET).write_bytes(sig)
    return d


def test_active_prefers_newer_downloaded(signer, tmp_path):
    baked = tmp_path / "baked.html"
    baked.write_bytes(_html("2026-09-21:0629"))
    _install_files(signer, "2026-09-22:1000")
    a = mu.get_active_manual(baked)
    assert a["source"] == "downloaded" and a["stamp"] == "2026-09-22:1000"


def test_active_ignores_older_or_equal_downloaded(signer, tmp_path):
    baked = tmp_path / "baked.html"
    baked.write_bytes(_html("2026-09-25:0000"))
    _install_files(signer, "2026-09-22:1000")
    assert mu.get_active_manual(baked)["source"] == "baked"


def test_active_ignores_tampered_downloaded(signer, tmp_path):
    baked = tmp_path / "baked.html"
    baked.write_bytes(_html("2026-09-21:0629"))
    d = _install_files(signer, "2026-09-22:1000")
    (d / mu.HTML_ASSET).write_bytes(_html("2026-09-22:1000") + b"evil")
    assert mu.get_active_manual(baked)["source"] == "baked"


def _fake_fetch(monkeypatch, files):
    monkeypatch.setattr(mu, "_fetch", lambda name, mx, to: files.get(name))


def test_check_reports_newer_and_too_old(signer, monkeypatch):
    mb, sig, html = signer(requires="2026-09-30:0000")
    _fake_fetch(monkeypatch, {mu.MANIFEST_ASSET: mb, mu.SIGNATURE_ASSET: sig})
    r = mu.check_for_manual_update("2026-09-21:0629", "2026-09-21:0526")
    assert r["stamp"] == "2026-09-22:1000" and r["program_too_old"] is True


def test_check_none_when_current_or_unsigned(signer, monkeypatch):
    mb, sig, html = signer()
    _fake_fetch(monkeypatch, {mu.MANIFEST_ASSET: mb, mu.SIGNATURE_ASSET: sig})
    assert mu.check_for_manual_update("2026-09-22:1000", "x") is None
    mu.clear_cache()
    _fake_fetch(monkeypatch, {mu.MANIFEST_ASSET: mb, mu.SIGNATURE_ASSET: b"AAAA"})
    assert mu.check_for_manual_update("2026-01-01:0000", "x") is None
    mu.clear_cache()
    _fake_fetch(monkeypatch, {})
    assert mu.check_for_manual_update("2026-01-01:0000", "x") is None


def test_install_success_and_refusals(signer, monkeypatch):
    mb, sig, html = signer()
    _fake_fetch(monkeypatch, {mu.MANIFEST_ASSET: mb, mu.SIGNATURE_ASSET: sig, mu.HTML_ASSET: html})
    assert mu.install_update("2026-09-21:0629") == {"ok": True, "stamp": "2026-09-22:1000"}
    assert (mu.installed_dir() / mu.HTML_ASSET).read_bytes() == html
    # already current
    assert mu.install_update("2026-09-22:1000")["ok"] is False
    # tampered html: nothing written
    import shutil
    shutil.rmtree(mu.installed_dir())
    _fake_fetch(monkeypatch, {mu.MANIFEST_ASSET: mb, mu.SIGNATURE_ASSET: sig, mu.HTML_ASSET: html + b"x"})
    r = mu.install_update("2026-09-21:0629")
    assert r["ok"] is False and "NOT installed" in r["error"]
    assert not mu.installed_dir().exists()


def test_public_key_matches_publisher_key_format():
    assert len(base64.b64decode(mu._PUBLIC_KEY_B64)) == 32
