import sys

from trace_grabber import tools, firstrun

def _selftest() -> int:
    """Verify the frozen bundle has everything it needs (no GUI, no downloads)."""
    from pathlib import Path
    from trace_grabber import paths
    web = paths.resource_dir() / "gui" / "web" / "index.html"
    ff = tools.ffmpeg_path()
    try:
        from playwright._impl._driver import compute_driver_executable
        driver = bool(compute_driver_executable())
    except Exception as e:
        driver = False
        print("driver error:", e)
    ok = web.exists() and Path(ff).exists() and driver
    print(f"SELFTEST web={web.exists()} ffmpeg={Path(ff).exists()} ({ff}) driver={driver}")
    return 0 if ok else 1

def main():
    firstrun.init()
    tools.setup_browser_env()
    if "--selftest" in sys.argv:
        sys.exit(_selftest())
    if "--run" in sys.argv:
        from trace_grabber.main import run
        sys.exit(run("new"))
    from gui.app import main as gui_main
    gui_main()

if __name__ == "__main__":
    main()
