from django.db.models import Q
from django.http import Http404, HttpResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views import generic
from .models import BigCategory, Post, SmallCategory, Tag, get_public_posts
from .series import (
    ANGULAR_SERIES_PREFIX, VPS_SERIES_PREFIX,
    group_posts_by_series, group_vps_posts, order_series_posts,
)
from .sitemaps import CANONICAL_ORIGIN
import logging


class BaseListView(generic.ListView):
    paginate_by = 10 
    def base_queryset(self):
        queryset = Post.objects.filter(
            is_publick=True).order_by('-created_at')
        logging.getLogger('command').debug('ON View.py > BaseListView')
        return queryset

class PostIndexView(BaseListView):
    def get_queryset(self):
        if self.is_top_page():
            return Post.objects.none()

        queryset = self.base_queryset()
        keyword = self.request.GET.get("quick")
        if keyword:
            queryset = queryset.filter(
                Q(title__icontains=keyword) | Q(text__icontains=keyword))
        logging.getLogger('command').debug('ON View.py > PostIndexView')

        # Log the contents of queryset
        queryset_list = list(queryset.values())  # Convert QuerySet to list of dictionaries
        logging.getLogger('command').debug(f'QuerySet contents: {queryset_list}')

        return queryset

    def is_top_page(self):
        return not self.request.GET

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["is_top_page"] = self.is_top_page()
        context["is_search_no_results"] = (
            "quick" in self.request.GET and not context["post_list"]
        )
        if not context["is_top_page"]:
            return context

        public_posts = get_public_posts()
        context["latest_posts"] = public_posts.only("id", "title", "created_at").order_by(
            "-created_at", "-pk",
        )[:5]
        context["math_posts"] = public_posts.filter(
            category__parent__name="数理科学",
        ).only("id", "title").order_by("pk")
        context["vps_series"] = group_vps_posts(
            public_posts.filter(title__icontains=VPS_SERIES_PREFIX).only("id", "title"),
        )
        context["angular_posts"] = order_series_posts(
            public_posts.filter(title__icontains=ANGULAR_SERIES_PREFIX).only("id", "title"),
        )
        return context


class SitemapView(generic.TemplateView):
    template_name = "tblog/sitemap.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        posts = get_public_posts().select_related("category__parent").defer("text").order_by(
            "-category__parent_id", "category_id", "pk",
        )
        categories = {}
        post_count = 0
        for post in posts:
            category = post.category
            parent = categories.setdefault(category.parent_id, {
                "category": category.parent,
                "children": {},
            })
            child = parent["children"].setdefault(category.pk, {
                "category": category,
                "posts": [],
            })
            child["posts"].append(post)
            post_count += 1

        for parent in categories.values():
            for child in parent["children"].values():
                child["series"] = group_posts_by_series(child.pop("posts"))
            parent["children"] = list(parent["children"].values())

        context.update({
            "sitemap_categories": list(categories.values()),
            "sitemap_post_count": post_count,
            "canonical_url": CANONICAL_ORIGIN + reverse("tblog:sitemap"),
        })
        return context


def robots_txt(request):
    sitemap_url = CANONICAL_ORIGIN + reverse("tblog:sitemap_xml")
    return HttpResponse(
        f"User-agent: *\nDisallow: /admin/\n\nSitemap: {sitemap_url}\n",
        content_type="text/plain; charset=utf-8",
    )


class CategoryView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        big_name = self.kwargs["big"]
        small_name = self.kwargs.get("small")
        if small_name:
            category = get_object_or_404(
                SmallCategory,
                parent__name=big_name,
                name=small_name,
            )
            queryset = queryset.filter(category=category)
        else:
            category = get_object_or_404(BigCategory, name=big_name)
            queryset = queryset.filter(category__parent=category)
        logging.getLogger('command').debug('ON View.py > CategoryView')
        return queryset

class TagView(BaseListView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, name=self.kwargs["tag"])
        queryset = self.base_queryset().filter(tag=tag)
        logging.getLogger('command').debug('ON View.py > TagView')
        return queryset

class ProfileView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class ContactView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class PpolicyView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        return queryset

class PostDetailView(generic.DetailView):
    model = Post
    def get_object(self, queryset=None):
        post = super().get_object()
        if str(post.category) not in str("PaidContent") and post.is_publick:
            return post
        elif str(post.category) in str("PaidContent") and post.is_publick and self.request.user.is_authenticated:
            return post
        else:
            raise Http404
