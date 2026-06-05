# login.py — log into Trace by hand (email + phone code). Run when first
# setting up, or when trace-grabber says the session expired.
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    ctx = p.chromium.launch_persistent_context(".chrome-profile", headless=False)
    page = ctx.pages[0] if ctx.pages else ctx.new_page()
    page.goto("https://traceup.com", wait_until="domcontentloaded")
    input("\n>>> Log into Trace in the Chrome window (email + phone code).\n"
          ">>> When you can see your games, press Enter here to save the session...\n")
    print("Session saved to .chrome-profile. You can close this.")
    ctx.close()
