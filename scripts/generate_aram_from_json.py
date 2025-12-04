import json
from pathlib import Path
from datetime import date

ROOT = Path(__file__).resolve().parent.parent
TOPICS_DIR = ROOT / "Writerside" / "topics"
JSON_PATH = TOPICS_DIR / "Aram-data.json"
# 先輸出到 Aram.generated.md，避免直接覆蓋手寫版 Aram.md
MD_PATH = TOPICS_DIR / "Aram.generated.md"


def load_data():
    with JSON_PATH.open("r", encoding="utf-8") as f:
        return json.load(f)


def render_coverage_block(coverage: dict) -> str:
    # 保留 JSON 原樣方便日後工具解析
    json_text = json.dumps(coverage, ensure_ascii=False, indent=2)
    lines = ["<!--", "ARAM-DATA-COVERAGE:", json_text, "-->"]

    human = [
        "> 資料來源覆蓋範圍（巴哈 ARAM 大混戰討論串)",
    ]
    bahamut = coverage.get("bahamut") or {}
    from_page = bahamut.get("from_page")
    to_page = bahamut.get("to_page")
    last_floor = bahamut.get("last_floor")
    last_url = bahamut.get("last_url")
    last_updated = coverage.get("last_updated") or str(date.today())

    if from_page and to_page:
        human.append(f"> - 已處理頁數：{from_page}–{to_page} 頁")
    if last_floor is not None:
        human.append(f"> - 最後處理樓層：第 {to_page} 頁 第 {last_floor} 樓")
    if last_url:
        human.append(f"> - 最後處理網址：{last_url}")
    human.append(f"> - 最後更新時間：{last_updated}")

    return "\n".join(lines) + "\n" + "\n".join(human) + "\n\n"


def render_hero_section(hero: dict) -> str:
    name_zh = hero.get("hero")
    name_en = hero.get("hero_en") or ""
    title = f"### 英雄：{name_zh} {name_en}".rstrip()

    core = hero.get("core_augments") or []
    build_notes = hero.get("build_notes") or ""

    lines = [title, "", "- 主要核心海克斯：" + ("、".join(core) if core else "（尚未整理）"), ""]

    if build_notes:
        lines.append("**玩法與選擇說明**")
        lines.append("")
        lines.append(build_notes)
        lines.append("")

    return "\n".join(lines) + "\n"


def render_heroes(hero_synergy: list) -> str:
    if not hero_synergy:
        return ""

    blocks = ["## 英雄 × 海克斯推薦表", "", "> 本章內容由中介 JSON (`hero_synergy`) 自動生成，僅列出已整理的英雄。", ""]
    for hero in hero_synergy:
        blocks.append(render_hero_section(hero))
    return "\n".join(blocks)


def render_augments(augments: list) -> str:
    if not augments:
        return ""

    lines = ["## 代表性海克斯增幅摘要", "", "> 本章內容由中介 JSON (`augments_summary`) 自動生成。", ""]

    for aug in augments:
        zh = aug.get("augment_name_zh")
        en = aug.get("augment_name_en")
        rarity = aug.get("rarity")
        strong_for = aug.get("strong_for") or []
        summary = aug.get("summary") or ""
        bugs = aug.get("bugs") or []

        title = f"### {en}（{zh}）" if en else f"### {zh}"
        lines.append(title)
        if rarity:
            lines.append(f"- 稀有度：{rarity}")
        if strong_for:
            lines.append("- 推薦英雄 / 類型：" + "、".join(strong_for))
        if summary:
            lines.append("- 摘要：" + summary)
        if bugs:
            lines.append("- 已知問題：")
            for b in bugs:
                lines.append(f"  - {b}")
        lines.append("")

    return "\n".join(lines)


def render_bugs(bugs: list) -> str:
    if not bugs:
        return ""
    lines = ["## Bug / 坑點與翻譯雷區", "", "> 本章由中介 JSON (`bugs_and_traps`) 自動生成。", ""]
    for item in bugs:
        title = item.get("title") or "(未命名)"
        typ = item.get("type") or "info"
        detail = item.get("detail") or ""
        lines.append(f"- [{typ}] {title}")
        if detail:
            lines.append(f"  - {detail}")
    lines.append("")
    return "\n".join(lines)


def render_macro(macro_tips: list) -> str:
    if not macro_tips:
        return ""
    lines = ["## 模式與增幅整體原則摘要", ""]
    for tip in macro_tips:
        lines.append(f"- {tip}")
    lines.append("")
    return "\n".join(lines)


def build_markdown(data: dict) -> str:
    coverage = data.get("coverage") or {}
    augments = data.get("augments_summary") or []
    heroes = data.get("hero_synergy") or []
    bugs = data.get("bugs_and_traps") or []
    macro = data.get("macro_tips") or []

    parts = [
        render_coverage_block(coverage),
        "# LoL ARAM 大混戰（ARAM Mayhem）海克斯增幅與玩法總整理\n",
        "## 1. 英雄 × 海克斯建議索引\n",
        render_heroes(heroes),
        "\n",
        render_augments(augments),
        "\n",
        render_bugs(bugs),
        "\n",
        render_macro(macro),
        "> 本檔案為由中介 JSON 自動生成；若要更新內容，請先依 `/Writerside/topics/Aram-maintain.md` 5.1～5.3 更新 JSON，\n> 再重新執行產生腳本覆寫本檔。\n",
    ]
    return "\n".join(p for p in parts if p)


def main() -> None:
    data = load_data()
    md = build_markdown(data)
    MD_PATH.write_text(md, encoding="utf-8")
    print(f"Generated {MD_PATH} from {JSON_PATH}")


if __name__ == "__main__":
    main()

