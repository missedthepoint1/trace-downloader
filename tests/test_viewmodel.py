from trace_grabber.games import Game
from gui.viewmodel import game_view, games_view, connection_state

def _g(i): return Game(id=i, team_id="t", date="2026-05-28", opponent="Rivals", title="T vs. Rivals")

def test_game_view_saved_vs_new():
    assert game_view(_g("t-1"), {"t-1"})["state"] == "saved"
    assert game_view(_g("t-2"), {"t-1"})["state"] == "new"

def test_game_view_fields():
    v = game_view(_g("t-9"), set())
    assert v["id"] == "t-9" and v["date"] == "2026-05-28" and v["opponent"] == "Rivals"
    assert v["team_id"] == "t"

def test_games_view_maps_all():
    views = games_view([_g("t-1"), _g("t-2")], {"t-1"})
    assert [v["state"] for v in views] == ["saved", "new"]

def test_connection_state_no_account_is_none_not_expired():
    # A fresh install (no account yet) must NOT read as a stale session —
    # otherwise the UI shows "Session expired" + Reconnect, a dead end.
    assert connection_state(has_account=False, logged_in=False) == "none"
    assert connection_state(has_account=False, logged_in=True) == "none"

def test_connection_state_with_account():
    assert connection_state(has_account=True, logged_in=False) == "expired"
    assert connection_state(has_account=True, logged_in=True) == "ok"
