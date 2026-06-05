from trace_grabber.games import Game

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
