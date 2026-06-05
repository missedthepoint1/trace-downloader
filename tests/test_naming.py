from pathlib import Path
from trace_grabber.naming import build_path

def test_basic_name(tmp_path):
    p = build_path(tmp_path, date="2026-06-04", half=1, opponent=None)
    assert p == tmp_path / "2026-06-04_half1.mp4"

def test_opponent_slugified(tmp_path):
    p = build_path(tmp_path, date="2026-06-04", half=2, opponent="FC Rivals!")
    assert p == tmp_path / "2026-06-04_vs-fc-rivals_half2.mp4"

def test_collision_suffix(tmp_path):
    (tmp_path / "2026-06-04_half1.mp4").write_text("x")
    p = build_path(tmp_path, date="2026-06-04", half=1, opponent=None)
    assert p == tmp_path / "2026-06-04_half1-2.mp4"
