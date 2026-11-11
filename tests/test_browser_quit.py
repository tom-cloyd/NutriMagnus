"""numa_app/services/browser_quit.py: NuMa stops when Firefox quits."""
from numa_app.services import browser_quit as bq

FF = "Mozilla/5.0 (X11; Linux x86_64; rv:140.0) Gecko/20100101 Firefox/140.0"
CHROME = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 Chrome/140.0 Safari/537.36"


def _watch(states):
    it = iter(states)
    return bq.FirefoxWatch(on_quit=lambda: None, running=lambda: next(it))


def test_stops_after_firefox_quits_with_a_numa_page_last_in_it():
    w = _watch([True, False, False])
    w.page_seen(FF)
    assert [w.check(), w.check(), w.check()] == [False, False, True]


def test_one_missed_check_is_not_enough():
    w = _watch([True, False, True, False, True])
    w.page_seen(FF)
    assert not any(w.check() for _ in range(5))


def test_ignored_when_the_last_page_was_in_another_browser():
    w = _watch([True, False, False])
    w.page_seen(FF)
    w.check()
    w.page_seen(CHROME)
    assert not w.check() and not w.check()


def test_firefox_never_seen_running_does_not_stop_numa():
    w = _watch([False, False, False])
    w.page_seen(FF)
    assert not any(w.check() for _ in range(3))


def test_unknown_state_does_nothing():
    w = _watch([True, None, None, None])
    w.page_seen(FF)
    assert not any(w.check() for _ in range(4))


def test_is_firefox_ua():
    assert bq.is_firefox_ua(FF) and not bq.is_firefox_ua(CHROME)


def test_close_app_window_without_kde_does_nothing(monkeypatch):
    monkeypatch.setattr(bq.shutil, "which", lambda name: None)
    bq.close_app_window("/nutrimagnus")      # no error, nothing run


def test_close_app_window_matches_numas_window_only(monkeypatch):
    scripts, calls = [], []
    monkeypatch.setattr(bq.shutil, "which", lambda name: "/usr/bin/qdbus6" if name == "qdbus6" else None)
    monkeypatch.setattr(bq.time, "sleep", lambda s: None)

    def fake_run(cmd, **kw):
        calls.append(cmd)
        if cmd[-2:-1] and cmd[3] == "org.kde.kwin.Scripting.loadScript":
            scripts.append(open(cmd[4]).read())
        return type("R", (), {"stdout": "7", "returncode": 0})()
    monkeypatch.setattr(bq.subprocess, "run", fake_run)
    bq.close_app_window("/nutrimagnus-source")
    assert "'__nutrimagnus-source-Default'" in scripts[0]
    assert calls[1][2] == "/Scripting/Script7"
