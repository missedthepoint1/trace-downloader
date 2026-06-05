# gui/app.py
import json
import subprocess
import sys
from pathlib import Path

import webview
import yaml

from gui.worker import Worker
from gui.viewmodel import games_view
from trace_grabber import paths, platform_tasks
from trace_grabber.config import load_config

WEB = paths.resource_dir() / "gui" / "web"
DATA = paths.data_dir()
LAST_RUN = DATA / "last_run.json"


class Api:
    def __init__(self):
        self._worker = None
        self._window = None

    def _w(self):
        if self._worker is None:
            self._worker = Worker()
        return self._worker

    def set_window(self, window):
        self._window = window

    def get_status(self):
        last = json.loads(LAST_RUN.read_text()) if LAST_RUN.exists() else None
        cfg = load_config(DATA / "config.yaml")
        return {
            "logged_in": self._w().logged_in(),
            "last_run": last,
            "auto": platform_tasks.schedule_enabled(),
            "settings": {"output_dir": str(cfg.output_dir), "quality": cfg.quality, "combine": cfg.combine_halves},
        }

    def list_games(self):
        games, done = self._w().list_games()
        return games_view(games, done)

    def _run_download(self, game_id):
        games, _ = self._w().list_games()
        g = next((x for x in games if x.id == game_id), None)
        if not g:
            return {"ok": False, "error": "game not found"}

        def on_progress(half, pct, mbps):
            self._emit("progress", {"id": game_id, "half": half, "percent": pct,
                                    "speed": round(mbps, 1)})
        try:
            n = self._w().download_game(g.id, g.team_id, g.date, g.opponent, on_progress)
            if self._w().cancelled():
                self._emit("cancelled", {"id": game_id})
            else:
                self._emit("saved" if n > 0 else "unavailable", {"id": game_id})
            return {"ok": True, "files": n}
        except Exception as e:
            self._emit("error", {"id": game_id, "message": str(e)})
            return {"ok": False, "error": str(e)}

    def download_game(self, game_id):
        self._w().clear_cancel()
        return self._run_download(game_id)

    def cancel(self):
        self._w().cancel()
        return {"ok": True}

    def get_thumb(self, team_id, game_id):
        return self._w().get_thumb(team_id, game_id)

    def list_accounts(self):
        return self._w().list_accounts()

    def switch_account(self, account_id):
        return self._w().switch_account(account_id)

    def remove_account(self, account_id):
        return self._w().remove_account(account_id)

    def add_account_start(self):
        self._w().add_account_start()
        return {"ok": True}

    def add_account_finish(self):
        return self._w().add_account_finish()

    def confirm_team_url(self, url):
        return self._w().confirm_team_url(url)

    def download_new(self):
        self._w().clear_cancel()
        views = self.list_games()
        new_ids = [v["id"] for v in views if v["state"] == "new"]
        done = 0
        for gid in new_ids:
            if self._w().cancelled():
                break
            self._run_download(gid)
            done += 1
        return {"ok": True, "count": done}

    def set_auto(self, enabled):
        if enabled:
            platform_tasks.schedule_enable(load_config(DATA / "config.yaml").check_interval_hours)
        else:
            platform_tasks.schedule_disable()
        return platform_tasks.schedule_enabled()

    def open_folder(self):
        cfg = load_config(DATA / "config.yaml")
        cfg.output_dir.mkdir(parents=True, exist_ok=True)
        opener = "open" if sys.platform == "darwin" else ("explorer" if __import__("os").name == "nt" else "xdg-open")
        subprocess.run([opener, str(cfg.output_dir)], check=False)

    def reconnect_start(self):
        self._w().reconnect_start()
        return {"ok": True}

    def reconnect_finish(self):
        return {"logged_in": self._w().reconnect_finish()}

    def save_settings(self, settings):
        path = DATA / "config.yaml"
        data = yaml.safe_load(path.read_text())
        if "quality" in settings:
            data["quality"] = settings["quality"]
        if "combine" in settings:
            data["combine_halves"] = bool(settings["combine"])
        path.write_text(yaml.safe_dump(data, sort_keys=False))
        self._w().reload_config()
        return {"ok": True}

    def _emit(self, event, payload):
        if self._window:
            self._window.evaluate_js(f"window.onPy({json.dumps(event)}, {json.dumps(payload)})")


def main():
    from trace_grabber import firstrun, tools
    firstrun.init()
    tools.setup_browser_env()
    api = Api()
    need_setup = not tools.chromium_installed()
    first = WEB / ("setup.html" if need_setup else "index.html")
    window = webview.create_window("Trace Downloader", str(first), js_api=api,
                                   width=520, height=720)
    api.set_window(window)
    if need_setup:
        # Only when we showed the setup screen: install Chromium, then load the app.
        def _setup():
            try:
                tools.install_chromium()
            except Exception:
                pass
            window.load_url("file://" + str(WEB / "index.html"))
        import threading
        threading.Thread(target=_setup, daemon=True).start()
    webview.start()


if __name__ == "__main__":
    main()
