"""Shared theme definitions for the home page and the complete article directory."""

import re


SERIES_GUIDES = (
    {
        "label": '数学 - 計算の仕組み',
        "summary": '分数の除算や負の数、0で割れない理由など、計算規則の仕組みを具体例と数式で解説',
        "keywords": (
            '数学 - 計算の仕組み',
        ),
        "limit": 10,
    },
    {
        "label": 'Django - VPSで作るDjangoサイト',
        "summary": 'VPS上でDjangoサイトを構築し、公開するまでの手順を解説',
        "keywords": (
            'VPSで作るDjangoサイト構築手順 - Nginx編',
            'VPSで作るDjangoサイト構築手順 - Apache編',
        ),
        "limit": 10,
        "keyword_order": True,
    },
    {
        "label": '暗号技術の仕組み',
        "summary": '古典暗号から耐量子暗号まで、暗号の考え方を図解と具体例で解説',
        "keywords": (
            '情報セキュリティ - 暗号技術',
        ),
        "limit": 10,
    },
    {
        "label": 'Angular - システム開発の基礎',
        "summary": 'Angularの導入から基本構成まで、Webシステム開発の基礎を解説',
        "keywords": (
            'Webシステム開発 - Angular基礎',
        ),
        "limit": 10,
    },
    {
        "label": 'Python - 基礎',
        "summary": 'Pythonの開発環境、基本文法、標準機能、数値計算や可視化の基礎を整理',
        "keywords": (
            'Python - 例外',
            'Python - 高階関数と畳込み',
            'Python - ビット演算子',
            'Python - 論理演算子',
            'Python - 複合代入演算子',
            'Python - 算術演算子',
            'Python - 組込みデータ型',
            'Python - Matplotlib',
            'Python - NumPy',
            'Python - 標準デバッガー（Pdb）',
            'Python - 開発向けVim設定',
            'Python - 対話モード',
        ),
        "limit": 30,
    },
    {
        "label": 'Python - タスク指向型対話',
        "summary": 'タスク指向型対話システムの考え方や構成要素をPythonを用いて解説',
        "keywords": (
            'Python - タスク指向型対話',
        ),
        "limit": 5,
    },
    {
        "label": 'Python - ニューラルネットワーク',
        "summary": 'ニューラルネットワークや深層学習の仕組みをPythonを用いて基礎から順番に解説',
        "keywords": (
            'Python - ニューラルネットワーク',
        ),
        "limit": 15,
    },
    {
        "label": 'Django - 基本操作',
        "summary": 'Django開発で使う基本操作やデバッグ支援ツールを整理',
        "keywords": (
            'Django - Django Debug Toolbar',
        ),
        "limit": 5,
    },
    {
        "label": '応用情報技術 - 基礎',
        "summary": '試験対策で押さえたい用語や考え方を、あとから見返しやすい形で整理',
        "keywords": (
            '応用情報技術 - 基礎',
        ),
        "limit": 25,
    },
    {
        "label": 'Git - 基本操作',
        "summary": 'Gitの開発準備や状態管理の考え方、基本操作を整理',
        "keywords": (
            'Git - GitHub登録・SSH鍵設定・ブランチ作成までの開発準備',
            'Git - 状態管理と基本操作',
        ),
        "limit": 5,
    },
    {
        "label": 'MathJax',
        "summary": 'MathJaxを使った数式表示の基本と、MathML・LaTeXによる記述方法を整理',
        "keywords": (
            'MathJax - MathML、LaTeX ',
        ),
        "limit": 5,
    },
)


def _natural_title_key(title):
    return tuple(int(part) if part.isdigit() else part.casefold()
                 for part in re.split(r"(\d+)", title))


def group_posts_by_series(posts, *, for_home=False):
    """Keep known themes in order and retain unmatched posts in the directory."""
    remaining = list(posts)
    groups = []
    for definition in SERIES_GUIDES:
        keywords = tuple(term.casefold() for term in definition["keywords"])
        matched = [post for post in remaining
                   if any(term in post.title.casefold() for term in keywords)]
        if not matched:
            continue

        def sort_key(post):
            keyword_position = 0
            if definition.get("keyword_order"):
                keyword_position = next(index for index, term in enumerate(keywords)
                                        if term in post.title.casefold())
            order = (post.pk,) if for_home else (_natural_title_key(post.title), post.pk)
            return (keyword_position, *order)

        matched.sort(key=sort_key)
        matched_ids = {post.pk for post in matched}
        remaining = [post for post in remaining if post.pk not in matched_ids]
        groups.append({
            "label": definition["label"],
            "summary": definition["summary"],
            "posts": matched[:definition["limit"]] if for_home else matched,
        })
    if remaining and not for_home:
        groups.append({
            "label": "その他の記事",
            "summary": "",
            "posts": sorted(remaining, key=lambda post: (_natural_title_key(post.title), post.pk)),
        })
    return groups
