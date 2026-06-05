from playwright.sync_api import BrowserContext, Page
from . import selectors as S

CARD_SELECTOR = "a.GameLink.GameCard"

def is_logged_in(page: Page, team_url: str) -> bool:
    page.goto(team_url, wait_until="domcontentloaded")
    if "/login" in page.url or "traceup.com" == page.url.rstrip("/").split("//")[-1]:
        return False
    try:
        page.wait_for_selector(CARD_SELECTOR, timeout=15000)
        return True
    except Exception:
        return False

def cookie_headers(context: BrowserContext) -> dict:
    cookies = context.cookies()
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    return {"Cookie": cookie_str, "Referer": S.BASE_URL}
