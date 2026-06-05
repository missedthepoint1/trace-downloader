import json
from trace_grabber.main import write_last_run

def test_write_last_run(tmp_path):
    p = tmp_path / "last_run.json"
    write_last_run(p, count=2, error=None, when="2026-06-05T10:00:00")
    data = json.loads(p.read_text())
    assert data["count"] == 2
    assert data["error"] is None
    assert data["when"] == "2026-06-05T10:00:00"
