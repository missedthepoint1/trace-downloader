import html as _html
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from playwright.sync_api import Page

from .state import new_game_ids

@dataclass
class Game:
    id: str           # full game id, e.g. "demoteam1-1001"
    team_id: str      # e.g. "demoteam1"
    date: str         # ISO "YYYY-MM-DD", or "" if unparseable
    opponent: str | None
    title: str        # raw label, e.g. "Demo FC vs. Rovers"

# Each game card is an <a class="GameLink GameCard"> ... </a>. Split on the
# opening tag so each block holds one card's poster URL, title, and date.
_CARD_SPLIT = re.compile(r'(?=<a class="GameLink GameCard")')
_POSTER_RE = re.compile(r'/teams/([a-z0-9]+)/games/([a-z0-9]+-\d+)/')
_TITLE_RE = re.compile(r'<p class="two-lines label[^"]*">([^<]*)</p>')
_DATE_RE = re.compile(r'<p class="subtitle[^"]*">([^<]*)</p>')
_DATE_HEAD = re.compile(r'([A-Z][a-z]+ \d{1,2}, \d{4})')

def _iso_date(text: str) -> str:
    m = _DATE_HEAD.match(text.strip())
    if not m:
        return ""
    # Trace uses full month names ("June 4, 2026"); accept abbreviated too.
    for fmt in ("%B %d, %Y", "%b %d, %Y"):
        try:
            return datetime.strptime(m.group(1), fmt).strftime("%Y-%m-%d")
        except ValueError:
            continue
    return ""

def parse_games(page_html: str) -> list[Game]:
    games: list[Game] = []
    seen: set[str] = set()
    for block in _CARD_SPLIT.split(page_html):
        pm = _POSTER_RE.search(block)
        if not pm:
            continue
        team_id, gid = pm.group(1), pm.group(2)
        if gid in seen:
            continue
        seen.add(gid)
        try:
            tm = _TITLE_RE.search(block)
            title = _html.unescape(tm.group(1).strip()) if tm else ""
            dm = _DATE_RE.search(block)
            date = _iso_date(_html.unescape(dm.group(1))) if dm else ""
            opponent = title.split(" vs. ", 1)[1].strip() if " vs. " in title else None
        except Exception:
            title, date, opponent = "", "", None  # never let one card blank the list
        games.append(Game(id=gid, team_id=team_id, date=date, opponent=opponent, title=title))
    return games

def list_games(page: Page, team_url: str, max_games: int = 60, max_scrolls: int = 15) -> list[Game]:
    page.goto(team_url, wait_until="domcontentloaded")
    page.wait_for_selector("a.GameLink.GameCard", timeout=20000)
    seen = 0
    for _ in range(max_scrolls):
        cards = page.query_selector_all("a.GameLink.GameCard")
        if len(cards) >= max_games or len(cards) == seen:
            break
        seen = len(cards)
        page.mouse.wheel(0, 20000)
        page.wait_for_timeout(1200)
    return parse_games(page.content())[:max_games]

def list_new_games(page: Page, team_url: str, state_path: Path) -> list[Game]:
    games = list_games(page, team_url)
    fresh = set(new_game_ids([g.id for g in games], state_path))
    return [g for g in games if g.id in fresh]
