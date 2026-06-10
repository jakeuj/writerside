#!/usr/bin/env python3
"""
補齊 Writerside topic 內的空 Markdown image alt text。

規則：
- 不修改 fenced code block 內的文字。
- 不覆蓋既有非空 alt text。
- 優先使用圖片前一行短文字，其次最近標題，最後使用 URL 檔名。
"""

from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import unquote, urlparse


TOPICS_DIR = Path("Writerside/topics")
IMAGE_PATTERN = re.compile(r"!\[\]\(([^)\n]*)\)")
FENCE_PATTERN = re.compile(r"^ {0,3}(```+|~~~+)")


def clean_context(text: str) -> str:
    """把 Markdown 行清成適合放進 alt text 的短句。"""
    text = re.sub(r"!\[[^\]]*\]\([^)]*\)", "", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", text)
    text = re.sub(r"^#{1,6}\s*", "", text)
    text = re.sub(r"^>\s*", "", text)
    text = re.sub(r"^[-*+]\s+", "", text)
    text = re.sub(r"^\d+\.\s+", "", text)
    text = re.sub(r"[*_`~<>]", "", text)
    text = re.sub(r"\s+", " ", text.replace("&nbsp;", " ")).strip()
    return text[:80].strip()


def alt_from_url(url: str) -> str:
    parsed = urlparse(url)
    if "card.psnprofiles.com" in parsed.netloc:
        return "PSNProfiles 卡片"

    basename = unquote(Path(parsed.path).name)
    stem = re.sub(r"\.(png|jpe?g|gif|webp|svg|bmp)$", "", basename, flags=re.I)
    stem = re.sub(r"[-_]+", " ", stem).strip()
    return f"圖片 {stem}" if stem else "圖片"


def choose_alt(url: str, previous_text: str, current_heading: str) -> str:
    if "card.psnprofiles.com" in url:
        return "PSNProfiles 卡片"

    if previous_text:
        return previous_text

    if current_heading:
        return current_heading

    return alt_from_url(url)


def process_file(path: Path) -> int:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    changed = 0
    in_fence = False
    fence_marker = ""
    current_heading = ""
    previous_text = ""
    output: list[str] = []

    for line in lines:
        fence_match = FENCE_PATTERN.match(line)
        if fence_match:
            marker = fence_match.group(1)
            if in_fence and marker.startswith(fence_marker[0]):
                in_fence = False
                fence_marker = ""
            elif not in_fence:
                in_fence = True
                fence_marker = marker
            output.append(line)
            continue

        new_line = line
        if not in_fence and IMAGE_PATTERN.search(line):
            image_index = 0

            def replace(match: re.Match[str]) -> str:
                nonlocal changed, image_index
                image_index += 1
                url = match.group(1)
                alt = choose_alt(url, previous_text, current_heading)
                if image_index > 1 and alt != "PSNProfiles 卡片":
                    alt = f"{alt} {image_index}"
                changed += 1
                return f"![{alt}]({url})"

            new_line = IMAGE_PATTERN.sub(replace, line)

        output.append(new_line)

        if not in_fence:
            heading_match = re.match(r"^(#{1,6})\s+(.+?)\s*$", new_line)
            if heading_match:
                current_heading = clean_context(heading_match.group(2))

            context = clean_context(new_line)
            if context:
                previous_text = context

    if changed:
        path.write_text("".join(output), encoding="utf-8")

    return changed


def main() -> None:
    total_changed = 0
    changed_files = 0
    for path in sorted(TOPICS_DIR.glob("**/*.md")):
        changed = process_file(path)
        if changed:
            changed_files += 1
            total_changed += changed
            print(f"{path}: {changed}")

    print(f"\n已補齊 {changed_files} 個檔案中的 {total_changed} 個空 alt text。")


if __name__ == "__main__":
    main()
