## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：4/4 PostgreSQL・Django本番設定と起動確認

## 概要

PostgreSQLの初期設定、Djangoのデータベース接続、settings.pyの本番向け設定、起動確認までを整理する。

Djangoサイトを公開する最後の段階では、データベース、マイグレーション、セキュリティ設定、静的ファイル、Apache連携をまとめて確認する必要がある。runserverと本番起動の違いも押さえておく。

※ 注意：この記事は、2018年当時のCentOS 7.4環境の構築記録をもとに、前記事で採用した後年の旧バージョン（Django 2.2、psycopg2 2.8系）と整合するよう再構成した例であり、2018年当時のパッケージ構成を厳密に再現するものではない。<br>
CentOS 7標準のPostgreSQL 9.2はDjango 2.2の要件（PostgreSQL 9.4以上）を満たさないため、PGDG版PostgreSQL 9.6を使用する。<br>
これらはすべてサポート終了済みなので、新規の本番環境へ採用しない。<br>
以下では、データベースをDjangoと同じVPSで動かす構成を前提とする。

## 前提環境

- OS<br>
CentOS 7.4（サポート終了済み）
- 言語<br>
Python
- Webサーバー<br>
Apache
- フレームワーク<br>
Django
- データベース<br>
PostgreSQL 9.6（サポート終了済み）
- ドメイン<br>
example.com

## この記事で扱うこと
- PostgreSQLの初期化、ユーザー、データベース作成。
- Djangoのmakemigrationsとmigrateの役割。
- settings.pyで確認する本番向け設定。
- DATABASES、STATIC、MEDIA、LOGGINGの基本。
- runserverとApache経由の起動確認の違い。

## 作業時の注意点

- データベースユーザー<br>
作成したユーザー名とDjangoのDATABASES設定を一致させる。
- DEBUG設定<br>
本番ではFalseにし、ALLOWED_HOSTSを正しく設定する。
- マイグレーション<br>
モデル変更後はmakemigrationsとmigrateを忘れない。
- runserverとApache<br>
両方を混同すると、どちらで動いているか分かりにくくなる。

## 実施内容
### データベースの環境構築
- PostgreSQL 9.6インストール（旧環境の例）<br>
  当時のPostgreSQL公式Yumリポジトリ（PGDG 9.6）を有効化した後、Django 2.2の要件を満たすPostgreSQL 9.6を導入する。<br>現在はPostgreSQL 9.6もサポート終了済みなので、このパッケージ名を新規構築へ流用せず、サポート中のOSとPostgreSQLを選ぶ。
  ```bash
  $ yum -y install postgresql96-server postgresql96-devel gcc
  ```

- DjangoからPostgreSQLへ接続するドライバーをインストール<br>
  この記事のPython 3.6環境では、対応する`psycopg2`を仮想環境へ導入する。新しい環境では、利用中のDjangoが対応する`psycopg`または`psycopg2`と公式の導入方法を確認する。
  ```bash
  $ source /var/www/vops/bin/activate
  $ export PATH="/usr/pgsql-9.6/bin:$PATH"
  $ python -m pip install "psycopg2<2.9"
  ```

- データベースとユーザーの作成<br>
データベース**exampledb**とアクセスユーザー**appuser**を作成する。<br>PostgreSQLでは引用符なしの識別子が小文字へ変換されるため、SQLとDjangoの設定で最初から小文字に統一する。
  ```bash
  $ /usr/pgsql-9.6/bin/postgresql96-setup initdb    # データベースの初期化
  $ systemctl start postgresql-9.6    # PostgreSQLを起動
  $ systemctl enable postgresql-9.6    # 自動起動を有効化
  $ sudo -u postgres /usr/pgsql-9.6/bin/psql    # postgresでログイン
  postgres=# CREATE USER appuser WITH PASSWORD '十分に長いパスワード';
  postgres=# CREATE DATABASE exampledb OWNER appuser;
  postgres=# ALTER ROLE appuser SET client_encoding TO 'utf8';
  postgres=# ALTER ROLE appuser SET default_transaction_isolation TO 'read committed';
  postgres=# ALTER ROLE appuser SET timezone TO 'Asia/Tokyo';
  ```

- PostgreSQLを起動確認<br>
active (running) と表示されていれば成功。
  ```bash
  $ systemctl status postgresql-9.6
  ```

### Django周りの設定
以下、Djangoのモデル定義が終わっていることが前提。
- マイグレーションファイルを作成<br>
※ マイグレーションファイル(モデルの内容をデータベースに適用するファイル)<br>
  ```bash
  $ /var/www/vops/bin/python /var/www/vops/ops/manage.py makemigrations
  ```

- マイグレーションファイルをデータベースに反映<br>
マイグレーションファイルを基に、データベースの構造(テーブルの作成や更新)を変更する。
  ```bash
  $ /var/www/vops/bin/python /var/www/vops/ops/manage.py migrate
  ```

- スーパーユーザーの作成<br>
  ```bash
  $ /var/www/vops/bin/python /var/www/vops/ops/manage.py createsuperuser
  ```

- Djangoの開発用サーバーを外部公開しない<br>
`runserver`は動作確認専用であり、本番公開を目的としたサーバーではない。<br>同じVPS内から`127.0.0.1`で確認し、8080番ポートを`firewalld`で外部へ開放しない。

### PostgreSQL周りの設定
- **postgresql.conf**の`listen_addresses`をローカル接続に限定<br>
  DjangoとPostgreSQLが同じVPS上にあるため、インターネットから5432番ポートへ接続させる必要はない。
  ```bash
  $ vim /var/lib/pgsql/9.6/data/postgresql.conf
  listen_addresses = 'localhost'
  ```

- **pg_hba.conf（認証設定ファイル）**にドメイン情報を追加<br>
ローカルホストから`exampledb`へ接続するルールを追加する。<br>アドレス欄はサーバー自身ではなく、接続元クライアントの範囲を表す。<br>`pg_hba.conf`は上から順に最初に一致したルールが使われるため、`host all all 127.0.0.1/32 ...`のような広いルールより前へ挿入する。
  ```bash
  $ vim /var/lib/pgsql/9.6/data/pg_hba.conf
  # ローカルホスト向けの広いhostルールより前へ追加
  host    exampledb    appuser    127.0.0.1/32    md5
  ```
  `md5`はこの旧環境に合わせた認証方式である。現行PostgreSQLではSCRAM認証を優先し、サーバーとクライアントの対応状況を公式ドキュメントで確認する。

- PostgreSQLの再起動<br>
  `listen_addresses`と`pg_hba.conf`を変更した後、PostgreSQLを再起動する。<br>5432番ポートは`firewalld`で公開しない。データベースを別サーバーへ分離する場合だけ、接続元IP、TLS、クラウド側のセキュリティグループを含めて別途設計する。
  ```bash
  $ systemctl restart postgresql-9.6
  ```

### settings.pyの設定
- デバッグモードの無効化
  ```bash
  DEBUG = False    # 開発モードのTrueからFalseに修正
  ```
- ALLOWED_HOSTSを自身のドメインに設定
  ```bash
  ALLOWED_HOSTS = ['example.com']    # 自身のドメインに修正
  ```
- INSTALLED_APPSにアプリケーション名を追加
  ```bash
  INSTALLED_APPS = [
      'webapp',    # アプリケーション名を追加
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  ]
  ```
- SSL/TLS周りの設定を追加
  ```bash
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
  `SECURE_PROXY_SSL_HEADER`は、TLSを終端する信頼済みリバースプロキシが`X-Forwarded-Proto`を設定し、外部から届いた同名ヘッダーを除去できる場合にだけ設定する。<br>ApacheのHTTPS VirtualHostからmod_wsgiへ直接渡す今回の構成では不要となる。
- ROOT_URLCONFの修正
  ```bash
  ROOT_URLCONF = 'ops.urls'    # URLとビューを対応付けるURLconfモジュールを指定
  ```
- DATABASESの設定
  ```bash
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql',
          'NAME': 'exampledb',
          'USER': 'appuser',
          'PASSWORD': os.environ['DJANGO_DB_PASSWORD'],
          'HOST': '127.0.0.1',
          'PORT': '5432'
      }
  }
  ```
  パスワードや`SECRET_KEY`はソースコードへ直接書かず、環境変数や権限を制限した設定ファイルから読み込む。<br>この例では`DJANGO_DB_PASSWORD`が未設定だとDjango起動時にエラーになるため、`manage.py`を実行するシェルだけでなく、Apacheサービスの起動環境にも同じ値を安全に渡す必要がある。<br>具体的な受渡し方法はOSやサービス管理方法に合わせ、権限を制限した環境ファイルやシークレット管理機能を利用する。
- 日本語化、タイムゾーンの設定
  ```bash
  LANGUAGE_CODE = 'ja'
  TIME_ZONE = 'Asia/Tokyo'
  USE_I18N = True
  USE_L10N = True
  USE_TZ = True
  ```
- 静的ファイル、メディアファイルのパス設定
  ```bash
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```
  `MEDIA_ROOT`はアップロードファイルの保存先を定めるだけで、`DEBUG=False`の環境でApacheから自動配信されるわけではない。<br>メディア機能を使う場合は、アップロードされた内容を実行させない安全なApache設定またはオブジェクトストレージを別途用意する。
  `STATIC_ROOT`を設定した後、Apacheが配信する静的ファイルを集約する。
  ```bash
  $ /var/www/vops/bin/python /var/www/vops/ops/manage.py collectstatic --noinput
  ```
- ログの設定(任意)<br>
  まずは標準エラーへ出力する`StreamHandler`を使うと、Apache側のエラーログやサービス管理機能へ集約しやすい。<br>`FileHandler`を使う場合は、mod_wsgiの実行ユーザーが出力先へ書き込める権限とSELinux設定を別途用意する。
  ```python
  LOGGING = {
      'version': 1,
      'disable_existing_loggers': False,
      'formatters': {
          'all': {
              'format': ' *** '.join([
                  "[%(levelname)s]",
                  "asctime:%(asctime)s",
                  "module:%(module)s",
                  "message:%(message)s",
                  "process:%(process)d",
                  "thread:%(thread)d",
              ])
          },
      },
      'handlers': {
          'console': {
              'class': 'logging.StreamHandler',
              'formatter': 'all'
          },
      },
      'loggers': {
          'django': {
              'handlers': ['console'],
              'level': 'INFO',
              'propagate': False,
          },
      },
  }
  ```

### 起動確認
- Django単体の診断<br>
  **manage.py**の`runserver`をループバックアドレスだけにバインドし、VPS内から確認する。これは問題の切り分け用であり、本番トラフィックには使用しない。<br>上記の`SECURE_SSL_REDIRECT=True`が有効なため、このHTTPリクエストではHTTPSへのリダイレクトが返ればDjangoが応答していることを確認できる。<br>画面内容まで確認する場合は、本番設定を弱めず、リダイレクトを無効にした開発用設定を別途使用する。
    ```bash
    $ /var/www/vops/bin/python /var/www/vops/ops/manage.py runserver 127.0.0.1:8080
    $ curl -I -H 'Host: example.com' http://127.0.0.1:8080/
    ```

- 本番環境の起動確認<br>
DjangoのデプロイチェックとApacheの構文確認を行い、**Apache**、**PostgreSQL**を再起動する。<br>その後、https://example.comへアクセスし、作成したアプリがApache経由で表示されれば成功となる。
  ```bash
  $ /var/www/vops/bin/python /var/www/vops/ops/manage.py check --deploy
  $ apachectl configtest
  $ systemctl restart postgresql-9.6 httpd
  $ curl -I https://example.com/
  ```
モデルを修正した場合は、**manage.py**の`makemigrations`、`migrate`を実行する。<br>`runserver`とApacheは通常は別ポートで動くため競合するわけではないが、確認先を取り違えないよう、単体診断後は`runserver`を停止してApache経由の結果を確認する。

## まとめ
- Djangoサイト公開の仕上げでは、PostgreSQL、マイグレーション、settings.pyをまとめて確認する。
- 本番環境ではDEBUGを無効化し、ALLOWED_HOSTSやSSL/TLS関連設定を整える。
- 起動確認はrunserverではなく、最終的にApache経由で確認する。

### 参考文献
- [The CentOS Project, CentOS Linux（CentOS Linux 7のEOL）](https://www.centos.org/centos-linux/)
- [PostgreSQL, Linux downloads（Red Hat family）](https://www.postgresql.org/download/linux/redhat/)
- [PostgreSQL Documentation, The pg_hba.conf File](https://www.postgresql.org/docs/current/auth-pg-hba-conf.html)
- [PostgreSQL Documentation, Connections and Authentication](https://www.postgresql.org/docs/current/runtime-config-connection.html)
- [PostgreSQL 9.6 Documentation, The pg_hba.conf File](https://www.postgresql.org/docs/9.6/auth-pg-hba-conf.html)
- [PostgreSQL Documentation, Password Authentication（SCRAM）](https://www.postgresql.org/docs/current/auth-password.html)
- [Psycopg Documentation, Installation（psycopg2）](https://www.psycopg.org/docs/install.html)
- [Django 2.2 Documentation, Databases（PostgreSQL要件）](https://docs.djangoproject.com/en/2.2/ref/databases/)
- [Django Documentation, Deployment checklist](https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/)
- [Django Documentation, SECURE_PROXY_SSL_HEADER](https://docs.djangoproject.com/en/5.2/ref/settings/#secure-proxy-ssl-header)
- [Django Documentation, The staticfiles app](https://docs.djangoproject.com/en/5.2/ref/contrib/staticfiles/)
