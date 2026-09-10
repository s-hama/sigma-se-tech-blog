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
