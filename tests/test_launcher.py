"""Tests for web/launcher.py's startup loading page."""
import importlib.util
import pathlib
import socket
import urllib.request

_spec = importlib.util.spec_from_file_location(
    "numa_launcher", pathlib.Path(__file__).parent.parent / "web" / "launcher.py")
launcher = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(launcher)


def _get(port: int) -> str:
    with urllib.request.urlopen(f"http://127.0.0.1:{port}/meals", timeout=5) as resp:
        return resp.read().decode()


def test_loading_page_served_then_socket_handed_on() -> None:
    """The loading page answers at once on the real port; after stop() the
    same listening socket still accepts connections (for uvicorn)."""
    sock = launcher._bind_socket("127.0.0.1", 0)
    port = sock.getsockname()[1]
    loading = launcher._LoadingServer(sock)
    loading.start()
    try:
        page = _get(port)
        assert "Loading NutriMagnus" in page
        assert 'http-equiv="refresh"' in page
        loading.page = launcher._FAILED_PAGE
        assert "did not start" in _get(port)
    finally:
        loading.stop()
    client = socket.create_connection(("127.0.0.1", port), timeout=2)
    conn, _ = sock.accept()
    conn.close()
    client.close()
    sock.close()
