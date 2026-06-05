# probe_discover.py — manual discovery probe.
# Opens Chrome with a saved profile. You log in and navigate BY HAND;
# it then captures the real page (URL + screenshot + HTML) so we can write
# correct selectors. Logging in here also persists your session for later
# automated runs (same .chrome-profile).
from pathlib import Path
from playwright.sync_api import sync_playwright

Path("debug").mkdir(exist_ok=True)

# Start at the main site and log in normally (email + phone code).
# If you have a bookmark you use instead, just type it into the address bar.
START = "https://traceup.com"

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(".chrome-profile", headless=False)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()

    try:
        page.goto(START, wait_until="domcontentloaded", timeout=15000)
    except Exception as e:
        print(f"Couldn't open {START}: {e}")
        print(">>> No problem — type your REAL Trace URL into the address bar.")

    input(
        "\n>>> In the Chrome window: log into Trace, then open your GAMES LIST page.\n"
        ">>> When your list of games is on screen, come back here and press Enter...\n"
    )

    # Grab the front-most tab in case new tabs were opened during login.
    page = ctx.pages[-1]
    print("\nCurrent URL:", page.url)
    page.screenshot(path="debug/games_page.png", full_page=True)
    Path("debug/games_page.html").write_text(page.content())
    print("Saved debug/games_page.png and debug/games_page.html")

    input("\n>>> Now open ONE game (so the player loads), then press Enter...\n")
    page = ctx.pages[-1]
    print("Game URL:", page.url)
    page.screenshot(path="debug/game_page.png", full_page=True)
    Path("debug/game_page.html").write_text(page.content())
    print("Saved debug/game_page.png and debug/game_page.html")

    input("\nPress Enter to close the browser...")
    ctx.close()
