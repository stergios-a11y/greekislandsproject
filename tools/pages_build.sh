#!/usr/bin/env bash
# Cloudflare Pages build step: copy the site into dist/ WITHOUT the build
# tooling and source data. Until Sep 2026 the whole repo root was deployed, so
# /tools/prerender.py, /tools/IDEAS.md, /costs.csv and friends were public.
#
# Cloudflare Pages settings (Settings -> Builds & deployments):
#   Build command:           bash tools/pages_build.sh
#   Build output directory:  dist
# Nothing else changes: _headers, _redirects and every page are copied as-is.
#
# Runtime data that MUST stay deployed (fetched by script.js): islands/*.json,
# vs_verdicts.json, vs_faqs.json, whats-on.json, hero-photos.json,
# festivals-index.json. Build-only inputs live in tools/, markets/ and templates/.
set -euo pipefail
cd "$(dirname "$0")/.."
# Refuse to package a broken build (static checks of every sitemap page).
if command -v python3 >/dev/null 2>&1; then python3 tools/smoke.py; fi
rm -rf dist && mkdir dist
tar -cf - \
  --exclude=./dist \
  --exclude=./.git \
  --exclude=./.gitignore \
  --exclude=./tools \
  --exclude=./markets --exclude=./templates \
  --exclude=./vs_verdicts.json --exclude=./vs_faqs.json \
  --exclude=./costs.json \
  --exclude='./*.md' \
  --exclude='*/__pycache__' \
  . | tar -xf - -C dist
echo "dist/: $(find dist -type f | wc -l) files, $(du -sh dist | cut -f1)"
