import sys
from pathlib import Path

import platformdirs

APP_NAME = "TraceDown"
APP_VERSION = "1.2"

def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False))

def data_dir() -> Path:
    d = Path(platformdirs.user_data_dir(APP_NAME))
    d.mkdir(parents=True, exist_ok=True)
    return d

def resource_dir() -> Path:
    if is_frozen():
        return Path(sys._MEIPASS)
    return Path(__file__).resolve().parents[2]
