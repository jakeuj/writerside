import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT / "Writerside" / "topics"
JSON_PATH = TOPICS_DIR / "Aram-data.json"
KB_PATH = TOPICS_DIR / "Aram-kb.md"


def load_data():
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_hero_index(heroes):
    if not heroes:
        return ""
    lines = [
        "## 英雄 × 海克斯建議索引",
        "",
        "| 英雄 | 英文 | 核心海克斯 | 簡要備註 |",
        "| --- | --- | --- | --- |",
    ]
    for h in heroes:
        zh = h.get("hero") or "?"
        en = h.get("hero_en") or ""
        core = "、".join(h.get("core_augments") or []) or "(待補)"
        note = (h.get("build_notes") or "").replace("\n", " ")
        if len(note) > 60:
            note = note[:57] + "..."
        lines.append(f"| {zh} | {en} | {core} | {note} |")
    lines.append("")
    return "\n".join(lines)


def render_augment_index(augments):
    if not augments:
        return ""
    lines = [
        "## Augment → 英雄 / 類型 對照表",
        "",
        "| 增幅 | 稀有度 | 適合英雄 / 類型 | 摘要 |",
        "| --- | --- | --- | --- |",
    ]
    for a in augments:
        zh = a.get("augment_name_zh") or "?"
        en = a.get("augment_name_en") or ""
        name = f"{en} ({zh})" if en else zh
        rarity = a.get("rarity") or "?"
        strong_for = "、".join(a.get("strong_for") or []) or "(待補)"
        summary = (a.get("summary") or "").replace("\n", " ")
        if len(summary) > 80:
            summary = summary[:77] + "..."
        lines.append(f"| {name} | {rarity} | {strong_for} | {summary} |")
    lines.append("")
    return "\n".join(lines)


def render_bugs(bugs):
    if not bugs:
        return ""
    lines = ["## Bug / 坑點與翻譯雷區", ""]
    for b in bugs:
        title = b.get("title") or "(未命名)"
        typ = b.get("type") or "info"
        detail = b.get("detail") or ""
        lines.append(f"- [{typ}] {title}")
        if detail:
            lines.append(f"  - {detail}")
    lines.append("")
    return "\n".join(lines)


def render_macro(macro_tips):
    if not macro_tips:
        return ""
    lines = ["## 模式與增幅整體原則摘要", ""]
    for tip in macro_tips:
        lines.append(f"- {tip}")
    lines.append("")
    return "\n".join(lines)


def build_kb_md(data):
    heroes = data.get("hero_synergy") or []
    augments = data.get("augments_summary") or []
    bugs = data.get("bugs_and_traps") or []
    macro = data.get("macro_tips") or []

    parts = [
        "# LoL ARAM 大混戰海克斯增幅知識庫（給 ChatGPT 用）\n",
        "## 使用說明（給 ChatGPT 看）\n",
        "- 把本檔視為 ARAM 大混戰（ARAM Mayhem）海克斯增幅 + 英雄搭配的知識庫。",
        "- 玩家問特定英雄時，優先查《英雄 × 海克斯建議索引》。",
        "- 玩家問某顆增幅時，優先查《Augment → 英雄 / 類型 對照表》。",
        "- 回答時請用繁體中文，語氣實戰向但保持條理清晰。\n",
        render_macro(macro),
        render_hero_index(heroes),
        render_augment_index(augments),
        render_bugs(bugs),
        "\n> 資料來源與更新流程請參考專案內 `/Writerside/topics/Aram-maintain.md` 5.1～5.3。\n",
    ]
    return "\n".join(p for p in parts if p)


def main() -> None:
    data = load_data()
    md = build_kb_md(data)
    KB_PATH.write_text(md, encoding="utf-8")
    print(f"Generated {KB_PATH} from {JSON_PATH}")


if __name__ == "__main__":
    main()

