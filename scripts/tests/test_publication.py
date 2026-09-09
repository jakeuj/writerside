import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace
import xml.etree.ElementTree as ET

spec = importlib.util.spec_from_file_location(
    "publication", Path(__file__).parents[1] / "publication.py"
)
p = importlib.util.module_from_spec(spec)
spec.loader.exec_module(p)


class PublicationTests(unittest.TestCase):
    def setUp(self):
        self.data = copy.deepcopy(p.load())

    def test_rss_dates_escaping_limit_and_updates(self):
        data = self.data
        data["posts"][0]["title"] = "中文 & <RSS>"
        data["posts"][0]["summary"] = "A & B < C"
        before = p.rss(data)
        data["posts"][0].update(updated="2026-09-01", update_summary="重大更新")
        self.assertEqual(before, p.rss(data))
        root = ET.fromstring(before)
        items = root.findall("channel/item")
        self.assertEqual(len(items), 20)
        self.assertEqual(items[0].findtext("title"), "中文 & <RSS>")
        self.assertTrue(items[0].findtext("pubDate").endswith("00:00:00 +0800"))
        self.assertEqual(items[0].findtext("guid"), data["posts"][0]["url"])
        self.assertIn("重大更新", p.render(data)[0])
        self.assertNotIn("## 重大更新", p.render(p.load())[0])

    def test_new_post_enters_feed_and_oldest_leaves(self):
        data = self.data
        new = copy.deepcopy(data["posts"][0])
        new.update(
            topic="new.md", url="https://jakeuj.com/new.html", published="2026-09-09"
        )
        data["posts"].insert(0, new)
        items = ET.fromstring(p.rss(data)).findall("channel/item")
        self.assertEqual(len(items), 20)
        self.assertEqual(items[0].findtext("link"), new["url"])
        self.assertNotIn(data["posts"][-1]["url"], [i.findtext("link") for i in items])

    def test_site_validation_and_idempotence(self):
        with tempfile.TemporaryDirectory() as tmp:
            site = Path(tmp)
            for post in self.data["posts"]:
                name = p.urlsplit(post["url"]).path.lstrip("/")
                (site / name).write_text(
                    f'<html><head><meta property="og:url" content="{post["url"]}"></head><body></body></html>'
                )
            p.publish(self.data, site)
            files = {f.name: f.read_bytes() for f in site.iterdir()}
            p.publish(self.data, site)
            self.assertEqual(files, {f.name: f.read_bytes() for f in site.iterdir()})
            first = self.data["posts"][0]
            page = site / p.urlsplit(first["url"]).path.lstrip("/")
            head = p.Head(page.read_text())
            self.assertEqual(head.canonicals, [first["url"]])
            self.assertEqual(head.feeds, [p.FEED])
            page.write_text(
                page.read_text().replace(
                    'rel="canonical" href="https://jakeuj.com/',
                    'rel="canonical" href="https://wrong.example/',
                )
            )
            with self.assertRaises(ValueError):
                p.publish(self.data, site)
            page.unlink()
            with self.assertRaises(FileNotFoundError):
                p.publish(self.data, site)

    def test_registry_invalid_metadata_and_sorting(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "data").mkdir()
            (root / "Writerside").mkdir()
            (root / "Writerside/topics").symlink_to(
                p.ROOT / "Writerside/topics", target_is_directory=True
            )
            (root / "Writerside/hi.tree").symlink_to(p.ROOT / "Writerside/hi.tree")
            original = json.loads((p.ROOT / "data/posts.json").read_text())
            path = root / "data/posts.json"
            for field, value in [
                ("published", "2026-02-30"),
                ("url", original["posts"][1]["url"]),
                ("topic", "missing.md"),
                ("date_basis", ""),
                ("updated", "2020-01-01"),
            ]:
                data = copy.deepcopy(original)
                data["posts"][0][field] = value
                path.write_text(json.dumps(data))
                with self.assertRaises((ValueError, FileNotFoundError)):
                    p.load(root)
            data = copy.deepcopy(original)
            data["posts"].reverse()
            path.write_text(json.dumps(data))
            self.assertEqual(
                [x["topic"] for x in p.load(root)["posts"]],
                [x["topic"] for x in self.data["posts"]],
            )
            data = copy.deepcopy(original)
            target = next(
                x
                for x in data["posts"]
                if x["topic"] == "macos-mdns-ssh-hostname-resolution.md"
            )
            target.pop("summary")
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                p.load(root)

    def test_new_topics_require_registration_or_exclusion(self):
        with patch.object(
            p.subprocess,
            "run",
            return_value=SimpleNamespace(stdout="Writerside/topics/new.md\0"),
        ):
            with self.assertRaises(ValueError):
                p.check_new_topics(self.data)
            self.data["excluded"]["new.md"] = "分類入口"
            p.check_new_topics(self.data)

    def test_stale_page_is_rejected(self):
        original = Path.read_text

        def read(path, *args, **kwargs):
            text = original(path, *args, **kwargs)
            if path.name == "recent-posts.md":
                return text + "\n舊資料\n"
            return text

        with patch.object(Path, "read_text", read):
            with self.assertRaisesRegex(ValueError, "stale"):
                p.generate(check=True)

    def test_generated_pages_current_and_bounded(self):
        p.generate(check=True)
        _, recent = p.render(self.data)
        for section in recent.split("\n## "):
            self.assertLess(len(section.encode()), 8000)


if __name__ == "__main__":
    unittest.main()
