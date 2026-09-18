"""Public URLs shared by the HTML and XML sitemaps."""

from types import SimpleNamespace
from urllib.parse import urlsplit

from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import get_public_posts


CANONICAL_ORIGIN = "https://sigma-se.com"
STATIC_PAGES = (
    ("tblog:index", "トップ"),
    ("tblog:sitemap", "サイトマップ"),
    ("tblog:profile", "プロフィール"),
    ("tblog:contact", "お問い合わせ"),
    ("tblog:ppolicy", "プライバシーポリシー"),
)


class CanonicalSitemap(Sitemap):
    protocol = "https"

    def get_urls(self, page=1, site=None, protocol=None):
        # Match article canonicals even behind an HTTP proxy or on the www host.
        canonical_site = SimpleNamespace(domain=urlsplit(CANONICAL_ORIGIN).netloc)
        return super().get_urls(page=page, site=canonical_site, protocol=self.protocol)


class PostSitemap(CanonicalSitemap):
    def items(self):
        return get_public_posts().only("id", "updated_at").order_by("pk")

    def location(self, post):
        return reverse("tblog:detail", kwargs={"pk": post.pk})

    def lastmod(self, post):
        return post.updated_at


class StaticPageSitemap(CanonicalSitemap):
    def items(self):
        return [name for name, label in STATIC_PAGES]

    def location(self, name):
        return reverse(name)

    # Static pages have no tracked content-modification date; omit lastmod.
