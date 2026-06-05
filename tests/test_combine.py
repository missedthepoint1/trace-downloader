from pathlib import Path
from trace_grabber.combine import build_concat_cmd

def test_build_concat_cmd():
    cmd = build_concat_cmd([Path("/v/a.mp4"), Path("/v/b.mp4")],
                           Path("/v/out.mp4"), Path("/tmp/list.txt"))
    assert cmd[0] == "ffmpeg"
    assert "concat" in cmd and "-safe" in cmd and "0" in cmd
    assert "/tmp/list.txt" in cmd
    assert "copy" in cmd
    assert "/v/out.mp4" in cmd
