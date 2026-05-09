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
                "label": "暗号技術の歴史と仕組み",
                "summary": "古典暗号から多表式暗号まで、暗号の仕組みを図解と具体例で順番に解説",
                "posts": public_posts.filter(title__icontains="情報セキュリティ - 暗号技術").order_by("pk")[:10],
            },
            {
                "label": "Angular - システム開発の基礎",
                "summary": "Angularの導入から基本構成まで、Webシステム開発の基礎を解説",
                "posts": public_posts.filter(
                    Q(title__icontains="Webシステム開発 - Angular入門")
                ).order_by("pk")[:10],
            },
            {
                "label": "Python - 基礎",
                "summary": "Pythonの開発環境、基本文法、標準機能、数値計算や可視化の基礎を整理",
                "posts": public_posts.filter(
                    Q(title__icontains="Python - 開発向けVim設定")
                    | Q(title__icontains="Python - 対話モード")
                    | Q(title__icontains="Python - 標準デバッガー（Pdb）")
                    | Q(title__icontains="Python - NumPy")
                    | Q(title__icontains="Python - Matplotlib")
                    | Q(title__icontains="Python - 組込みデータ型")
                    | Q(title__icontains="Python - 算術演算子まとめ")
                    | Q(title__icontains="Python - 複合代入演算子まとめ")
                    | Q(title__icontains="Python - 論理演算子まとめ")
                    | Q(title__icontains="Python - ビット演算子まとめ")
                    | Q(title__icontains="Python - 高階関数と畳込み")
                    | Q(title__icontains="Python - 例外")
                ).order_by("pk")[:30],
            },
            {
                "label": "Python - タスク指向型対話",
                "summary": "タスク指向型対話システムの考え方や構成要素をPythonを用いて解説",
                "posts": public_posts.filter(
                    Q(title__icontains="Python - タスク指向型対話")
                ).order_by("pk")[:5],
            },
            {
                "label": "Python - ニューラルネットワーク",
                "summary": "ニューラルネットワークや深層学習の仕組みをPythonを用いて基礎から順番に解説",
                "posts": public_posts.filter(
                    Q(title__icontains="Python - ニューラルネットワーク")
                ).order_by("pk")[:15],
            },
            {
                "label": "Django - 基本操作",
                "summary": "Django開発で使う基本操作やデバッグ支援ツールを整理",
                "posts": public_posts.filter(
                    Q(title__icontains="Django - Django Debug Toolbar")
                ).order_by("pk")[:5],
            },
            {
                "label": "Django - VPSで作るDjangoサイト",
                "summary": "VPS上でDjangoサイトを構築し、公開するまでの手順を解説",
                "posts": public_posts.filter(title__icontains="VPSで作るDjangoサイト構築手順 - ").order_by("pk")[:5],
            },
            {
                "label": "応用情報技術",
                "summary": "試験対策で押さえたい用語や考え方を、あとから見返しやすい形で整理",
                "posts": public_posts.filter(title__icontains="応用情報技術 - ").order_by("pk")[:25],
            },
            {
                "label": "Git - 基本操作",
                "summary": "Gitの開発準備や状態管理の考え方、基本操作を整理",
                "posts": public_posts.filter(
                    Q(title__icontains="Git - 開発準備")
                    | Q(title__icontains="Git - 状態管理の概念と基本操作")
                ).order_by("pk")[:5],
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
