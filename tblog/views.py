from django.db.models import Q
from django.views import generic
from .models import Post
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
        if not context["is_top_page"]:
            return context

        public_posts = Post.objects.filter(is_publick=True).exclude(category__name="PaidContent")
        context["series_guides"] = [
            {
                "label": "暗号技術",
                "summary": "古典暗号から多表式暗号まで、暗号の仕組みを図解と具体例で順番に整理しています。",
                "posts": public_posts.filter(title__icontains="暗号技術").order_by("pk")[:6],
            },
            {
                "label": "Python / AI 基礎",
                "summary": "AIの基本的な考え方や、Pythonで扱うための前提知識を整理します。",
                "posts": public_posts.filter(Q(title__icontains="Python - AI")).order_by("pk")[:5],
            },
            {
                "label": "Python / 機械学習",
                "summary": "教師あり学習、分類、回帰など、機械学習の基本的な考え方をPythonの文脈で整理します。",
                "posts": public_posts.filter(
                    Q(title__icontains="Python - 機械学習")
                    | Q(title__icontains="Python - Machine Learning")
                ).order_by("pk")[:5],
            },
            {
                "label": "Python / ニューラルネットワーク",
                "summary": "ニューラルネットワークや深層学習の仕組みを、基礎から順番に整理します。",
                "posts": public_posts.filter(
                    Q(title__icontains="Python - ニューラルネットワーク")
                    | Q(title__icontains="Python - Neural Networks")
                ).order_by("pk")[:5],
            },
            {
                "label": "応用情報技術者試験",
                "summary": "試験対策で押さえたい用語や考え方を、あとから見返しやすい形でまとめます。",
                "posts": public_posts.filter(title__icontains="応用情報技術").order_by("pk")[:5],
            },
        ]
        return context

class CategoryView(BaseListView):
    def get_queryset(self):
        queryset = self.base_queryset()
        category = self.kwargs.get("small")
        if category:
            queryset = queryset.filter(category__name=category)
        else:
            category = self.kwargs.get("big")
            queryset = queryset.filter(category__parent__name=category)
        logging.getLogger('command').debug('ON View.py > CategoryView')
        return queryset

class TagView(BaseListView):
    def get_queryset(self):
        tag = self.kwargs["tag"]
        queryset = self.base_queryset().filter(tag__name=tag)
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
