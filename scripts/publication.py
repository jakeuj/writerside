#!/usr/bin/env python3
"""Deterministic publication index and RSS; Python standard library only."""

import argparse
from datetime import date, datetime, time, timedelta, timezone
from email.utils import format_datetime
import html
from html.parser import HTMLParser
import json
from pathlib import Path
import re
import sys
import subprocess
from urllib.parse import urlsplit, unquote
import xml.etree.ElementTree as ET

ROOT = Path(__file__).resolve().parents[1]
FEED = "https://jakeuj.com/feed.xml"
START, END = "<!-- publications:start -->", "<!-- publications:end -->"


def plain(value):
    return html.unescape(re.sub(r"<[^>]+>", "", value)).strip()


def load(root=ROOT):
    data = json.loads((root / "data/posts.json").read_text())
    topics = root / "Writerside/topics"
    tree = ET.parse(root / "Writerside/hi.tree")
    public = {e.get("topic") for e in tree.iter() if e.get("topic")}
    seen, urls = set(), set()
    for p in data["posts"]:
        name = p["topic"]
        if Path(name).name != name or name not in public or name in seen:
            raise ValueError(f"Invalid/duplicate/unlisted topic: {name}")
        seen.add(name)
        url = urlsplit(p["url"])
        if (
            url.scheme != "https"
            or url.netloc != "jakeuj.com"
            or url.query
            or url.fragment
            or not url.path.endswith(".html")
            or ".." in unquote(url.path).split("/")
        ):
            raise ValueError(f"Invalid public URL: {p['url']}")
        if unquote(p["url"]) in urls:
            raise ValueError("Duplicate URL")
        urls.add(unquote(p["url"]))
        for key in ["published", "updated"]:
            if key in p:
                d = date.fromisoformat(p[key])
                if (
                    d.isoformat() != p[key]
                    or d > datetime.now(timezone(timedelta(hours=8))).date()
                ):
                    raise ValueError(f"Invalid {key}: {name}")
        if not p["date_basis"].strip():
            raise ValueError(f"Missing date basis: {name}")
        if ("updated" in p) != bool(p.get("update_summary")) or p.get(
            "updated", p["published"]
        ) < p["published"]:
            raise ValueError(f"Invalid major update: {name}")
        text = (topics / name).read_text()
        title = re.search(r"^# (.+)$", text, re.M)
        summary = re.search(r"<web-summary>(.*?)</web-summary>", text, re.S)
        p["title"] = plain(title[1]) if title else ""
        p["summary"] = plain(summary[1] if summary else p.get("summary", ""))
        if not p["title"] or not p["summary"]:
            raise ValueError(f"Missing title/summary: {name}")
    if (
        len(data["featured"]) != 3
        or len(set(data["featured"])) != 3
        or not set(data["featured"]) <= seen
    ):
        raise ValueError("Choose three distinct registered featured posts")
    for name, reason in data.get("excluded", {}).items():
        if (
            Path(name).name != name
            or name in seen
            or not reason.strip()
            or not (topics / name).is_file()
        ):
            raise ValueError(f"Invalid exclusion: {name}")
    data["posts"].sort(
        key=lambda p: (-date.fromisoformat(p["published"]).toordinal(), p["topic"])
    )
    return data


def md(value):
    return (
        html.escape(value, quote=False)
        .replace("[", r"\[")
        .replace("]", r"\]")
        .replace("*", r"\*")
        .replace("`", r"\`")
    )


def entries(posts):
    return "\n\n".join(
        f"- [{md(p['title'])}]({p['topic']}) — {p['published']}\n\n  {md(p['summary'])}"
        for p in posts
    )


def render(data):
    posts = data["posts"]
    by_topic = {p["topic"]: p for p in posts}
    home = (
        "## 最新文章\n\n"
        + entries(posts[:10])
        + "\n\n[查看所有近期文章](recent-posts.md)\n\n## 精選文章\n\n"
        + entries([by_topic[t] for t in data["featured"]])
    )
    home += "\n\n## 主題入口\n\n- [.NET／C#](C-Sharp.md)\n- [ABP](ABP.md)\n- [Azure](Azure.md)\n- [Docker](Docker.md)\n- [AI／LLM](LLM.md)\n- [macOS：開發環境設定](macOS_dotfiles_guide.md)"
    updates = sorted(
        [p for p in posts if p.get("updated")],
        key=lambda p: (-date.fromisoformat(p["updated"]).toordinal(), p["topic"]),
    )[:5]
    if updates:
        home += "\n\n## 重大更新\n\n" + "\n\n".join(
            f"- [{md(p['title'])}]({p['topic']}) — {p['updated']}\n\n  {md(p['update_summary'])}"
            for p in updates
        )
    recent = "# 最新文章\n\n<web-summary>依發布日期瀏覽 Jakeuj 的近期技術文章，涵蓋雲端、開發工具與實作排錯筆記。</web-summary>\n\n這裡收錄已整理發布日期的文章，尚未涵蓋全部歷史文章；其他筆記可從左側分類瀏覽。\n\n[訂閱新文章 RSS](https://jakeuj.com/feed.xml) · [返回首頁](Default.md)\n"
    years = sorted({p["published"][:4] for p in posts}, reverse=True)
    for year in years:
        yearly = [p for p in posts if p["published"].startswith(year)]
        # Bound sections for Algolia; preserve year grouping with numbered continuations.
        for i in range(0, len(yearly), 10):
            label = year if i == 0 else f"{year}（續 {i // 10}）"
            recent += (
                f"\n## {label} {{#year-{year}-{i // 10 + 1}}}\n\n"
                + entries(yearly[i : i + 10])
                + "\n"
            )
    return home + "\n", recent


def generate(root=ROOT, check=False):
    data = load(root)
    home, recent = render(data)
    path = root / "Writerside/topics/Default.md"
    current = path.read_text()
    if current.count(START) != 1 or current.count(END) != 1:
        raise ValueError("Homepage generation markers missing/duplicated")
    result = (
        current.split(START)[0]
        + START
        + "\n\n"
        + home
        + "\n"
        + END
        + current.split(END)[1]
    )
    for path, content in [
        (path, result),
        (root / "Writerside/topics/recent-posts.md", recent),
    ]:
        if check:
            if not path.exists() or path.read_text() != content:
                raise ValueError(
                    "Publication pages stale; run npm run publications:generate"
                )
        else:
            path.write_text(content)
    return data


class Head(HTMLParser):
    def __init__(self, text):
        super().__init__()
        self.canonicals = []
        self.og = []
        self.feeds = []
        self.feed_tags = []
        self.feed(text)

    def handle_starttag(self, tag, attrs):
        a = dict(attrs)
        if tag == "link" and a.get("rel") == "canonical":
            self.canonicals.append(a.get("href"))
        if tag == "meta" and a.get("property") == "og:url":
            self.og.append(a.get("content"))
        if tag == "link" and a.get("type") == "application/rss+xml":
            self.feeds.append(a.get("href"))
            self.feed_tags.append(self.get_starttag_text())


def rss(data):
    ET.register_namespace("atom", "http://www.w3.org/2005/Atom")
    root = ET.Element("rss", version="2.0")
    channel = ET.SubElement(root, "channel")
    for tag, value in [
        ("title", "Jakeuj 筆記本"),
        ("link", "https://jakeuj.com/default.html"),
        ("description", "Jakeuj 的最新技術文章"),
        ("language", "zh-TW"),
    ]:
        ET.SubElement(channel, tag).text = value
    ET.SubElement(
        channel,
        "{http://www.w3.org/2005/Atom}link",
        href=FEED,
        rel="self",
        type="application/rss+xml",
    )
    for p in data["posts"][:20]:
        item = ET.SubElement(channel, "item")
        for tag, value in [
            ("title", p["title"]),
            ("description", p["summary"]),
            ("link", p["url"]),
        ]:
            ET.SubElement(item, tag).text = value
        ET.SubElement(item, "guid", isPermaLink="true").text = p["url"]
        dt = datetime.combine(
            date.fromisoformat(p["published"]), time(), timezone(timedelta(hours=8))
        )
        ET.SubElement(item, "pubDate").text = format_datetime(dt)
    ET.indent(root)
    return ET.tostring(root, encoding="utf-8", xml_declaration=True)


def publish(data, site):
    site = site.resolve()
    # Validate everything before writing any artifact.
    patches = {}
    for p in data["posts"]:
        path = site / unquote(urlsplit(p["url"]).path).lstrip("/")
        text = path.read_text()
        head = Head(text)
        if head.canonicals and head.canonicals != [p["url"]]:
            raise ValueError(f"Canonical mismatch: {path}")
        if head.og != [p["url"]]:
            raise ValueError(f"Built URL mismatch: {path}")
        if not head.canonicals:
            text = text.replace(
                "</head>",
                f'<link rel="canonical" href="{html.escape(p["url"], quote=True)}"></head>',
                1,
            )
        if Head(text).canonicals != [p["url"]]:
            raise ValueError(f"Missing head: {path}")
        patches[path] = text
    for path in site.rglob("*.html"):
        text = patches.get(path, path.read_text())
        head = Head(text)
        if "</head>" not in text:
            continue
        for tag in head.feed_tags:
            text = text.replace(tag, "")
        text = text.replace(
            "</head>",
            f'<link rel="alternate" type="application/rss+xml" title="Jakeuj 筆記本 RSS" href="{FEED}"></head>',
            1,
        )
        patches[path] = text
    for path, text in patches.items():
        path.write_text(text)
    (site / "feed.xml").write_bytes(rss(data))


def check_new_topics(data):
    """Grandfather existing notes; require registration for additions after rollout."""
    baseline = data["registration_baseline"]
    if not re.fullmatch(r"[0-9a-f]{40}", baseline):
        raise ValueError("Invalid registration baseline commit")
    commands = [
        [
            "git",
            "diff",
            "--name-only",
            "--diff-filter=A",
            "-z",
            baseline,
            "--",
            "Writerside/topics/*.md",
        ],
        [
            "git",
            "ls-files",
            "--others",
            "--exclude-standard",
            "-z",
            "--",
            "Writerside/topics/*.md",
        ],
    ]
    names = set()
    for command in commands:
        result = subprocess.run(
            command, cwd=ROOT, capture_output=True, text=True, check=True
        )
        names.update(Path(f).name for f in result.stdout.split("\0") if f)
    registered = {p["topic"] for p in data["posts"]} | set(data.get("excluded", {}))
    missing = names - registered
    if missing:
        raise ValueError(
            "Register new topics or explain exclusion in data/posts.json: "
            + ", ".join(sorted(missing))
        )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("command", choices=["generate", "check", "publish"])
    parser.add_argument("--site", type=Path)
    args = parser.parse_args()
    try:
        data = generate(check=args.command != "generate")
        if args.command == "check":
            check_new_topics(data)
        if args.command == "publish":
            if not args.site:
                parser.error("--site is required")
            publish(data, args.site)
    except (
        ValueError,
        KeyError,
        OSError,
        ET.ParseError,
        subprocess.CalledProcessError,
    ) as e:
        print(f"Publication check failed: {e}", file=sys.stderr)
        return 1
    print(f"Publication {args.command}: OK ({len(data['posts'])} posts)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
