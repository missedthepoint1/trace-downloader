import os
import shutil
import subprocess
import sys
from pathlib import Path

from . import paths

def subprocess_flags() -> dict:
    """Kwargs to keep child processes from popping a console window on Windows.

    The frozen app is windowed (console=False); launching a console child
    (node/ffmpeg) without this would allocate a visible console window.
    CREATE_NO_WINDOW exists only on Windows, so it is referenced only there.
    """
    if os.name == "nt":
        return {"creationflags": subprocess.CREATE_NO_WINDOW}
    return {}

def _ffmpeg_name() -> str:
    return "ffmpeg.exe" if os.name == "nt" else "ffmpeg"

def ffmpeg_path() -> str:
    name = _ffmpeg_name()
    for base in (paths.resource_dir() / "bin", paths.data_dir() / "bin"):
        cand = base / name
        if cand.exists():
            return str(cand)
    found = shutil.which("ffmpeg")
    if found:
        return found
    for p in ("/opt/homebrew/bin/ffmpeg", "/usr/local/bin/ffmpeg", "/usr/bin/ffmpeg"):
        if Path(p).exists():
            return p
    return "ffmpeg"

def setup_browser_env() -> None:
    """Point Playwright at a data-dir browsers folder only when frozen.
    In dev we leave it alone so the existing OS cache is reused."""
    if paths.is_frozen():
        os.environ["PLAYWRIGHT_BROWSERS_PATH"] = str(paths.data_dir() / "ms-playwright")

def _browsers_path() -> Path:
    env = os.environ.get("PLAYWRIGHT_BROWSERS_PATH")
    if env:
        return Path(env)
    if os.name == "nt":
        return Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "ms-playwright"
    if sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / "ms-playwright"
    return Path.home() / ".cache" / "ms-playwright"

def chromium_installed() -> bool:
    base = _browsers_path()
    return base.exists() and any(base.glob("chromium-*"))

def install_chromium() -> None:
    from playwright._impl._driver import compute_driver_executable, get_driver_env
    driver = compute_driver_executable()
    args = list(driver) if isinstance(driver, (list, tuple)) else [driver]
    env = {**os.environ, **get_driver_env()}
    subprocess.run([*args, "install", "chromium"], env=env, check=True, **subprocess_flags())
