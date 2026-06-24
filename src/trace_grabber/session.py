from playwright.sync_api import APIRequestContext, BrowserContext, Page
from . import selectors as S

CARD_SELECTOR = "a.GameLink.GameCard"

# Authoritative auth endpoint: returns the user when the session cookie is live,
# {"success": false, "error": {"id": "user_not_logged_in"}} when it has lapsed.
USERS_SELF_URL = "https://teams.traceup.com/webapp/users/self"

def api_logged_in(request: APIRequestContext) -> tuple[bool, str]:
    """Instant, reliable auth check via Trace's webapp API (shares the browser
    context's session cookies). Preferred over waiting for the games SPA to
    render — that wait races the page and reports false 'session expired'.
    Returns (logged_in, human-readable detail)."""
    try:
        r = request.get(USERS_SELF_URL, timeout=12000)
    except Exception as e:
        return False, f"api unreachable: {e!r}"
    try:
        j = r.json()
    except Exception:
        return False, f"api http {r.status} (non-JSON)"
    data = j.get("data") or {}
    if j.get("success") and data.get("user_id"):
        return True, f"logged in (user_id={data['user_id']})"
    return False, (j.get("error") or {}).get("id") or "not logged in"

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
