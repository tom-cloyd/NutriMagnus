"""
platform_utils.py — Cross-platform config and data directory resolution for numa.

Linux/macOS:
  config: ~/.config/numa/
  data:   ~/.local/share/numa/

Windows:
  config: %APPDATA%/numa/        (Roaming — profiles, theme preference, prefs)
  data:   %LOCALAPPDATA%/numa/   (Local — database, large data files)
"""
import os
import pathlib
import sys


def get_config_dir() -> pathlib.Path:
    """Return the user config directory for numa (profiles, theme, prefs).

    NUMA_CONFIG_DIR overrides this outright — used to point a subprocess
    (e.g. a live server under Playwright E2E tests) at an isolated dir
    instead of the real one, mirroring how in-process tests monkeypatch
    the path constants derived from this function.
    """
    if os.environ.get("NUMA_CONFIG_DIR"):
        return pathlib.Path(os.environ["NUMA_CONFIG_DIR"])
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA") or str(pathlib.Path.home() / "AppData" / "Roaming")
        return pathlib.Path(appdata) / "numa"
    return pathlib.Path.home() / ".config" / "numa"


def get_data_dir() -> pathlib.Path:
    """Return the user data directory for numa (database, cache).

    NUMA_DATA_DIR overrides this outright — see get_config_dir().
    """
    if os.environ.get("NUMA_DATA_DIR"):
        return pathlib.Path(os.environ["NUMA_DATA_DIR"])
    if sys.platform == "win32":
        localappdata = os.environ.get("LOCALAPPDATA") or str(pathlib.Path.home() / "AppData" / "Local")
        return pathlib.Path(localappdata) / "numa"
    return pathlib.Path.home() / ".local" / "share" / "numa"
