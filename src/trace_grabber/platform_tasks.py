import os
import subprocess
import sys
from pathlib import Path

from . import paths

PLIST_LABEL = "com.tracedownloader"
LAUNCH_AGENT = Path.home() / "Library" / "LaunchAgents" / f"{PLIST_LABEL}.plist"
WIN_TASK = "TraceDownloader"

def run_command() -> list[str]:
    if paths.is_frozen():
        return [sys.executable, "--run"]
    return [sys.executable, "-m", "gui.entry", "--run"]

def _mac_plist(interval_hours: int) -> str:
    args = "".join(f"      <string>{a}</string>\n" for a in run_command())
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" '
        '"http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0"><dict>\n'
        f'  <key>Label</key><string>{PLIST_LABEL}</string>\n'
        f'  <key>ProgramArguments</key><array>\n{args}  </array>\n'
        f'  <key>StartInterval</key><integer>{interval_hours * 3600}</integer>\n'
        '</dict></plist>\n'
    )

def _mac_enable(interval_hours):
    LAUNCH_AGENT.parent.mkdir(parents=True, exist_ok=True)
    LAUNCH_AGENT.write_text(_mac_plist(interval_hours))
    subprocess.run(["launchctl", "load", str(LAUNCH_AGENT)], check=False)

def _mac_disable():
    subprocess.run(["launchctl", "unload", str(LAUNCH_AGENT)], check=False)
    if LAUNCH_AGENT.exists():
        LAUNCH_AGENT.unlink()

def _win_cmd_string():
    return " ".join(f'"{a}"' if " " in a else a for a in run_command())

def _win_enable(interval_hours):
    subprocess.run(["schtasks", "/Create", "/F", "/SC", "HOURLY", "/MO",
                    str(interval_hours), "/TN", WIN_TASK, "/TR", _win_cmd_string()],
                   check=False)

def _win_disable():
    subprocess.run(["schtasks", "/Delete", "/F", "/TN", WIN_TASK], check=False)

def schedule_enable(interval_hours: int = 3) -> None:
    if sys.platform == "darwin":
        _mac_enable(interval_hours)
    elif os.name == "nt":
        _win_enable(interval_hours)

def schedule_disable() -> None:
    if sys.platform == "darwin":
        _mac_disable()
    elif os.name == "nt":
        _win_disable()

def schedule_enabled() -> bool:
    if sys.platform == "darwin":
        return LAUNCH_AGENT.exists()
    if os.name == "nt":
        r = subprocess.run(["schtasks", "/Query", "/TN", WIN_TASK],
                           capture_output=True, text=True)
        return r.returncode == 0
    return False

def notify(message: str) -> None:
    try:
        if sys.platform == "darwin":
            subprocess.run(["osascript", "-e",
                f'display notification "{message}" with title "TraceDown"'],
                check=False)
        elif os.name == "nt":
            safe = message.replace("'", "")
            subprocess.run(["powershell", "-NoProfile", "-Command",
                f"New-BurntToastNotification -Text 'TraceDown','{safe}'"],
                check=False)
    except Exception:
        pass
