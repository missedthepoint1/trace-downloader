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
