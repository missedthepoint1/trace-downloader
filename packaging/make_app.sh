#!/usr/bin/env bash
# Build "Trace Downloader.app" — a native .app bundle (with icon) that launches
# the GUI from this repo's venv. It uses the repo's existing data (login,
# accounts, config), so no re-login. Tied to this Mac's paths by design.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
APP="$REPO/dist/TraceDown.app"

rm -rf "$APP"
mkdir -p "$APP/Contents/MacOS" "$APP/Contents/Resources"

cat > "$APP/Contents/Info.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
  <key>CFBundleName</key><string>TraceDown</string>
  <key>CFBundleDisplayName</key><string>TraceDown</string>
  <key>CFBundleIdentifier</key><string>com.tracegrabber.app</string>
  <key>CFBundleVersion</key><string>1.0</string>
  <key>CFBundleShortVersionString</key><string>1.0</string>
  <key>CFBundlePackageType</key><string>APPL</string>
  <key>CFBundleExecutable</key><string>launcher</string>
  <key>CFBundleIconFile</key><string>icon.icns</string>
  <key>LSMinimumSystemVersion</key><string>11.0</string>
  <key>NSHighResolutionCapable</key><true/>
</dict>
</plist>
PLIST

cat > "$APP/Contents/MacOS/launcher" <<LAUNCH
#!/bin/bash
# Make Homebrew tools (ffmpeg) reachable when launched from Finder.
export PATH="/opt/homebrew/bin:/usr/local/bin:\$PATH"
cd "$REPO"
exec "$REPO/.venv/bin/python3" -m gui.entry
LAUNCH
chmod +x "$APP/Contents/MacOS/launcher"

cp "$REPO/assets/icon.icns" "$APP/Contents/Resources/icon.icns"

# Refresh Finder's icon cache for the new bundle.
touch "$APP"
echo "Built: $APP"
