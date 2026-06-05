def test_migrate_app_rename_moves(monkeypatch, tmp_path):
    import platformdirs
    from trace_grabber import firstrun, paths
    old = tmp_path / "old"; old.mkdir()
    (old / "accounts.json").write_text('{"active": null, "accounts": []}')
    (old / ".chrome-profile").mkdir()
    new = tmp_path / "new"; new.mkdir()
    monkeypatch.setattr(paths, "data_dir", lambda: new)
    monkeypatch.setattr(platformdirs, "user_data_dir",
                        lambda name: str(old) if name == "Trace Downloader" else str(new))
    firstrun.migrate_app_rename()
    assert (new / "accounts.json").exists()
    assert (new / ".chrome-profile").exists()

def test_migrate_app_rename_noop_when_new_has_data(monkeypatch, tmp_path):
    import platformdirs
    from trace_grabber import firstrun, paths
    old = tmp_path / "old"; old.mkdir(); (old / "accounts.json").write_text("x")
    new = tmp_path / "new"; new.mkdir(); (new / "accounts.json").write_text("keep")
    monkeypatch.setattr(paths, "data_dir", lambda: new)
    monkeypatch.setattr(platformdirs, "user_data_dir", lambda name: str(old))
    firstrun.migrate_app_rename()
    assert (new / "accounts.json").read_text() == "keep"

def test_ensure_config_seeds_when_absent(monkeypatch, tmp_path):
    from trace_grabber import firstrun, paths
    monkeypatch.setattr(paths, "data_dir", lambda: tmp_path / "data")
    (tmp_path / "data").mkdir()
    monkeypatch.setattr(paths, "resource_dir", lambda: tmp_path)  # no template here
    firstrun.ensure_config()
    cfg = tmp_path / "data" / "config.yaml"
    assert cfg.exists()
    import yaml
    data = yaml.safe_load(cfg.read_text())
    assert data["team_urls"] == [] and data["quality"] == "highest"

def test_ensure_config_keeps_existing(monkeypatch, tmp_path):
    from trace_grabber import firstrun, paths
    d = tmp_path / "data"; d.mkdir()
    (d / "config.yaml").write_text("output_dir: ~/X\ncheck_interval_hours: 3\nquality: 1000k\nteam_urls: []\n")
    monkeypatch.setattr(paths, "data_dir", lambda: d)
    monkeypatch.setattr(paths, "resource_dir", lambda: tmp_path)
    firstrun.ensure_config()
    import yaml
    assert yaml.safe_load((d / "config.yaml").read_text())["quality"] == "1000k"
