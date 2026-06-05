from pathlib import Path
from trace_grabber.games import parse_games, Game

FIXTURE = Path(__file__).parent / "fixtures" / "games_sample.html"

def test_parses_all_cards():
    games = parse_games(FIXTURE.read_text())
    assert len(games) == 3
    assert all(isinstance(g, Game) for g in games)

def test_first_card_fields():
    g = parse_games(FIXTURE.read_text())[0]
    assert g.id == "demoteam1-1001"
    assert g.team_id == "demoteam1"
    assert g.date == "2026-05-28"
    assert g.opponent == "Rovers"

def test_opponent_parsed_for_each():
    opps = [g.opponent for g in parse_games(FIXTURE.read_text())]
    assert opps == ["Rovers", "United", "Athletic"]

def test_no_duplicate_ids():
    games = parse_games(FIXTURE.read_text())
    assert len(games) == len({g.id for g in games})
