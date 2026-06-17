def test_data_dir_uses_platformdirs(monkeypatch, tmp_path):
    import platformdirs
    monkeypatch.setattr(platformdirs, "user_data_dir", lambda name: str(tmp_path / name))
    from trace_grabber import paths
    d = paths.data_dir()
    assert d == tmp_path / "TraceDown"
    assert d.exists()

def test_resource_dir_is_repo_in_dev():
    from trace_grabber import paths
    assert (paths.resource_dir() / "pyproject.toml").exists()

def test_app_name_and_version():
    from trace_grabber import paths
    assert paths.APP_NAME == "TraceDown"
    assert isinstance(paths.APP_VERSION, str) and paths.APP_VERSION

def test_data_dir_portable_next_to_exe(monkeypatch, tmp_path):
    from trace_grabber import paths
    exe_dir = tmp_path / "app"; exe_dir.mkdir()
    exe = exe_dir / "TraceDown"; exe.write_text("")
    monkeypatch.setattr(paths.sys, "executable", str(exe))
    monkeypatch.setattr(paths.sys, "platform", "win32")
    monkeypatch.setattr(paths, "is_frozen", lambda: True)
    d = paths.data_dir()
    assert d == exe_dir / "data"
    assert d.exists()

def test_data_dir_falls_back_when_not_writable(monkeypatch, tmp_path):
    import platformdirs
    from trace_grabber import paths
    exe_dir = tmp_path / "app"; exe_dir.mkdir()
    exe = exe_dir / "TraceDown"; exe.write_text("")
    # A FILE where the data/ dir would go => mkdir(exist_ok=True) raises => fallback.
    (exe_dir / "data").write_text("")
    monkeypatch.setattr(paths.sys, "executable", str(exe))
    monkeypatch.setattr(paths.sys, "platform", "win32")
    monkeypatch.setattr(paths, "is_frozen", lambda: True)
    fallback = tmp_path / "appdata"
    monkeypatch.setattr(platformdirs, "user_data_dir", lambda name: str(fallback / name))
    d = paths.data_dir()
    assert d == fallback / "TraceDown"
    assert d.exists()

def test_data_dir_darwin_frozen_uses_platformdirs(monkeypatch, tmp_path):
    import platformdirs
    from trace_grabber import paths
    monkeypatch.setattr(paths.sys, "platform", "darwin")
    monkeypatch.setattr(paths, "is_frozen", lambda: True)
    monkeypatch.setattr(platformdirs, "user_data_dir", lambda name: str(tmp_path / name))
    assert paths.data_dir() == tmp_path / "TraceDown"
