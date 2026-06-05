import re
from pathlib import Path

def _slug(text: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return s

def build_path(output_dir: Path, date: str, half: int, opponent: str | None) -> Path:
    parts = [date]
    if opponent:
        parts.append(f"vs-{_slug(opponent)}")
    parts.append(f"half{half}")
    base = "_".join(parts)
    candidate = output_dir / f"{base}.mp4"
    n = 2
    while candidate.exists():
        candidate = output_dir / f"{base}-{n}.mp4"
        n += 1
    return candidate
