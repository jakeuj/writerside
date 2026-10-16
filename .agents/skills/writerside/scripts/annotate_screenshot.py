#!/usr/bin/env python3
"""依 JSON 規格在截圖上畫框、標籤、箭頭與遮罩，供 Writerside 文章截圖使用。

用法：
    python3 annotate_screenshot.py <input.png> <output.png> <spec.json | ->

spec 格式（座標一律是原圖像素，左上為 0,0）：
{
  "items": [
    {"mask": [x1, y1, x2, y2]},
    {"box": [x1, y1, x2, y2], "color": "red", "width": 6},
    {"label": "① 幣別 USD ≠ 單據 EUR → 被篩掉", "at": [x, y], "color": "red",
     "size": 30, "arrow_to": [x, y]}
  ]
}

color：red（原因、異常、不要做）、green（結果、正常、確認點）、gray（背景說明）、blue（要操作的按鈕或欄位），或 "#RRGGBB"。
items 依序繪製；mask 用實心框遮住帳號、組織名稱、卡號、金鑰或其他識別資料；公開文章的遮罩要在存進 Writerside/images 之前完成。
"""
import json
import math
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

COLORS = {
    "red": (220, 30, 30),
    "green": (20, 150, 60),
    "gray": (90, 90, 90),
    "blue": (30, 90, 220),
}

FONT_CANDIDATES = [
    "/System/Library/Fonts/STHeiti Medium.ttc",
    "/System/Library/Fonts/Hiragino Sans GB.ttc",
    "/System/Library/Fonts/Supplemental/Arial Unicode.ttf",
    "C:/Windows/Fonts/msjh.ttc",
    "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc",
    "/usr/share/fonts/noto-cjk/NotoSansCJK-Regular.ttc",
]


def load_font(size):
    for path in FONT_CANDIDATES:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    sys.exit("找不到中文字型，請在 FONT_CANDIDATES 加入本機 CJK 字型路徑")


def color_of(name):
    if name.startswith("#"):
        return tuple(int(name[i:i + 2], 16) for i in (1, 3, 5))
    return COLORS[name]


def draw_arrow(draw, start, end, color, width=4):
    draw.line([start, end], fill=color, width=width)
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    for delta in (2.6, -2.6):
        tip = (end[0] + 18 * math.cos(angle + delta), end[1] + 18 * math.sin(angle + delta))
        draw.line([end, tip], fill=color, width=width)


def arrow_start(bbox, target):
    left, top, right, bottom = bbox
    cx, cy = (left + right) / 2, (top + bottom) / 2
    if target[1] < top:
        return (min(max(target[0], left), right), top)
    if target[1] > bottom:
        return (min(max(target[0], left), right), bottom)
    return (left if target[0] < cx else right, cy)


def main():
    if len(sys.argv) != 4:
        sys.exit(__doc__)
    src, dst, spec_path = sys.argv[1:]
    spec = json.load(sys.stdin if spec_path == "-" else open(spec_path, encoding="utf-8"))

    img = Image.open(src).convert("RGB")
    draw = ImageDraw.Draw(img)

    for item in spec["items"]:
        if "mask" in item:
            draw.rectangle(item["mask"], fill=(40, 40, 40))
            continue
        color = color_of(item.get("color", "red"))
        if "box" in item:
            draw.rectangle(item["box"], outline=color, width=item.get("width", 5))
        if "label" in item:
            font = load_font(item.get("size", 30))
            x, y = item["at"]
            left, top, right, bottom = draw.textbbox((x, y), item["label"], font=font)
            bbox = (left - 8, top - 8, right + 8, bottom + 8)
            draw.rectangle(bbox, fill=(255, 255, 255), outline=color, width=3)
            draw.text((x, y), item["label"], fill=color, font=font)
            if "arrow_to" in item:
                target = tuple(item["arrow_to"])
                draw_arrow(draw, arrow_start(bbox, target), target, color)

    img.save(dst, optimize=True)
    print(f"{dst} {img.size[0]}x{img.size[1]}")


if __name__ == "__main__":
    main()
