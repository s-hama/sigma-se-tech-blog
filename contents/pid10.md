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

### django-debug-toolbarの設定追加
- settings.pyの設定<br>
settings.pyの最低限必要な設定を変更する。<br>
  - DEBUGモードの変更<br>
  `DEBUG`を`True`に変更する。
    ```bash
    $ vim /var/www/vops/ops/ops/settings.py
     … (省略)…
     DEBUG = True    # DEBUGモードをTrueに変更
     … (省略)…
    ```

  - INSTALLED_APPSへ追加<br>
  `INSTALLED_APPS`に`'debug_toolbar'`を追記する。
  `'debug_toolbar'`が`'django.contrib.staticfiles'`よりも**後ろ**になるよう注意。
    ```bash
    $ vim /var/www/vops/ops/ops/settings.py
     … (省略)…
     INSTALLED_APPS = [
         'macuos',
         'django.contrib.admin',
         'django.contrib.auth',
         'django.contrib.contenttypes',
         'django.contrib.sessions',
         'django.contrib.messages',
         'django.contrib.staticfiles',
         'debug_toolbar'    # ← 追記：'django.contrib.staticfiles' よりも後ろに設定
     ]
     … (省略)…
    ```

  - MIDDLEWAREへ追加<br>
  `MIDDLEWARE`に`'debug_toolbar.middleware.DebugToolbarMiddleware'`を追記する。
    ```bash
    $ vim /var/www/vops/ops/ops/settings.py
     … (省略)…
     MIDDLEWARE = [
         'django.middleware.security.SecurityMiddleware',
         'django.contrib.sessions.middleware.SessionMiddleware',
         'django.middleware.common.CommonMiddleware',
         'django.middleware.csrf.CsrfViewMiddleware',
         'django.contrib.auth.middleware.AuthenticationMiddleware',
         'django.contrib.messages.middleware.MessageMiddleware',
         'django.middleware.clickjacking.XFrameOptionsMiddleware',
         'debug_toolbar.middleware.DebugToolbarMiddleware'   # ← 追記
     ]
     … (省略)…
    ```

  - INTERNAL_IPSの追加<br>
  `INTERNAL_IPS`を追記する。<br>
    ```bash
    $ vim /var/www/vops/ops/ops/settings.py
     … (省略)…
    INTERNAL_IPS = ['127.0.0.1']   # 追加
     … (省略)…
    ```
    ※ INTERNAL_IPSは、このIPアドレスで接続されたときのみ、django-debug-toolbar が表示される設定項目であるため、ローカル開発時は、localhost の '127.0.0.1' を設定する。<br>
    ローカルではない別サーバーでDjangoを動かしている場合は、開発マシンのグローバルIPアドレスを入力すること。

- urls.pyの設定
`urlpatterns`に`Debug Toolbar`を追加する。<br>
  - `urlpatterns`に`Debug Toolbar`を追加<br>
    ```bash
    $ vim /var/www/vops/ops/ops/urls.py
     … (省略)…
     if settings.DEBUG:    # この if 文 (5STEP) を追加する。
         import debug_toolbar
         urlpatterns = [
             url(r'^__debug__/', include(debug_toolbar.urls))
         ] + urlpatterns
     … (省略)…
    ```
  以上で設定は完了。

### Debug Toolbarの表示確認
管理者画面や作成したWebアプリの画面に接続すると右側に`Debug Toolbar`が表示される。
![pid10_1](/static/tblog/img/pid10_1.png)

- CSSが効いてない場合の対処
staticファイルのロード先を別フォルダに設定している場合は、CSSが効いてない状態で表示されている可能性がある。<br>
その場合は、下記コマンドでインストール先を特定し、その直下にある`debug_toolbar/static/debug_toolbar`ディレクトリをstaticファイルのロード先ディレクトリ直下にコピーすること。
  ```bash
  $ pip show django-debug-toolbar
   … (省略)…
   Location: /var/www/vops/lib/python3.6/site-packages    # django-debug-toolbar のインストール先を確認
   … (省略)…
  $ cp -r /var/www/vops/lib/python3.6/site-packages/debug_toolbar/static/debug_toolbar [staticファイルのロード先フォルダ]
  ```
