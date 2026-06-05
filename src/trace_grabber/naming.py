import re
from pathlib import Path

def _slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")

def _unique(output_dir: Path, base: str) -> Path:
    candidate = Path(output_dir) / f"{base}.mp4"
    n = 2
    while candidate.exists():
        candidate = Path(output_dir) / f"{base}-{n}.mp4"
        n += 1
    return candidate

def build_path(output_dir: Path, date: str, half: int, opponent: str | None) -> Path:
    parts = [date]
    if opponent:
        parts.append(f"vs-{_slug(opponent)}")
    parts.append(f"half{half}")
    return _unique(output_dir, "_".join(parts))

def combined_path(output_dir: Path, date: str, opponent: str | None) -> Path:
    parts = [date]
    if opponent:
        parts.append(f"vs-{_slug(opponent)}")
    return _unique(output_dir, "_".join(parts))
