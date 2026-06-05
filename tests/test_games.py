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

def test_full_month_name_dates():
    # Trace shows full month names; "June" must not crash (only "May" is 3 letters).
    from trace_grabber.games import _iso_date
    assert _iso_date("June 4, 2026 @ 7:30 pm") == "2026-06-04"
    assert _iso_date("August 12, 2026") == "2026-08-12"
    assert _iso_date("May 28, 2026") == "2026-05-28"

def test_no_duplicate_ids():
    games = parse_games(FIXTURE.read_text())
    assert len(games) == len({g.id for g in games})
