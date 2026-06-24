from playwright.sync_api import BrowserContext, Page
from . import selectors as S

CARD_SELECTOR = "a.GameLink.GameCard"

def login_status(page: Page, team_url: str) -> tuple[bool, str]:
    """(logged_in, human-readable detail). Detail is for on-screen diagnostics
    so a Windows user can tell us WHY a check failed without digging in logs."""
    try:
        page.goto(team_url, wait_until="domcontentloaded")
    except Exception as e:
        return False, f"navigation failed: {e!r}"
    url = page.url
    if "/login" in url or "traceup.com" == url.rstrip("/").split("//")[-1]:
        return False, f"redirected to login (url={url})"
    try:
        page.wait_for_selector(CARD_SELECTOR, timeout=15000)
        n = len(page.query_selector_all(CARD_SELECTOR))
        return True, f"ok (cards={n})"
    except Exception:
        n = len(page.query_selector_all(CARD_SELECTOR))
        try:
            title = page.title()
        except Exception:
            title = "?"
        return False, f"no game cards (found={n}, url={url}, title={title!r})"

def is_logged_in(page: Page, team_url: str) -> bool:
    return login_status(page, team_url)[0]

def cookie_headers(context: BrowserContext) -> dict:
    cookies = context.cookies()
    cookie_str = "; ".join(f"{c['name']}={c['value']}" for c in cookies)
    return {"Cookie": cookie_str, "Referer": S.BASE_URL}
