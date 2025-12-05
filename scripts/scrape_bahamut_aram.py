#!/usr/bin/env python3
"""
Scrape Bahamut ARAM Mayhem discussion thread and save to Aram-baha-raw.json.

支援增量更新：自動從上次進度繼續抓取，不重複處理舊資料。
支援留言抓取：透過 AJAX API 抓取每樓的留言。

Usage:
    # 增量更新（從上次進度繼續，包含留言）
    python3 scripts/scrape_bahamut_aram.py

    # 強制重新抓取指定範圍
    python3 scripts/scrape_bahamut_aram.py --from-page 1 --to-page 15 --force

    # 只抓取新頁面（從上次最後一頁開始）
    python3 scripts/scrape_bahamut_aram.py --new-only

    # 只更新留言（不抓取新樓層）
    python3 scripts/scrape_bahamut_aram.py --comments-only

Requires: requests, beautifulsoup4
    pip install requests beautifulsoup4
"""
import argparse
import json
import re
import time
from datetime import date
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
RAW_PATH = TOPICS_DIR / "Aram-baha-raw.json"

BASE_URL = "https://forum.gamer.com.tw/C.php"
COMMENTS_API = "https://forum.gamer.com.tw/ajax/moreCommend.php"
BSN = 17532
SNA = 705476

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "X-Requested-With": "XMLHttpRequest",
}


def fetch_page(page: int) -> str:
    url = f"{BASE_URL}?bsn={BSN}&snA={SNA}&page={page}"
    resp = requests.get(url, headers=HEADERS, timeout=30)
    resp.raise_for_status()
    return resp.text


def fetch_comments(snB: str) -> list[dict]:
    """
    Fetch comments for a floor using the AJAX API.
    API: GET /ajax/moreCommend.php?bsn={BSN}&snB={snB}&returnHtml=1
    Returns list of comments with floor, author, content.
    """
    url = f"{COMMENTS_API}?bsn={BSN}&snB={snB}&returnHtml=1"
    try:
        resp = requests.get(url, headers=HEADERS, timeout=30)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"  Warning: Failed to fetch comments for snB={snB}: {e}")
        return []

    comments = []
    html_list = data.get("html", [])
    for html in html_list:
        soup = BeautifulSoup(html, "html.parser")
        # Extract from data-comment attribute (JSON)
        item = soup.select_one(".c-reply__item")
        if item and item.get("data-comment"):
            try:
                comment_data = json.loads(item["data-comment"])
                floor_el = soup.select_one("[name='comment_floor']")
                author_el = soup.select_one(".reply-content__user")
                comments.append({
                    "floor": floor_el.get_text(strip=True) if floor_el else "",
                    "author": author_el.get_text(strip=True) if author_el else "",
                    "content": comment_data.get("content", ""),
                })
            except json.JSONDecodeError:
                pass
    return comments


def parse_floors(html: str, page: int, fetch_comments_flag: bool = True) -> list[dict]:
    """Parse floors from HTML. Optionally fetch comments via API."""
    soup = BeautifulSoup(html, "html.parser")
    floors = []
    for section in soup.select("section.c-section"):
        floor_el = section.select_one("a.floor")
        floor_text = floor_el.get_text(strip=True) if floor_el else "樓主"

        author_el = section.select_one("a.userid")
        author = author_el.get_text(strip=True) if author_el else ""

        time_el = section.select_one("a.edittime")
        post_time = time_el.get("data-mtime", "") if time_el else ""

        content_el = section.select_one("div.c-article__content")
        content = content_el.get_text("\n", strip=True) if content_el else ""

        # Extract snB (floor ID) for comments API
        # href format: Co.php?bsn=17532&sn=6276939&subbsn=6&bPage=0
        # We need the 'sn' parameter (not 'bsn')
        snB = None
        floor_link = section.select_one("a.floor")
        if floor_link and floor_link.get("href"):
            m = re.search(r"[?&]sn=(\d+)", floor_link["href"])
            if m:
                snB = m.group(1)

        comments = []
        if fetch_comments_flag and snB:
            comments = fetch_comments(snB)
            if comments:
                print(f"    Floor {floor_text}: {len(comments)} comments")
            time.sleep(0.3)  # polite delay for comments API

        if content:
            floors.append({
                "page": page,
                "floor": floor_text,
                "snB": snB,  # Store for future comment updates
                "author": author,
                "time": post_time,
                "content": content,
                "comments": comments
            })
    return floors


def detect_last_page(html: str) -> int:
    soup = BeautifulSoup(html, "html.parser")
    last_link = soup.select_one("p.BH-pagebtnA a:last-child")
    if last_link and last_link.get("href"):
        m = re.search(r"page=(\d+)", last_link["href"])
        if m:
            return int(m.group(1))
    return 1


def get_floor_number(floor_text: str) -> int:
    """Convert floor text to number for comparison."""
    if floor_text == "樓主":
        return 0
    try:
        return int(floor_text.replace(" 樓", ""))
    except:
        return 999


def scrape_pages(from_page: int, to_page: int, skip_until: tuple = None, fetch_comments_flag: bool = True) -> list[dict]:
    """
    Scrape pages. If skip_until is provided (page, floor_num), skip floors until that point.
    """
    all_floors = []
    skipping = skip_until is not None

    for p in range(from_page, to_page + 1):
        print(f"Fetching page {p}...")
        html = fetch_page(p)
        floors = parse_floors(html, p, fetch_comments_flag)

        for f in floors:
            if skipping:
                skip_page, skip_floor_num = skip_until
                current_floor_num = get_floor_number(f["floor"])
                # Skip until we pass the last scraped position
                if p < skip_page or (p == skip_page and current_floor_num <= skip_floor_num):
                    continue
                else:
                    skipping = False
            all_floors.append(f)

        time.sleep(1)  # polite delay
    return all_floors


def update_comments_only(floors: list[dict]) -> int:
    """Update comments for all floors that have snB. Returns count of updated floors."""
    updated = 0
    for i, f in enumerate(floors):
        snB = f.get("snB")
        if not snB:
            continue
        print(f"  Updating comments for floor {f['floor']} (snB={snB})...")
        comments = fetch_comments(snB)
        if comments:
            floors[i]["comments"] = comments
            updated += 1
            print(f"    -> {len(comments)} comments")
        time.sleep(0.3)
    return updated


def load_raw() -> dict:
    if RAW_PATH.exists():
        with RAW_PATH.open("r", encoding="utf-8") as f:
            return json.load(f)
    return {
        "source": f"{BASE_URL}?bsn={BSN}&snA={SNA}",
        "title": "【討論】隨機單中：大混戰 討論串",
        "scrape_progress": {
            "last_scraped_page": 0,
            "last_scraped_floor": "",
            "total_pages": 0,
            "is_complete": False
        },
        "floors": []
    }


def save_raw(data: dict) -> None:
    with RAW_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {RAW_PATH}")


def sort_floors(floors: list[dict]) -> list[dict]:
    """Sort floors by page, then floor number."""
    def sort_key(f):
        return (f["page"], get_floor_number(f["floor"]))
    return sorted(floors, key=sort_key)


def merge_floors(existing: list[dict], new_floors: list[dict]) -> list[dict]:
    """Merge new floors into existing. Updates snB and comments for existing floors."""
    # Build index of existing floors
    existing_index = {(f["page"], f["floor"]): i for i, f in enumerate(existing)}
    added = 0
    updated = 0

    for f in new_floors:
        key = (f["page"], f["floor"])
        if key in existing_index:
            # Update existing floor with new snB and comments
            idx = existing_index[key]
            if f.get("snB") and not existing[idx].get("snB"):
                existing[idx]["snB"] = f["snB"]
            if f.get("comments"):
                existing[idx]["comments"] = f["comments"]
                updated += 1
        else:
            existing.append(f)
            existing_index[key] = len(existing) - 1
            added += 1

    print(f"Added {added} new floors, updated {updated} floors with comments")
    return sort_floors(existing)


def main() -> None:
    parser = argparse.ArgumentParser(description="Scrape Bahamut ARAM thread (支援增量更新+留言)")
    parser.add_argument("--from-page", type=int, default=None, help="起始頁碼（預設：從上次進度繼續）")
    parser.add_argument("--to-page", type=int, default=None, help="結束頁碼（預設：最後一頁）")
    parser.add_argument("--force", action="store_true", help="強制重新抓取，忽略上次進度")
    parser.add_argument("--new-only", action="store_true", help="只抓取新頁面（從上次最後一頁開始）")
    parser.add_argument("--comments-only", action="store_true", help="只更新留言（不抓取新樓層）")
    parser.add_argument("--no-comments", action="store_true", help="不抓取留言（加快速度）")
    args = parser.parse_args()

    # Load existing data
    data = load_raw()
    progress = data.get("scrape_progress", {})

    # Detect current last page
    print("Checking forum for latest page count...")
    html_first = fetch_page(1)
    current_last_page = detect_last_page(html_first)
    print(f"Forum currently has {current_last_page} pages")

    # Determine scraping range
    last_scraped_page = progress.get("last_scraped_page", 0)
    last_scraped_floor = progress.get("last_scraped_floor", "")

    if args.force:
        # Force mode: use specified range or full range
        from_page = args.from_page or 1
        to_page = args.to_page or current_last_page
        skip_until = None
        print(f"Force mode: scraping pages {from_page}-{to_page}")
    elif args.new_only:
        # New-only mode: start from last scraped page
        from_page = max(last_scraped_page, 1)
        to_page = args.to_page or current_last_page
        skip_until = (last_scraped_page, get_floor_number(last_scraped_floor)) if last_scraped_floor else None
        print(f"New-only mode: scraping pages {from_page}-{to_page}, skipping until page {last_scraped_page} floor {last_scraped_floor}")
    else:
        # Default: incremental update
        if last_scraped_page == 0:
            # First run
            from_page = args.from_page or 1
            to_page = args.to_page or current_last_page
            skip_until = None
            print(f"First run: scraping pages {from_page}-{to_page}")
        else:
            # Continue from last position
            from_page = last_scraped_page
            to_page = args.to_page or current_last_page
            skip_until = (last_scraped_page, get_floor_number(last_scraped_floor))
            print(f"Incremental update: from page {from_page} floor {last_scraped_floor} to page {to_page}")

    # Comments-only mode
    if args.comments_only:
        print("Comments-only mode: updating comments for existing floors...")
        updated = update_comments_only(data.get("floors", []))
        print(f"Updated comments for {updated} floors")
        data["last_updated"] = str(date.today())
        save_raw(data)
        return

    # Check if already complete
    if not args.force and progress.get("is_complete") and current_last_page == progress.get("total_pages"):
        print("Already complete and no new pages. Use --force to re-scrape or wait for new posts.")
        return

    # Scrape
    fetch_comments_flag = not args.no_comments
    new_floors = scrape_pages(from_page, to_page, skip_until, fetch_comments_flag)
    print(f"Scraped {len(new_floors)} new floors")

    if not new_floors and not args.force:
        print("No new floors found.")
        # Still update progress in case page count changed
        data["scrape_progress"]["total_pages"] = current_last_page
        data["last_updated"] = str(date.today())
        save_raw(data)
        return

    # Merge and save
    data["floors"] = merge_floors(data.get("floors", []), new_floors)

    # Update progress
    if data["floors"]:
        last_floor = data["floors"][-1]
        data["scrape_progress"] = {
            "last_scraped_page": last_floor["page"],
            "last_scraped_floor": last_floor["floor"],
            "total_pages": current_last_page,
            "is_complete": last_floor["page"] >= current_last_page
        }

    data["last_updated"] = str(date.today())
    save_raw(data)

    # Count total comments
    total_comments = sum(len(f.get("comments", [])) for f in data["floors"])

    print(f"\n✅ Total floors in {RAW_PATH}: {len(data['floors'])}")
    print(f"   Total comments: {total_comments}")
    print(f"   Progress: page {data['scrape_progress']['last_scraped_page']}, floor {data['scrape_progress']['last_scraped_floor']}")
    if data["scrape_progress"]["is_complete"]:
        print("   Status: Complete ✓")
    else:
        print(f"   Status: In progress ({data['scrape_progress']['last_scraped_page']}/{current_last_page} pages)")


if __name__ == "__main__":
    main()

