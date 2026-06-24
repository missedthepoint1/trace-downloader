from trace_grabber.games import Game

def connection_state(has_account: bool, logged_in: bool) -> str:
    """Header connection state for the UI.

    Three states, not two: a fresh install with no account is "none" (prompt to
    connect), distinct from an added account whose session lapsed ("expired",
    which is what Reconnect is for). Collapsing them made new users see
    "Session expired" + a Reconnect button that can never succeed.
    """
    if not has_account:
        return "none"
    return "ok" if logged_in else "expired"

def game_view(game: Game, downloaded_ids: set[str]) -> dict:
    return {
        "id": game.id,
        "team_id": game.team_id,
        "date": game.date,
        "opponent": game.opponent or "",
        "title": game.title,
        "state": "saved" if game.id in downloaded_ids else "new",
        "thumb": None,
    }

def games_view(games: list[Game], downloaded_ids: set[str]) -> list[dict]:
    return [game_view(g, downloaded_ids) for g in games]
