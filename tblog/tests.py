from datetime import datetime, timezone
from html.parser import HTMLParser
from unittest.mock import patch
from urllib.parse import urlsplit
from xml.etree import ElementTree

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import BigCategory, Post, SmallCategory, Tag


class ListPageTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.big_category = BigCategory.objects.create(name="数学")
        cls.small_category = SmallCategory.objects.create(
            name="計算の仕組み",
            parent=cls.big_category,
        )
        cls.post = Post.objects.create(
            title="除算の仕組み",
            text="本文",
            category=cls.small_category,
            is_publick=True,
        )
        cls.used_tag = Tag.objects.create(name="除算")
        cls.unused_tag = Tag.objects.create(name="未使用")
        cls.private_only_tag = Tag.objects.create(name="非公開記事のみ")
        cls.post.tag.add(cls.used_tag)

        private_post = Post.objects.create(
            title="非公開記事",
            text="本文",
            category=cls.small_category,
            is_publick=False,
        )
        private_post.tag.add(cls.private_only_tag)

    def test_unknown_big_category_returns_404(self):
        response = self.client.get(
            reverse("tblog:category", kwargs={"big": "存在しないカテゴリ"})
        )

        self.assertEqual(response.status_code, 404)

    def test_existing_category_is_displayed(self):
        response = self.client.get(
            reverse(
                "tblog:category",
                kwargs={
                    "big": self.big_category.name,
                    "small": self.small_category.name,
                },
            )
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_unknown_small_category_returns_404(self):
        response = self.client.get(
            reverse(
                "tblog:category",
                kwargs={"big": self.big_category.name, "small": "存在しないカテゴリ"},
            )
        )

        self.assertEqual(response.status_code, 404)

    def test_unknown_tag_returns_404(self):
        response = self.client.get(
            reverse("tblog:tag", kwargs={"tag": "存在しないタグ"})
        )

        self.assertEqual(response.status_code, 404)

    def test_existing_tag_is_displayed(self):
        response = self.client.get(
            reverse("tblog:tag", kwargs={"tag": self.used_tag.name})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_search_with_no_results_is_noindex(self):
        response = self.client.get(reverse("tblog:index"), {"quick": "該当なし"})

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<meta name="robots" content="noindex,follow">',
            html=True,
        )
        self.assertContains(response, "該当する記事がありません。")
        self.assertNotContains(response, 'aria-label="Page navigation"')

    def test_search_with_results_is_indexable(self):
        response = self.client.get(reverse("tblog:index"), {"quick": "除算"})

        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "noindex,follow")

    def test_sidebar_hides_unused_tags_and_shows_all_used_tags(self):
        additional_tags = []
        for index in range(25):
            tag = Tag.objects.create(name=f"使用中{index:02d}")
            self.post.tag.add(tag)
            additional_tags.append(tag)

        response = self.client.get(reverse("tblog:index"))
        sidebar_tags = list(response.context["tags"])

        self.assertEqual(len(sidebar_tags), len(additional_tags) + 1)
        self.assertIn(self.used_tag, sidebar_tags)
        for tag in additional_tags:
            self.assertIn(tag, sidebar_tags)
        self.assertNotIn(self.unused_tag, sidebar_tags)
        self.assertNotIn(self.private_only_tag, sidebar_tags)


class LinkParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        if tag == "a":
            self.links.append(dict(attrs).get("href", ""))


class SitemapTest(TestCase):
    namespace = {"sm": "http://www.sitemaps.org/schemas/sitemap/0.9"}
    static_paths = {"/", "/sitemap/", "/profile/", "/contact/", "/ppolicy/"}

    @classmethod
    def setUpTestData(cls):
        cls.big = BigCategory.objects.create(name="情報技術")
        cls.small = SmallCategory.objects.create(name="暗号技術", parent=cls.big)
        # Create out of sequence, and exceed the home page's ten-article limit.
        cls.series_posts = {
            number: Post.objects.create(
                title=f"情報セキュリティ - 暗号技術：{number}/12 解説",
                text="公開本文",
                category=cls.small,
            )
            for number in (10, 2, 1, 12, 3, 11, 4, 5, 6, 7, 8, 9)
        }
        cls.standalone = Post.objects.create(
            title="未登録テーマの解説 & <サンプル>", text="公開本文", category=cls.small,
        )
        cls.other_big = BigCategory.objects.create(name="数学")
        cls.other_small = SmallCategory.objects.create(name="計算の仕組み", parent=cls.other_big)
        cls.other_post = Post.objects.create(
            title="数学 - 計算の仕組み：負の数", text="公開本文", category=cls.other_small,
        )
        cls.draft = Post.objects.create(
            title="非公開の下書き", text="非公開本文", category=cls.small, is_publick=False,
        )
        paid_category = SmallCategory.objects.create(name="PaidContent", parent=cls.big)
        cls.paid = Post.objects.create(
            title="ログイン必須記事", text="限定本文", category=paid_category,
        )
        cls.public_posts = list(cls.series_posts.values()) + [cls.standalone, cls.other_post]
        cls.public_paths = {
            reverse("tblog:detail", kwargs={"pk": post.pk}) for post in cls.public_posts
        }
        cls.updated_at = datetime(2025, 1, 10, 3, 0, tzinfo=timezone.utc)
        Post.objects.update(updated_at=cls.updated_at)

    def xml_entries(self, **request_kwargs):
        response = self.client.get(reverse("tblog:sitemap_xml"), **request_kwargs)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("application/xml"))
        root = ElementTree.fromstring(response.content)
        self.assertEqual(root.tag, "{http://www.sitemaps.org/schemas/sitemap/0.9}urlset")
        entries = root.findall("sm:url", self.namespace)
        urls = [entry.findtext("sm:loc", namespaces=self.namespace) for entry in entries]
        self.assertEqual(len(urls), len(set(urls)))
        return dict(zip(urls, entries))

    def test_html_lists_every_public_article_once_without_series_limit(self):
        response = self.client.get(reverse("tblog:sitemap"))
        self.assertEqual(response.status_code, 200)
        parser = LinkParser()
        parser.feed(response.content.decode())
        article_links = [href for href in parser.links if href.startswith("/detail/")]
        self.assertCountEqual(article_links, self.public_paths)
        self.assertEqual(response.context["sitemap_post_count"], len(self.public_paths))
        self.assertContains(response, "未登録テーマの解説 &amp; &lt;サンプル&gt;")
        self.assertNotContains(response, self.draft.title)
        self.assertNotContains(response, self.paid.title)

    def test_html_groups_by_category_and_orders_series_numerically(self):
        response = self.client.get(reverse("tblog:sitemap"))
        parents = response.context["sitemap_categories"]
        parent = next(group for group in parents if group["category"].pk == self.big.pk)
        self.assertEqual(len(parent["children"]), 1)
        child = parent["children"][0]
        self.assertEqual(child["category"], self.small)
        self.assertEqual(child["series"][0]["posts"], [self.series_posts[i] for i in range(1, 13)])
        self.assertEqual(child["series"][1]["posts"], [self.standalone])

    def test_html_omits_site_guide_and_is_accessible_from_menu_and_footer(self):
        response = self.client.get(reverse("tblog:sitemap"))
        self.assertNotContains(response, "サイトのご案内")
        self.assertNotContains(response, "sitemap-pages")
        parser = LinkParser()
        parser.feed(response.content.decode())
        self.assertTrue(self.static_paths.issubset(set(parser.links)))
        for page in ("tblog:index", "tblog:profile", "tblog:contact", "tblog:ppolicy"):
            response = self.client.get(reverse(page))
            self.assertContains(response, 'href="/sitemap/"', count=2)

    def test_html_does_not_load_ads_but_articles_still_do(self):
        script_url = "https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js"
        response = self.client.get(reverse("tblog:sitemap"))
        self.assertNotContains(response, script_url)
        self.assertContains(response, '<link rel="canonical" href="https://sigma-se.com/sitemap/">', html=True)
        response = self.client.get(reverse("tblog:detail", kwargs={"pk": self.standalone.pk}))
        self.assertContains(response, script_url)

    def test_xml_only_lists_public_articles_and_fixed_canonical_urls(self):
        entries = self.xml_entries()
        expected = {"https://sigma-se.com" + path for path in self.static_paths | self.public_paths}
        self.assertEqual(set(entries), expected)

    def test_xml_uses_canonical_host_and_https_for_alternate_host_requests(self):
        entries = self.xml_entries(HTTP_HOST="www.sigma-se.com")
        self.assertTrue(all(url.startswith("https://sigma-se.com/") for url in entries))

    def test_xml_links_resolve_to_public_pages(self):
        for url in self.xml_entries():
            with self.subTest(url=url):
                response = self.client.get(urlsplit(url).path)
                self.assertEqual(response.status_code, 200)

    def test_xml_tracks_article_updates_without_inventing_static_page_dates(self):
        entries = self.xml_entries()
        for url, entry in entries.items():
            lastmod = entry.findtext("sm:lastmod", namespaces=self.namespace)
            expected = "2025-01-10" if urlsplit(url).path in self.public_paths else None
            self.assertEqual(lastmod, expected)
        changed_at = datetime(2025, 2, 20, 3, 0, tzinfo=timezone.utc)
        with patch("django.db.models.fields.timezone.now", return_value=changed_at):
            self.standalone.text = "説明を加筆した本文"
            self.standalone.save()
        updated_entries = self.xml_entries()
        for post in self.public_posts:
            url = "https://sigma-se.com" + reverse("tblog:detail", kwargs={"pk": post.pk})
            expected = "2025-02-20" if post.pk == self.standalone.pk else "2025-01-10"
            self.assertEqual(updated_entries[url].findtext("sm:lastmod", namespaces=self.namespace), expected)

    def test_authenticated_requests_do_not_expose_restricted_articles(self):
        user = get_user_model().objects.create_user(username="sitemap-reader", password="test-password")
        self.client.force_login(user)
        entries = self.xml_entries()
        self.assertEqual({urlsplit(url).path for url in entries}, self.static_paths | self.public_paths)
        response = self.client.get(reverse("tblog:sitemap"))
        self.assertNotContains(response, self.paid.title)
        self.assertNotContains(response, self.draft.title)

    def test_new_and_unpublished_articles_are_reflected_automatically(self):
        added = Post.objects.create(title="追加記事", text="本文", category=self.small)
        added_path = reverse("tblog:detail", kwargs={"pk": added.pk})
        self.assertIn("https://sigma-se.com" + added_path, self.xml_entries())
        self.assertContains(self.client.get(reverse("tblog:sitemap")), f'href="{added_path}"')
        added.is_publick = False
        added.save()
        self.assertNotIn("https://sigma-se.com" + added_path, self.xml_entries())
        self.assertNotContains(self.client.get(reverse("tblog:sitemap")), f'href="{added_path}"')

    def test_empty_site_keeps_fixed_pages_and_valid_xml(self):
        Post.objects.all().delete()
        response = self.client.get(reverse("tblog:sitemap"))
        self.assertContains(response, "公開記事はまだありません。")
        self.assertEqual(response.context["sitemap_categories"], [])
        self.assertEqual({urlsplit(url).path for url in self.xml_entries()}, self.static_paths)

    def test_robots_advertises_xml_sitemap_and_allows_public_pages(self):
        response = self.client.get(reverse("tblog:robots"))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response["Content-Type"].startswith("text/plain"))
        self.assertEqual(response.content.decode(),
                         "User-agent: *\nDisallow: /admin/\n\nSitemap: https://sigma-se.com/sitemap.xml\n")

    def test_home_keeps_existing_series_limit_and_server_order(self):
        for server in ("Apache", "Nginx"):
            Post.objects.create(
                title=f"VPSで作るDjangoサイト構築手順 - {server}編：1/4 初期設定",
                text="本文", category=self.small,
            )
        response = self.client.get(reverse("tblog:index"))
        guides = {guide["label"]: guide["posts"] for guide in response.context["series_guides"]}
        self.assertEqual(len(guides["暗号技術の仕組み"]), 10)
        self.assertIn("Nginx編", guides["Django - VPSで作るDjangoサイト"][0].title)
        self.assertContains(response, "新着記事を見る")
