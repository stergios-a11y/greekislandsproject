#!/usr/bin/env python3
"""
auto-images-crete.py
====================

Fully-automated image populator for the 5 Crete island JSONs.
Uses the Wikimedia Commons API to fetch top-result images for every
slot (beach, day-stop, specialty, festival) that doesn't already have
a photo. Outputs a JSON patch file you can apply via apply-image-patch.py.

WHY LOCAL? The Anthropic sandbox cannot reach commons.wikimedia.org.
Run this on your Mac where there's no proxy block.

USAGE
  cd ~/Desktop/greekislandsproject
  python3 auto-images-crete.py
    --islands islands/                          # where the island JSONs live
    --out crete-image-patch.json                # patch file to send back to Claude
    [--also-include rethymno,heraklion,...]     # default: all 5 Crete

  Then send crete-image-patch.json to Claude in a follow-up turn.

QUALITY FILTERS
  - Minimum width: 800px (rejects thumbnails)
  - Excludes: SVG, GIF, maps (filename contains "map"), diagrams, charts
  - Excludes images where width <= height by ≥30% (rejects portraits/posters)
    UNLESS the slot is a person (festivals about a person)
  - Prefers files with "Crete" in title (place-disambiguation)

CITATIONS
  Each image record includes:
    url, attribution, license, page_url
  These get stored in the JSON so the rendered pages can show CC credits.
"""

import json
import sys
import re
import time
import argparse
from pathlib import Path
from urllib.parse import quote
import urllib.request
import urllib.error

WIKIMEDIA_API = "https://commons.wikimedia.org/w/api.php"

# Politeness for the Wikimedia API — they want us to identify ourselves
USER_AGENT = "AegeanBlueprint/1.0 (https://aegeanblueprint.com; contact via website)"

# Quality thresholds
MIN_WIDTH = 800
ASPECT_LANDSCAPE_MIN = 1.0   # width/height must be at least this (1.0 = square OK)
DEFAULT_DELAY = 0.6           # seconds between API calls (be polite)


# ----------------------------------------------------------------
# Wikimedia API helpers
# ----------------------------------------------------------------
def api_call(params: dict) -> dict:
    """Make a Wikimedia API call. Always JSON. Returns parsed dict."""
    params = {**params, "format": "json", "formatversion": "2"}
    qs = "&".join(f"{k}={quote(str(v))}" for k, v in params.items())
    url = f"{WIKIMEDIA_API}?{qs}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=20) as r:
            return json.loads(r.read())
    except urllib.error.HTTPError as e:
        print(f"  ! HTTP {e.code}: {url[:120]}")
        return {}
    except Exception as e:
        print(f"  ! {type(e).__name__}: {e}")
        return {}


def search_images(query: str, limit: int = 10) -> list:
    """Search Commons for files matching query. Returns list of file titles."""
    data = api_call({
        "action": "query",
        "list": "search",
        "srsearch": f"{query} filetype:bitmap",
        "srnamespace": 6,  # File namespace
        "srlimit": limit,
    })
    return [r["title"] for r in data.get("query", {}).get("search", [])]


def get_image_info(file_title: str):
    """Fetch URL, dimensions, mime type, and license metadata for a file.
    Returns dict or None."""
    data = api_call({
        "action": "query",
        "titles": file_title,
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": 1600,  # request a 1600px-wide thumb URL we can use
    })
    pages = data.get("query", {}).get("pages", [])
    if not pages or "imageinfo" not in pages[0]:
        return None
    info = pages[0]["imageinfo"][0]
    meta = info.get("extmetadata", {})

    def _meta(key, default=""):
        v = meta.get(key, {})
        if isinstance(v, dict):
            v = v.get("value", default)
        # strip basic HTML tags Commons sometimes returns
        return re.sub(r"<[^>]+>", "", str(v)).strip()

    return {
        "title": file_title,
        "url_full": info.get("url"),
        "url_thumb": info.get("thumburl") or info.get("url"),
        "width": info.get("width", 0),
        "height": info.get("height", 0),
        "mime": info.get("mime", ""),
        "page_url": info.get("descriptionurl"),
        "artist": _meta("Artist"),
        "credit": _meta("Credit"),
        "license_short": _meta("LicenseShortName"),
        "license_url": _meta("LicenseUrl"),
        "object_name": _meta("ObjectName"),
    }


def passes_filters(info, expect_landscape=True):
    """Quality gate. Returns (ok, reason_if_rejected)."""
    if not info:
        return False, "no metadata"
    w, h = info.get("width", 0), info.get("height", 0)
    if w < MIN_WIDTH:
        return False, f"too small ({w}px)"
    mime = info.get("mime", "")
    if mime in ("image/svg+xml", "image/gif"):
        return False, f"unwanted format ({mime})"
    title_lower = info["title"].lower()
    bad_keywords = ["map of", "diagram", "chart", "logo", "coat of arms",
                    ".svg", "flag of", "icon", "schematic"]
    if any(b in title_lower for b in bad_keywords):
        return False, f"keyword reject"
    if expect_landscape and h > 0:
        ratio = w / h
        if ratio < 0.85:  # taller-than-wide → likely a portrait/poster
            return False, f"portrait aspect ({ratio:.2f})"
    return True, ""


def best_image_for_query(query: str, expect_landscape: bool = True,
                          delay: float = DEFAULT_DELAY):
    """Top-level: search + filter + return best file's info, or None."""
    titles = search_images(query, limit=10)
    if not titles:
        return None
    for title in titles:
        time.sleep(delay)
        info = get_image_info(title)
        ok, reason = passes_filters(info, expect_landscape=expect_landscape)
        if ok:
            print(f"  ✓ {title} ({info['width']}×{info['height']})")
            return info
        else:
            print(f"  · skip {title}: {reason}")
    print(f"  ! no match for '{query}'")
    return None


# ----------------------------------------------------------------
# Per-island slot enumeration
# ----------------------------------------------------------------
def enumerate_slots(island_key, data):
    """Return list of slots needing an image. Each slot is:
       {kind, path, query, expect_landscape, label}
    """
    slots = []

    # Get the island's display name in English to qualify location-based queries
    # (Wikimedia search needs disambiguation when island names overlap with words)
    location_qualifier = data.get("name") or island_key.title()

    # --- beaches ---
    for i, b in enumerate(data.get("beaches", [])):
        if b.get("photo"):
            continue  # already has one
        # Prefer the existing 'commons' filename hint when available
        commons_hint = b.get("commons")  # e.g. "Balos_Beach_Crete.jpg"
        if commons_hint:
            # Strip extension and underscores → searchable phrase
            q = commons_hint.rsplit(".", 1)[0].replace("_", " ")
        else:
            q = f"{b.get('name', '')} beach {location_qualifier}"
        slots.append({
            "kind": "beach",
            "path": ["beaches", i, "photo"],
            "query": q.strip(),
            "expect_landscape": True,
            "label": f"{island_key} / beach[{i}] {b.get('name', '?')}",
        })

    # --- day stops ---
    for di, day in enumerate(data.get("itinerary", {}).get("days", [])):
        for si, stop in enumerate(day.get("stops", [])):
            if stop.get("photo"):
                continue
            # Use wiki URL as a strong hint if present
            wiki = stop.get("wiki", "")
            stop_name = stop.get("name", "")
            if wiki:
                # Pull the article slug, e.g. ".../wiki/Knossos" → "Knossos"
                m = re.search(r"/wiki/([^#?]+)", wiki)
                slug = m.group(1).replace("_", " ") if m else stop_name
                q = f"{slug} {location_qualifier}"
            else:
                q = f"{stop_name} {location_qualifier}"
            slots.append({
                "kind": "day_stop",
                "path": ["itinerary", "days", di, "stops", si, "photo"],
                "query": q.strip(),
                "expect_landscape": True,
                "label": f"{island_key} / day{day.get('day','?')}.stop{si} {stop_name}",
            })

    # --- specialties (food) ---
    for i, s in enumerate(data.get("specialties", [])):
        if s.get("photo"):
            continue
        slots.append({
            "kind": "specialty",
            "path": ["specialties", i, "photo"],
            "query": f"{s.get('name', '')} Greek food {location_qualifier}",
            "expect_landscape": True,
            "label": f"{island_key} / specialty[{i}] {s.get('name','?')}",
        })

    # --- crafts ---
    for i, c in enumerate(data.get("crafts", [])):
        if c.get("photo"):
            continue
        slots.append({
            "kind": "craft",
            "path": ["crafts", i, "photo"],
            "query": f"{c.get('name', '')} {location_qualifier} craft",
            "expect_landscape": True,
            "label": f"{island_key} / craft[{i}] {c.get('name','?')}",
        })

    # --- festivals ---
    for i, f in enumerate(data.get("festivals", [])):
        if f.get("photo"):
            continue
        slots.append({
            "kind": "festival",
            "path": ["festivals", i, "photo"],
            "query": f"{f.get('name', '')} {location_qualifier}",
            "expect_landscape": True,
            "label": f"{island_key} / festival[{i}] {f.get('name','?')}",
        })

    return slots


# ----------------------------------------------------------------
# Main
# ----------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--islands", default="islands",
                    help="path to islands/ directory")
    ap.add_argument("--out", default="crete-image-patch.json",
                    help="output patch file")
    ap.add_argument("--keys", default="chania,rethymno,heraklion,lasithi,gavdos",
                    help="comma-separated island keys to process")
    ap.add_argument("--delay", type=float, default=DEFAULT_DELAY,
                    help="seconds between API calls")
    args = ap.parse_args()

    islands_dir = Path(args.islands)
    keys = [k.strip() for k in args.keys.split(",") if k.strip()]
    patch = {}  # { island_key: [ {path, value} ] }

    for k in keys:
        f = islands_dir / f"{k}.json"
        if not f.exists():
            print(f"! skip {k}: file missing")
            continue
        data = json.loads(f.read_text())
        slots = enumerate_slots(k, data)
        print(f"\n=== {k}: {len(slots)} slots to fill ===")
        if not slots:
            continue
        patch[k] = []
        for slot in slots:
            print(f"\n[{slot['label']}]")
            print(f"  query: {slot['query']}")
            info = best_image_for_query(
                slot["query"],
                expect_landscape=slot["expect_landscape"],
                delay=args.delay,
            )
            if not info:
                continue
            patch[k].append({
                "path": slot["path"],
                "value": {
                    "url": info["url_thumb"] or info["url_full"],
                    "url_full": info["url_full"],
                    "width": info["width"],
                    "height": info["height"],
                    "page_url": info["page_url"],
                    "artist": info["artist"][:200],
                    "credit": info["credit"][:200],
                    "license": info["license_short"],
                    "license_url": info["license_url"],
                    "wikimedia_title": info["title"],
                },
            })

    Path(args.out).write_text(json.dumps(patch, ensure_ascii=False, indent=2))
    total = sum(len(p) for p in patch.values())
    print(f"\n\n✓ Wrote {args.out} with {total} image picks across {len(patch)} islands")
    print(f"  Send this file to Claude in your next turn to apply it to the island JSONs.")


if __name__ == "__main__":
    main()
