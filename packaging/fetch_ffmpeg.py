# Download a static ffmpeg into bin/ for the current OS/arch.
import gzip
import os
import platform
import stat
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN = ROOT / "bin"
TAG = "b6.0"
BASE = f"https://github.com/eugeneware/ffmpeg-static/releases/download/{TAG}"

def asset_name() -> str:
    arch = platform.machine().lower()
    if os.name == "nt":
        return "ffmpeg-win32-x64.gz"
    if sys.platform == "darwin":
        return "ffmpeg-darwin-arm64.gz" if arch in ("arm64", "aarch64") else "ffmpeg-darwin-x64.gz"
    return "ffmpeg-linux-x64.gz"

def main():
    BIN.mkdir(exist_ok=True)
    out = BIN / ("ffmpeg.exe" if os.name == "nt" else "ffmpeg")
    url = f"{BASE}/{asset_name()}"
    print("downloading", url)
    with urllib.request.urlopen(url) as r:
        data = gzip.decompress(r.read())
    out.write_bytes(data)
    if os.name != "nt":
        out.chmod(out.stat().st_mode | stat.S_IEXEC | stat.S_IXGRP | stat.S_IXOTH)
    print("wrote", out, f"({len(data)} bytes)")

if __name__ == "__main__":
    main()
