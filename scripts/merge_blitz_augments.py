#!/usr/bin/env python3
"""
Merge Blitz ARAM Mayhem augments data into Aram-data.json.
This script takes a JSON file with Blitz augment data and merges it into the main data file.
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT / "Writerside" / "topics"
JSON_PATH = TOPICS_DIR / "Aram-data.json"
BLITZ_PATH = TOPICS_DIR / "Aram-blitz-augments.json"


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, data: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def merge_blitz_data(main_data: dict, blitz_augments: list) -> dict:
    """Merge Blitz augment data into main data structure."""
    
    # Create blitz_augments section if not exists
    if "blitz_augments" not in main_data:
        main_data["blitz_augments"] = []
    
    # Replace with new Blitz data
    main_data["blitz_augments"] = blitz_augments
    
    # Update coverage info
    main_data["coverage"]["blitz"] = {
        "url": "https://blitz.gg/lol/aram-mayhem-augments",
        "augment_count": len(blitz_augments),
        "last_updated": main_data["coverage"].get("last_updated", "2025-12-04")
    }
    
    # Also merge into augments_summary for KB generation
    existing_names = {a.get("augment_name_en") for a in main_data.get("augments_summary", [])}
    
    for aug in blitz_augments:
        if aug["name"] not in existing_names:
            main_data["augments_summary"].append({
                "augment_name_zh": "",  # Will need translation
                "augment_name_en": aug["name"],
                "rarity": aug["rarity"],
                "tier": aug["tier"],
                "strong_for": aug["champions"],
                "summary": f"Blitz Tier {aug['tier']} - 推薦英雄: {', '.join(aug['champions'][:3])}",
                "bugs": []
            })
    
    return main_data


def main():
    if not BLITZ_PATH.exists():
        print(f"Error: {BLITZ_PATH} not found. Please create it first.")
        return
    
    main_data = load_json(JSON_PATH)
    blitz_augments = load_json(BLITZ_PATH)
    
    merged = merge_blitz_data(main_data, blitz_augments)
    save_json(JSON_PATH, merged)
    
    print(f"Merged {len(blitz_augments)} Blitz augments into {JSON_PATH}")
    print(f"Total augments_summary: {len(merged.get('augments_summary', []))}")


if __name__ == "__main__":
    main()

