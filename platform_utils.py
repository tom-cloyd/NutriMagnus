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
    """Return the user config directory for numa (profiles, theme, prefs)."""
    if sys.platform == "win32":
        appdata = os.environ.get("APPDATA") or str(pathlib.Path.home() / "AppData" / "Roaming")
        return pathlib.Path(appdata) / "numa"
    return pathlib.Path.home() / ".config" / "numa"


def get_data_dir() -> pathlib.Path:
    """Return the user data directory for numa (database, cache)."""
    if sys.platform == "win32":
        localappdata = os.environ.get("LOCALAPPDATA") or str(pathlib.Path.home() / "AppData" / "Local")
        return pathlib.Path(localappdata) / "numa"
    return pathlib.Path.home() / ".local" / "share" / "numa"
