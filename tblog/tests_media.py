"""Keep the article image scrolling script connected to detail pages."""

from django.conf import settings
from django.test import TestCase

from .models import BigCategory, Post, SmallCategory


class PostMediaTests(TestCase):
    def test_article_loads_the_available_media_script_once_with_defer(self):
        big = BigCategory.objects.create(name="情報技術")
        small = SmallCategory.objects.create(name="基礎", parent=big)
        post = Post.objects.create(title="画像表示", text="本文", category=small)

        response = self.client.get(f"/detail/{post.pk}/")

        self.assertEqual(response.status_code, 200)
        self.assertContains(
            response,
            '<script src="/static/tblog/post_media.js" defer></script>',
            count=1,
        )
        self.assertTrue((settings.BASE_DIR / "static/tblog/post_media.js").is_file())
