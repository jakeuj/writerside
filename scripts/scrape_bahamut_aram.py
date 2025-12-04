#!/usr/bin/env python3
"""
Scrape Bahamut ARAM Mayhem discussion thread and update Aram-data.json.

Usage:
    python3 scripts/scrape_bahamut_aram.py [--from-page 1] [--to-page 15]

Requires: requests, beautifulsoup4
    pip install requests beautifulsoup4
"""
import argparse
import json
import re
import time
from pathlib import Path

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as e:
    raise SystemExit(
        "Missing dependencies. Run:\n  pip install requests beautifulsoup4"
    ) from e

ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT / "Writerside" / "topics"
JSON_PATH = TOPICS_DIR / "Aram-data.json"

BASE_URL = "https://forum.gamer.com.tw/C.php"
BSN = 17532
SNA = 705476

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36"
}


def fetch_page(page: int) -> str:
    url = f"{BASE_URL}?bsn={BSN}&snA={SNA}&page={page}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def parse_floors(html: str) -> list[dict]:
    soup = BeautifulSoup(html, "html.parser")
    floors = []
    for section in soup.select("section.c-section"):
        floor_el = section.select_one("a.floor")
        floor_text = floor_el.get_text(strip=True) if floor_el else "0"
        # 樓主 = 0, 其他為數字
        if floor_text == "樓主":
            floor_num = 0
        else:
            try:
                floor_num = int(floor_text)
            except ValueError:
                floor_num = 0
        content_el = section.select_one("div.c-article__content")
        text = content_el.get_text("\n", strip=True) if content_el else ""
        if text:
            floors.append({"floor": floor_num, "text": text})
    return floors


def detect_last_page(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    last_link = soup.select_one("p.BH-pagebtnA a:last-child")
    if last_link and last_link.get("href"):
        m = re.search(r"page=(\d+)", last_link["href"])
        if m:
            return int(m.group(1))
    return 1


def scrape_pages(from_page: int, to_page: int) -> list[dict]:
    all_floors = []
    for p in range(from_page, to_page + 1):
        print(f"Fetching page {p}...")
        html = fetch_page(p)
        floors = parse_floors(html)
        for f in floors:
            f["page"] = p
        all_floors.extend(floors)
        time.sleep(1)  # polite delay
    return all_floors


def load_json() -> dict:
    if JSON_PATH.exists():
        with JSON_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {}


def save_json(data: dict) -> None:
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {JSON_PATH}")


def update_coverage(data: dict, from_page: int, to_page: int, last_page: int, last_floor: int) -> None:
    from datetime import date
    cov = data.setdefault("coverage", {})
    cov["note"] = "SCRAPED_FROM_BAHAMUT"
    baha = cov.setdefault("bahamut", {})
    baha["bsn"] = BSN
    baha["snA"] = SNA
    baha["from_page"] = from_page
    baha["to_page"] = to_page
    baha["last_page"] = last_page
    baha["last_floor"] = last_floor
    baha["last_url"] = f"{BASE_URL}?bsn={BSN}&snA={SNA}&page={to_page}"
    cov["last_updated"] = str(date.today())


def append_raw_floors(data: dict, floors: list[dict]) -> None:
    existing = data.setdefault("raw_floors", [])
    seen = {(f["page"], f["floor"]) for f in existing}
    for f in floors:
        key = (f["page"], f["floor"])
        if key not in seen:
            existing.append(f)
            seen.add(key)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Bahamut ARAM thread")
    parser.add_argument("--from-page", type=int, default=1)
    parser.add_argument("--to-page", type=int, default=15)
    args = parser.parse_args()

    # detect last page from page 1
    html_first = fetch_page(1)
    last_page = detect_last_page(html_first)
    print(f"Detected last page: {last_page}")

    to_page = min(args.to_page, last_page)
    floors = scrape_pages(args.from_page, to_page)
    print(f"Scraped {len(floors)} floors from pages {args.from_page}-{to_page}")

    data = load_json()
    update_coverage(data, args.from_page, to_page, last_page, floors[-1]["floor"] if floors else 0)
    append_raw_floors(data, floors)
    save_json(data)


if __name__ == "__main__":
    main()

