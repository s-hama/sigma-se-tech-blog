## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：4/4 PostgreSQL・Django本番設定と起動確認

## 概要

PostgreSQLの初期設定、Djangoのデータベース接続、settings.pyの本番向け設定、起動確認までを整理する。

Djangoサイトを公開する最後の段階では、データベース、マイグレーション、セキュリティ設定、静的ファイル、Apache連携をまとめて確認する必要がある。runserverと本番起動の違いも押さえておく。

## 前提環境

| 項目 | 内容 |
| --- | --- |
| OS | CentOS 7.4 |
| 言語 | Python |
| Webサーバー | Apache |
| フレームワーク | Django |
| データベース | PostgreSQL |
| ドメイン | example.com |

## この記事で理解できること
- PostgreSQLの初期化、ユーザー、データベース作成。
- Djangoのmakemigrationsとmigrateの役割。
- settings.pyで確認する本番向け設定。
- DATABASES、STATIC、MEDIA、LOGGINGの基本。
- runserverとApache経由の起動確認の違い。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| PostgreSQL | データベース名、ユーザー名、接続元IP、権限を整理する。 |
| Djangoモデル | マイグレーション対象のモデル定義があることを確認する。 |
| settings.py | DEBUG、ALLOWED_HOSTS、DATABASES、SSL/TLS設定を確認する。 |
| ファイアウォール | 必要なポートだけを開放する。 |
| 起動確認 | 開発用runserverとApache経由の本番確認を分けて行う。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| データベースユーザー | 作成したユーザー名とDjangoのDATABASES設定を一致させる。 |
| DEBUG設定 | 本番ではFalseにし、ALLOWED_HOSTSを正しく設定する。 |
| マイグレーション | モデル変更後はmakemigrationsとmigrateを忘れない。 |
| runserverとApache | 両方を混同すると、どちらで動いているか分かりにくくなる。 |

## 実施内容
### データベースの環境構築
- PostgreSQLインストール
  ```bash
  $ yum -y install postgresql-server 
  ```

- データベースとユーザーの作成<br>
データベース**MACUOSDB**とアクセスユーザー**padmin**を作成。
  ```bash
  $ postgresql-setup initdb    # データベースの初期化
  $ service postgresql start    # PostgreSQLを起動
  $ sudo -u postgres psql    # postgresでログイン
  postgres=# CREATE DATABASE MACUOSDB;    # データベースの作成
  postgres=# CREATE USER padmin WITH PASSWORD '*****';    # ユーザー、パスワードの作成
  postgres=# ALTER ROLE padmin SET client_encoding TO 'utf8';    # padminの文字コードを設定
  postgres=# ALTER ROLE padmin SET default_transaction_isolation TO 'read committed';    # 実行された結果だけを見に行く
  postgres=# ALTER ROLE padmin SET timezone TO 'UTC+9'; # タイムゾーンを設定
  postgres=# GRANT ALL PRIVILEGES  ON DATABASE MACUOSDB TO padmin;    # padminに権限を付与
  ```

- PostgreSQLを起動確認<br>
active (running) と表示されていれば成功。
  ```bash
  $ service postgresql status
  ```

### Django周りの設定
以下、Djangoのモデル定義が終わっていることが前提。
- マイグレーションファイルを作成<br>
※ マイグレーションファイル(モデルの内容をデータベースに適用するファイル)<br>
  ```bash
  $ /var/www/vops/ops/manage.py makemigrations
  ```

- マイグレーションファイルをデータベースに反映<br>
マイグレーションファイルを基に、データベースの構造(テーブルの作成や更新)を変更する。
  ```bash
  $ /var/www/vops/ops/manage.py migrate
  ```

- スーパーユーザーの作成<br>
  ```bash
  $ /var/www/vops/ops/manage.py createsuperuser
  ```

- Djangoのポートを解放<br>
Djangoで使用する開発用ポート8080を解放する。<br>
  ```bash
  $ firewall-cmd --permanent --add-port=8080/tcp
  $ firewall-cmd --reload
  ```

### PostgreSQL周りの設定
- **postgresql.conf**の`listen_addresses`を公開
  ```bash
  $ vim /var/lib/pgsql/data/postgresql.conf
  listen_addresses = '*'    # localhostを*に修正
  ```

- **pg_hba.conf(認証設定ファイル)**にドメイン情報を追加<br>
IPアドレスは、サーバーのものを指定する。
その他項目については、公式文章を参照。
https://www.postgresql.jp/document/9.2/html/auth-pg-hba-conf.html
  ```bash
  $ vim /var/lib/pgsql/data/pg_hba.conf
  # 下記を追記
  host    all             all             XXX.XXX.XXX.XXX/32        md5
  ```

- firewallの設定<br>
ポート5432を解放する。
  ```bash
  $ firewall-cmd --add-port=5432/tcp --zone=public --permanent    # portを解放
  $ firewall-cmd --reload    # 再読込
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
      'macuos',    # アプリケーション名を追加。
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
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
- ROOT_URLCONFの修正
  ```bash
  ROOT_URLCONF = 'ops.urls'    # インタセプターの指令ファイルを指定
  ```
- DATABASESの設定
  ```bash
  DATABASES = {
      'default': {
          'ENGINE': 'django.db.backends.postgresql_psycopg2',
          'NAME': 'macuosdb', 
          'USER': 'padmin',
          'PASSWORD': '*****',
          'HOST': 'example.com',
          'PORT': '5432'
      }
  }
  ```
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
- ログの設定(任意)
  ```bash
  LOGGING = {
      'version': 1,
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
          'file': {
              'level': 'DEBUG',
              'class': 'logging.FileHandler',
              'filename': os.path.join('/var/log/httpd', 'django.log'),
              'formatter': 'all',
          },
          'console': {
              'level': 'DEBUG',
              'class': 'logging.StreamHandler',
              'formatter': 'all'
          },
      },
      'loggers': {
          'command': {
              'handlers': ['file', 'console'],
              'level': 'DEBUG',
          },
      },
  }
  ```

### 起動確認　
- Djangoの起動確認
  - **manage.py**の`runserver`コマンドでDjangoを起動<br>
  ※ `runserver`コマンド実行後、http://example.com:8080にアクセスし、ロケットが離陸している画像が表示されれば正常にDjangoが起動している。<br>
  ※ runserverは、開発モードでの起動であることに注意。
    ```bash
    $ /var/www/vops/ops/manage.py runserver example.com:8080
    ```

- 本番環境の起動確認<br>
**Apache**、**PostgreSQL**を再起動後、https://example.comにアクセスし、自身で作成したアプリが起動すれば成功。<br>
モデルを修正した場合は、**manage.py**の`makemigrations`、`migrate`を忘れないこと。<br><br>
また、Django を単独で起動する**manage.py**の`runserver`や`runsslserver`は、あくまで開発モードなのでApacheと混同して両方起動しないように注意。<br><br>
※ Apacheもrunserverも単独で動くので双方起動した場合、別プロセスで動きつつApache、Djangoそれぞれでリクエストを解析するので設定次第でどちらかが先に動き挙動がおかしくなる。<br>

## 実務とのつながり
- DB接続設定<br>
    アプリケーションとデータベースの責務分離を理解する基礎になる。
- 本番設定<br>
    DEBUG、Cookie、HTTPS設定はセキュリティに直結する。
- ログ設定<br>
    障害調査の入口になるため、出力先と内容を決めておくことが重要になる。

## 要約
- Djangoサイト公開の仕上げでは、PostgreSQL、マイグレーション、settings.pyをまとめて確認する。
- 本番環境ではDEBUGを無効化し、ALLOWED_HOSTSやSSL/TLS関連設定を整える。
- 起動確認はrunserverではなく、最終的にApache経由で確認する。
