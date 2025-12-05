#!/usr/bin/env python3
"""
Extract structured insights from Aram-baha-raw.json and merge into Aram-data.json.

This script parses the scraped Bahamut floor text and extracts:
- Hero + Augment synergy mentions
- Bug / trap reports
- Macro tips

Usage:
    python3 scripts/extract_aram_insights.py
"""
import json
import re
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT / "Writerside" / "topics"
RAW_PATH = TOPICS_DIR / "Aram-baha-raw.json"
JSON_PATH = TOPICS_DIR / "Aram-data.json"

# 常見英雄名（中文）- 從巴哈討論串常見的英雄名
HERO_NAMES = [
    "雷茲", "剛普拉克", "札克", "蒙多", "煞蜜拉", "伊澤", "吉茵珂絲", "凱特琳", "汎", "燼",
    "葛雷夫", "烏迪爾", "派克", "火人", "蓋倫", "乙", "艾希", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
    "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙", "乙",
]
# 過濾掉 placeholder
HERO_NAMES = [h for h in HERO_NAMES if h != "乙"]
HERO_PATTERN = re.compile(r"(" + "|".join(re.escape(h) for h in HERO_NAMES) + r")")

# 常見增幅名（中文）- 可持續擴充
AUGMENT_PATTERN = re.compile(
    r"(基本功|回歸基本功|死亡循環|拔劍|拔劍吧|封我為王|帽上加帽|球鞋收藏家|"
    r"煽動群眾|輕舞飛揚|導彈|煉獄|物轉魔|物轉法|雪地|幻影武器|彈幕神童|"
    r"升級彎刀|升級傲慢|狂躁|魔力轉血量|溢流|水龍魂|超狙|頂狙|強化射程|埃爾文|"
    r"Omni Soul|Back To Basics|Circle of Death|Draw Your Sword)"
)

# Bug / 問題關鍵字
BUG_KEYWORDS = ["bug", "BUG", "Bug", "問題", "不符", "沒有生效", "修", "壞", "錯"]
TRAP_KEYWORDS = ["噁心", "垃圾", "難", "坑", "雷", "不配"]


def load_raw() -> dict:
    """Load raw Bahamut data."""
    if not RAW_PATH.exists():
        return {"floors": []}
    with RAW_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def load_data() -> dict:
    """Load main data file."""
    if not JSON_PATH.exists():
        return {}
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_data(data: dict) -> None:
    with JSON_PATH.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"Saved {JSON_PATH}")


def get_floor_text(floor: dict) -> str:
    """Get all text from a floor including comments."""
    texts = [floor.get("content", "") or floor.get("text", "")]
    for comment in floor.get("comments", []):
        texts.append(comment.get("content", ""))
    return "\n".join(texts)


def extract_hero_augment_mentions(floors: list[dict]) -> dict:
    """Extract hero + augment co-mentions from floor text."""
    hero_augments = defaultdict(set)
    for f in floors:
        text = get_floor_text(f)
        heroes = set(HERO_PATTERN.findall(text))
        augments = set(AUGMENT_PATTERN.findall(text))
        for h in heroes:
            for a in augments:
                hero_augments[h].add(a)
    return hero_augments


def extract_bugs_and_traps(floors: list[dict]) -> list[dict]:
    """Extract bug / trap mentions from floor text."""
    results = []
    seen = set()
    for f in floors:
        text = get_floor_text(f)
        is_bug = any(kw in text for kw in BUG_KEYWORDS)
        is_trap = any(kw in text for kw in TRAP_KEYWORDS)
        if is_bug or is_trap:
            # 取前 100 字作為摘要
            summary = text[:100].replace("\n", " ")
            if summary not in seen:
                seen.add(summary)
                results.append({
                    "type": "bug" if is_bug else "trap",
                    "title": summary[:40] + ("..." if len(summary) > 40 else ""),
                    "detail": summary,
                    "page": f.get("page"),
                    "floor": f.get("floor"),
                })
    return results


def extract_macro_tips(floors: list[dict]) -> list[str]:
    """Extract general macro tips (heuristic: longer posts with strategy keywords)."""
    tips = []
    seen = set()
    strategy_kw = ["優先", "建議", "核心", "出裝", "順序", "前期", "後期", "線權", "清線"]
    for f in floors:
        text = get_floor_text(f)
        if len(text) > 80 and any(kw in text for kw in strategy_kw):
            tip = text[:120].replace("\n", " ")
            if tip not in seen:
                seen.add(tip)
                tips.append(tip)
    return tips[:20]  # 最多 20 條


def merge_hero_synergy(data: dict, hero_augments: dict) -> None:
    """Merge extracted hero-augment pairs into hero_synergy."""
    existing = {h["hero"]: h for h in data.get("hero_synergy", [])}
    for hero, augments in hero_augments.items():
        if hero in existing:
            # 合併增幅
            existing[hero]["core_augments"] = list(
                set(existing[hero].get("core_augments", [])) | augments
            )
        else:
            existing[hero] = {
                "hero": hero,
                "hero_en": "",
                "core_augments": list(augments),
                "build_notes": "(自動從巴哈討論串萃取)",
            }
    data["hero_synergy"] = list(existing.values())


def merge_bugs_and_traps(data: dict, new_bugs: list[dict]) -> None:
    """Merge new bugs/traps into bugs_and_traps."""
    existing = data.get("bugs_and_traps", [])
    existing_titles = {b["title"] for b in existing}
    for b in new_bugs:
        if b["title"] not in existing_titles:
            existing.append(b)
            existing_titles.add(b["title"])
    data["bugs_and_traps"] = existing


def merge_macro_tips(data: dict, new_tips: list[str]) -> None:
    """Merge new macro tips."""
    existing = set(data.get("macro_tips", []))
    for t in new_tips:
        existing.add(t)
    data["macro_tips"] = list(existing)[:30]


def main() -> None:
    # Load raw Bahamut data
    raw = load_raw()
    floors = raw.get("floors", [])
    if not floors:
        print(f"No floors found in {RAW_PATH}. Run scrape_bahamut_aram.py first.")
        return

    print(f"Processing {len(floors)} floors from {RAW_PATH}...")

    hero_augments = extract_hero_augment_mentions(floors)
    print(f"Found {len(hero_augments)} heroes with augment mentions")

    bugs = extract_bugs_and_traps(floors)
    print(f"Found {len(bugs)} bug/trap mentions")

    tips = extract_macro_tips(floors)
    print(f"Found {len(tips)} macro tips")

    # Load and update main data file
    data = load_data()
    merge_hero_synergy(data, hero_augments)
    merge_bugs_and_traps(data, bugs)
    merge_macro_tips(data, tips)

    save_data(data)
    print("Done!")


if __name__ == "__main__":
    main()

