#!/bin/zsh
# Render html -> PDF with headless Chrome. Usage: tools/pdf.sh business-plan.html Alpha-Hours-Business-Plan.pdf
set -e
cd "$(dirname "$0")/.."
CHROME="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
"$CHROME" --headless=new --disable-gpu --no-pdf-header-footer --virtual-time-budget=10000 \
  --print-to-pdf="$PWD/$2" "file://$PWD/$1" >/dev/null 2>&1
ls -la "$2"
