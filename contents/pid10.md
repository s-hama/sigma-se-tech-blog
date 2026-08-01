## タイトル
Django - Django Debug Toolbar：1/2 導入手順と設定方法

## 概要

Django Debug Toolbarを導入し、settings.pyとurls.pyへ必要な設定を追加する手順を整理する。

Django Debug Toolbarは、リクエスト、レスポンス、SQL、テンプレートなどの情報をブラウザ上で確認できる開発支援ツールとなる。<br>開発時の調査には便利だが、本番環境や公開サーバーでの利用を想定して強化されたツールではないため、開発環境だけで有効にすることが重要になる。

## この記事の構成
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [django-debug-toolbarの導入](#django-debug-toolbarの導入)<br>
  django-debug-toolbarの導入の手順と確認ポイントを整理。
- [django-debug-toolbarの設定追加](#django-debug-toolbarの設定追加)<br>
  django-debug-toolbarの設定追加の手順と確認ポイントを整理。
- [Debug Toolbarの表示確認](#debug-toolbarの表示確認)<br>
  Debug Toolbarの表示について、確認する項目と結果の見方を整理。

## 作業時の注意点

- Toolbarが出ない<br>
DEBUG、INTERNAL_IPS、URL設定、MIDDLEWAREの順に確認。
- CSSやJavaScriptが読み込めない<br>
staticfilesの設定とブラウザーの開発者ツールを確認。
- 設定順序<br>
DebugToolbarMiddlewareは早い位置に置き、レスポンスを圧縮するミドルウェアより後に置く。
- 本番利用<br>
デバッグ情報を公開しないよう、開発用途に限定する。

## 実施内容
### django-debug-toolbarの導入
`django-debug-toolbar`は、セッション、リクエスト/レスポンス、実行したSQLなどをリクエスト単位で確認できる開発支援パッケージとなる。<br>
- django-debug-toolbarのインストール<br>
仮想環境を有効にしてから、公式手順どおり`python -m pip`でインストール。<br>利用中のPython・Djangoに対応するバージョンは、インストール前に公式ドキュメントで確認。<br>
※ 仮想環境とDjangoの準備は、[Djangoインストール](https://sigma-se.com/detail/3/)を参照。
  ```bash
  $ source /var/www/vops/bin/activate
  (vops) $ python -m pip install django-debug-toolbar
  ```

- Django側の前提設定<br>
通常の`startproject`で作成したプロジェクトでは設定済みだが、`INSTALLED_APPS`に`django.contrib.staticfiles`があり、`TEMPLATES`のDjangoTemplatesバックエンドで`APP_DIRS=True`になっていることを確認。

### django-debug-toolbarの設定追加
- settings.pyの設定<br>
settings.pyの最低限必要な設定を変更。<br>
  - DEBUGモードの変更<br>
  開発環境で`DEBUG=True`となるように設定。<br>本番環境と設定を共有している場合は、環境変数や設定ファイルを分け、本番で誤って有効にならないようにする。
    ```python
    DEBUG = True
    ```

  - INSTALLED_APPSへ追加<br>
  `INSTALLED_APPS`に`"debug_toolbar"`を追記する。
    ```python
    INSTALLED_APPS = [
        # ...
        "django.contrib.staticfiles",
        "debug_toolbar",
    ]
    ```

  - MIDDLEWAREへ追加<br>
  `MIDDLEWARE`に`"debug_toolbar.middleware.DebugToolbarMiddleware"`を追記する。公式手順ではできるだけ早い位置が推奨されるが、`GZipMiddleware`などレスポンスをエンコードするミドルウェアを使用している場合は、その**後ろ**に置く。
    ```python
    MIDDLEWARE = [
        # "django.middleware.gzip.GZipMiddleware",  # 使用する場合はこの後ろ
        "debug_toolbar.middleware.DebugToolbarMiddleware",
        # ...
    ]
    ```

  - INTERNAL_IPSの追加<br>
  `INTERNAL_IPS`を追記する。<br>
    ```python
    INTERNAL_IPS = ["127.0.0.1"]
    ```
    既定の表示判定では、Djangoが認識する接続元IPが`INTERNAL_IPS`に含まれる場合だけToolbarが表示される。<br>Docker、リバースプロキシ、別の開発サーバーを利用する場合は見えるIPが変わるため、公式ドキュメントの`SHOW_TOOLBAR_CALLBACK`も含めて環境に合わせて設定。<br>単に常に`True`を返す設定を公開環境へ置かないよう注意。

- urls.pyの設定
現在の公式手順では、`debug_toolbar_urls()`を利用してToolbar用URLを追加できる。<br>既定では`__debug__/`がプレフィックスとなる。
    ```python
    from debug_toolbar.toolbar import debug_toolbar_urls

    urlpatterns = [
        # アプリケーションのURL
    ] + debug_toolbar_urls()
    ```

  使用しているバージョンやプロジェクト方針によってURLを明示する場合は、古い`url()`ではなく`path()`を使用。
    ```python
    from django.conf import settings
    from django.urls import include, path

    if settings.DEBUG:
        urlpatterns += [
            path("__debug__/", include("debug_toolbar.urls")),
        ]
    ```
  以上で設定は完了。

### Debug Toolbarの表示確認
管理者画面や作成したWebアプリの画面に接続すると右側に`Debug Toolbar`が表示される。
![Django管理画面の右側にDjango Debug Toolbarが表示された例](/static/tblog/img/pid10_1.png)

画像はDjango 2.0.2と当時のDjango Debug Toolbarによる表示例であり、現在のバージョンではパネル名や外観が異なる場合がある。<br>「画面右側に調査用パネルが挿入される」という位置関係の参考として利用できる。

- Toolbarが表示されない場合の確認順序
  1. `DEBUG=True`であり、接続元IPが`INTERNAL_IPS`に含まれているか。
  2. レスポンスのContent-Typeが`text/html`または`application/xhtml+xml`で、HTMLに閉じ`</body>`タグがあるか。
  3. `DebugToolbarMiddleware`、URL、`django.contrib.staticfiles`の設定に漏れがないか。
  4. ブラウザーの開発者ツールに、JavaScriptのMIMEタイプやCORS、404エラーが出ていないか。

パッケージ内のstaticディレクトリを手動コピーすると、更新時に古いファイルが残る原因になる。CSSやJavaScriptが読み込めない場合はコピーで回避せず、Djangoのstaticfiles設定や配信サーバーのMIMEタイプ・CORS設定を確認する。

## まとめ
- Django Debug Toolbarは、Django開発時の調査を助けるデバッグツールとなる。
- 導入には、パッケージインストール、settings.py、urls.pyの設定が必要になる。
- 便利な反面、内部情報を表示するため本番環境では無効化。

### 参考文献
- [Django 6.0 ドキュメント「静的ファイルを管理する」（日本語・公式解説）](https://docs.djangoproject.com/ja/6.0/howto/static-files/)
- [Django Debug Toolbar Documentation, Installation（英語・導入公式手順）](https://django-debug-toolbar.readthedocs.io/en/stable/installation.html)
- [Django Debug Toolbar Documentation, Configuration（英語・設定仕様）](https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html)
- [Django Debug Toolbar Documentation, Tips：The toolbar isn't displayed!（英語・表示トラブルの公式解説）](https://django-debug-toolbar.readthedocs.io/en/stable/tips.html#the-toolbar-isnt-displayed)
