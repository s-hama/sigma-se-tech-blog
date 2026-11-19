"""Dark-mode integration and SVG fidelity checks (no browser dependency)."""

import re
import xml.etree.ElementTree as ET

from django.test import SimpleTestCase, TestCase

from .models import BigCategory, Post, SmallCategory
from .svg_dm import IMAGE_DIR, PAINT_DECLARATION, SOURCE_NAME, render_dark


class DarkSvgTests(SimpleTestCase):
    def test_all_variants_are_current_and_preserve_content_and_geometry(self):
        sources = [p for p in IMAGE_DIR.iterdir() if SOURCE_NAME.fullmatch(p.name)]
        self.assertTrue(sources)
        paint = {"fill", "stroke", "color", "stop-color", "flood-color", "lighting-color"}
        allowed = {
            "#ffffff", "#f8f9fa", "#e9ecef", "#dee2e6", "#ced4da", "#adb5bd",
            "#6c757d", "#495057", "#343a40", "#212529",
            "none", "transparent", "currentColor", "inherit",
        }
        for source in sources:
            with self.subTest(svg=source.name):
                original = source.read_text()
                dark = source.with_stem(source.stem + "_dm").read_text()
                self.assertEqual(dark, render_dark(original), "Regenerate with python3 -m tblog.svg_dm")
                light_nodes = list(ET.fromstring(original).iter())
                dark_nodes = list(ET.fromstring(dark).iter())
                self.assertEqual(len(light_nodes), len(dark_nodes))
                for before, after in zip(light_nodes, dark_nodes):
                    self.assertEqual(before.tag, after.tag)
                    self.assertEqual(before.tail, after.tail)
                    self.assertEqual(
                        PAINT_DECLARATION.sub(r"\1:\2", before.text or ""),
                        PAINT_DECLARATION.sub(r"\1:\2", after.text or ""),
                    )
                    for value in (v for k, v in after.attrib.items() if k in paint):
                        self.assertIn(value, allowed)
                    def geometry(node):
                        return {
                            k: PAINT_DECLARATION.sub(r"\1:\2", v) if k == "style" else v
                            for k, v in node.attrib.items() if k not in paint
                        }
                    self.assertEqual(geometry(before), geometry(after))

    def test_white_labels_remain_distinct_from_filled_bands(self):
        source = '<svg xmlns="http://www.w3.org/2000/svg"><rect fill="#495057"/><text fill="#fff">A</text></svg>'
        result = ET.fromstring(render_dark(source))
        self.assertEqual(result[0].get("fill"), "#ffffff")
        self.assertEqual(result[1].get("fill"), "#212529")

    def test_unknown_color_requires_review(self):
        with self.assertRaisesRegex(ValueError, "Unmapped SVG color"):
            render_dark('<svg xmlns="http://www.w3.org/2000/svg"><path stroke="red"/></svg>')


class DarkThemeTemplateTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        big = BigCategory.objects.create(name="数学")
        small = SmallCategory.objects.create(name="図形", parent=big)
        cls.post = Post.objects.create(title="テーマ確認", text="本文", category=small)

    def test_public_pages_share_one_toggle_and_early_theme_script(self):
        for path in ("/", "/?page=1", "/?quick=テーマ", f"/detail/{self.post.pk}/", "/profile/", "/contact/", "/ppolicy/", "/sitemap/", "/category/数学/図形/"):
            with self.subTest(path=path):
                response = self.client.get(path)
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, 'data-bs-theme="light"', count=1)
                self.assertContains(response, 'id="theme-toggle-dm"', count=1)
                html = response.content.decode()
                script = re.search(r'<script[^>]+theme_dm\.js[^>]*>', html)[0]
                self.assertNotIn("defer", script)
                self.assertNotIn("async", script)
                self.assertLess(html.index(script), html.index("bootstrap@5.3.0/dist/css"))
                self.assertLess(html.index("tblog/custom.css"), html.index("tblog/custom_dm.css"))
