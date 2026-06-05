import subprocess
import tempfile
from pathlib import Path

from .tools import ffmpeg_path

def build_concat_cmd(parts, dest, list_file):
    return [
        "ffmpeg", "-y", "-f", "concat", "-safe", "0",
        "-i", str(list_file), "-c", "copy", str(dest),
    ]

def combine(parts, dest) -> None:
    """Losslessly concatenate the part files into dest (raises on failure)."""
    parts = [Path(p) for p in parts]
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".txt", delete=False) as f:
        for p in parts:
            f.write(f"file '{p.resolve()}'\n")
        list_file = Path(f.name)
    try:
        cmd = build_concat_cmd(parts, dest, list_file)
        cmd[0] = ffmpeg_path()
        result = subprocess.run(cmd, capture_output=True, text=True)
        if result.returncode != 0:
            raise RuntimeError(f"combine failed ({result.returncode}): {result.stderr[-400:]}")
        if not dest.exists() or dest.stat().st_size == 0:
            raise RuntimeError("combine produced no output")
    finally:
        list_file.unlink(missing_ok=True)
