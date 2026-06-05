from unittest.mock import patch

def test_run_command_dev(monkeypatch):
    from trace_grabber import platform_tasks as pt, paths
    monkeypatch.setattr(paths, "is_frozen", lambda: False)
    cmd = pt.run_command()
    assert cmd[-1] == "--run" and "gui.entry" in cmd

def test_run_command_frozen(monkeypatch):
    from trace_grabber import platform_tasks as pt, paths
    monkeypatch.setattr(paths, "is_frozen", lambda: True)
    assert pt.run_command()[-1] == "--run"

def test_mac_enable_writes_plist(monkeypatch, tmp_path):
    from trace_grabber import platform_tasks as pt
    monkeypatch.setattr(pt, "LAUNCH_AGENT", tmp_path / "x.plist")
    monkeypatch.setattr(pt.sys, "platform", "darwin")
    with patch.object(pt.subprocess, "run") as run:
        pt.schedule_enable(3)
        assert (tmp_path / "x.plist").exists()
        assert "StartInterval" in (tmp_path / "x.plist").read_text()
        assert pt.schedule_enabled() is True
        run.assert_called()

def test_win_enable_builds_schtasks(monkeypatch):
    from trace_grabber import platform_tasks as pt
    with patch.object(pt.subprocess, "run") as run:
        pt._win_enable(3)
        argv = run.call_args[0][0]
        assert argv[0] == "schtasks" and "/Create" in argv and "TraceDownloader" in argv

def test_notify_never_raises():
    from trace_grabber import platform_tasks as pt
    pt.notify("hi")  # must not raise on any platform
