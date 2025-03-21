## タイトル
Django - Django Debug Toolbar : 導入手順と設定方法

## 目的
この記事では、Django Debug Toolbarの導入手順と設定方法について説明する。

## 実施内容
### django-debug-toolbarの導入
`django-debug-toolbar`は、開発時に必要になってくる`セッション情報 `や`リクエスト/レスポンス情報`、そして`実行したSQL`などリアルタイムで様々な情報を確認できるプラグイン。<br>
- django-debug-toolbarのインストール<br>
ここでは、仮想環境上で`Django`が動いているため、仮想環境に`django-debug-toolbar`をインストールする。<br>
※ 詳細は、[Djangoインストール](https://sigma-se.com/detail/3/#:~:text=V%0APython%203.6.4-,Django%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB,-venv%E3%81%A7%E4%BB%AE%E6%83%B3)を参照。
  ```bash
  $ source /var/www/vops/bin/activate
  (vops) $ pip install django-debug-toolbar
  Collecting django-debug-toolbar
  　  Downloading https://files.pythonhosted.org/packages/97/c6/523fc2ca98119d21c709bbc47217b1d5fd17c6f9449ef32490889363d97d/django_debug_toolbar-1.10.1-py2.py3-none-any.whl (207kB)
      100% |################################| 215kB 10.0MB/s
  Collecting sqlparse>=0.2.0 (from django-debug-toolbar)
    Downloading https://files.pythonhosted.org/packages/65/85/20bdd72f4537cf2c4d5d005368d502b2f464ede22982e724a82c86268eda/sqlparse-0.2.4-py2.py3-none-any.whl
   Requirement already satisfied: Django>=1.11 in /var/www/vops/lib/python3.6/site-packages (from django-debug-toolbar) (2.0.2)
   Requirement already satisfied: pytz in /var/www/vops/lib/python3.6/site-packages (from Django>=1.11->django-debug-toolbar) (2018.3)
   Installing collected packages: sqlparse, django-debug-toolbar
   Successfully installed django-debug-toolbar-1.10.1 sqlparse-0.2.4
   You are using pip version 10.0.1, however version 18.1 is available.
   You should consider upgrading via the 'pip install --upgrade pip' command.
  ```
  上記でインストールが完了。<br>
