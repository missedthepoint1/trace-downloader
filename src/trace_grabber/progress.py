import re

_EXTINF = re.compile(r"#EXTINF:([\d.]+)")
_OUT_TIME = re.compile(r"out_time=(\d+):(\d+):(\d+(?:\.\d+)?)")
_TOTAL_SIZE = re.compile(r"total_size=(\d+)")

def playlist_duration(media_playlist_text: str) -> float:
    return sum(float(m) for m in _EXTINF.findall(media_playlist_text))

def parse_out_time(line: str) -> float | None:
    m = _OUT_TIME.search(line)
    if not m:
        return None
    h, mnt, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
    return h * 3600 + mnt * 60 + s

def parse_total_size(line: str) -> int | None:
    m = _TOTAL_SIZE.search(line)
    return int(m.group(1)) if m else None

def percent(done_seconds: float, total_seconds: float) -> int:
    if total_seconds <= 0:
        return 0
    return max(0, min(100, int(done_seconds / total_seconds * 100)))
