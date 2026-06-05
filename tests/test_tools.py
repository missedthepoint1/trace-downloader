def test_ffmpeg_prefers_bundled(monkeypatch, tmp_path):
    from trace_grabber import tools, paths
    binp = tmp_path / "bin"; binp.mkdir(); (binp / "ffmpeg").write_text("x")
    monkeypatch.setattr(paths, "resource_dir", lambda: tmp_path)
    monkeypatch.setattr(paths, "data_dir", lambda: tmp_path / "data")
    assert tools.ffmpeg_path() == str(binp / "ffmpeg")

def test_ffmpeg_falls_back_to_which(monkeypatch, tmp_path):
    from trace_grabber import tools, paths
    monkeypatch.setattr(paths, "resource_dir", lambda: tmp_path)
    monkeypatch.setattr(paths, "data_dir", lambda: tmp_path)
    monkeypatch.setattr(tools.shutil, "which", lambda n: "/somewhere/ffmpeg")
    assert tools.ffmpeg_path() == "/somewhere/ffmpeg"
