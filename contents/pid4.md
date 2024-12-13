## タイトル
VPSで作るDjangoサイト構築手順 - Apache編 : 4/4 データベース設定と起動確認

## 目的
この記事では、以下のVPS環境でDjangoサイトを構築するために必要な「データベース設定と起動確認手順」について説明する。
- OS：CentOS 7,4
- 言語：Python
- WEBサーバー：Apache
- FW：Django
- DB：PostgresSQL
- ドメイン：example.com

## 実施内容
### データベースの環境構築
- PostgreSQLインストール
  ```
  yum -y install postgresql-server 
  ```

- データベースとユーザーの作成<br>
データベース`MACUOSDB`とアクセスユーザー`padmin`を作成。
  ```
  $ postgresql-setup initdb # データベースの初期化
  $ service postgresql start # PostgreSqlを起動
  $ sudo -u postgres psql # postgresでログイン
  postgres=# CREATE DATABASE MACUOSDB; # データベースの作成
  postgres=# CREATE USER padmin WITH PASSWORD '*****'; # ユーザー、パスワードの作成
  postgres=# ALTER ROLE padmin SET client_encoding TO 'utf8'; # padminの文字コードを設定
  postgres=# ALTER ROLE padmin SET default_transaction_isolation TO 'read committed';  # 実行された結果だけを見に行く
  postgres=# ALTER ROLE padmin SET timezone TO 'UTC+9'; # タイムゾーンを設定
  postgres=# GRANT ALL PRIVILEGES  ON DATABASE MACUOSDB TO admin;  # padminに権限を付与
  ```

- PostgreSqlを起動確認<br>
active (running) と表示されていれば成功。
  ```
  $ service postgresql status
  ```

### Django周りの設定
以下、Djangoのモデル定義が終わっていることが前提。
- マイグレーションファイルを作成<br>
※ マイグレーションファイル(モデルの内容をデータベースに適用するファイル)<br>
  ```
  $ /var/www/vops/ops/manage.py makemigrations
  ```

- マイグレーションファイルをデータベースに反映<br>
マイグレーションファイルを基に、データベースの構造(テーブルの作成や更新)を変更する。
  ```
  $ /var/www/vops/ops/manage.py migrate
  ```

- スーパーユーザーの作成<br>
  ```
  $ /var/www/vops/ops/manage.py createsuperuser
  ```

- staticファイルの設定、収集<br>
`settings.py`に`STATIC_ROOT`を定義する。<br>
`collectstatic`により、このパスへ静的ファイルが収集される。
  ```
  $ vim /var/www/vops/ops/ops/settings.py
  # STATIC_ROOT = os.path.join(BASE_DIR, "static/") ← この行を追記
  $ /var/www/vops/ops/manage.py collectstatic
  ```

- Djangoのポートを解放<br>
Djangoで使用するポートを解放する。<br>
※ ここでは開発用として8080を解放する。
  ```
  # firewall-cmd --permanent --add-port=8080/tcp
  # firewall-cmd --reload
  ```

- プロジェクトのドメイン設定<br>
  - `settings.py`の`ALLOWED_HOST`にドメインを設定
  ```
  # firewall-cmd --permanent --add-port=8080/tcp
  # firewall-cmd --reload
  ```
  - `settings.py`に`STATIC_ROOT`を定義<br>
  ※ collectstaticにより、このパスへ静的ファイルが収集されるようになる。
  ```
  $ vim /var/www/vops/ops/ops/settings.py 
  # ALLOWED_HOSTS = ['example.com']を指定する。
  ```

### PostgreSql周りの設定
- `postgresql.conf`の`listen_addresses`を公開
  ```
  $ vim /var/lib/pgsql/data/postgresql.conf
  listen_addresses = '*' # localhostを*に修正。 
  ```

- `pg_hba.conf(認証設定ファイル)`にドメイン情報を追加<br>
IPアドレスは、サーバーのものを指定する。
その他項目については、公式文章を参照。
https://www.postgresql.jp/document/9.2/html/auth-pg-hba-conf.html
  ```
  $ vim /var/lib/pgsql/data/pg_hba.conf
  # 下記を追記
  host    all             all             XXX.XXX.XXX.XXX/32        md5
  ```

- firewallの設定<br>
ポート5432を解放する。
  ```
  $ firewall-cmd --add-port=5432/tcp --zone=public --permanent # portを解放
  $ firewall-cmd --reload # 再読込
  ```

### settings.pyの設定
- デバッグモードの無効化
  ```
  DEBUG = False # 開発モードのTrueからFalseに修正。
  ```
- ALLOWED_HOSTSを自身のドメインに設定
  ```
  ALLOWED_HOSTS = ['example.com'] # 自身のドメインに修正。
  ```
- INSTALLED_APPSにアプリケーション名を追加
  ```
  INSTALLED_APPS = [
      'macuos', # アプリケーション名を追加。
      'django.contrib.admin',
      'django.contrib.auth',
      'django.contrib.contenttypes',
      'django.contrib.sessions',
      'django.contrib.messages',
      'django.contrib.staticfiles',
  ]
  ```
- SSL/TLS周りの設定を追加
  ```
  SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
  SECURE_SSL_REDIRECT = True
  SESSION_COOKIE_SECURE = True
  CSRF_COOKIE_SECURE = True
  ```
- ROOT_URLCONFの修正
  ```
  ROOT_URLCONF = 'ops.urls' # インタセプターの指令ファイルを指定。
  ```
- DATABASESの設定
  ```
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
  ```
  LANGUAGE_CODE = 'ja'
  TIME_ZONE = 'Asia/Tokyo'
  USE_I18N = True
  USE_L10N = True
  USE_TZ = True
  ```
- 静的ファイル、メディアファイルのパス設定
  ```
  STATIC_URL = '/static/'
  STATIC_ROOT = os.path.join(BASE_DIR, 'static')
  MEDIA_URL = '/media/'
  MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
  ```
- ログの設定(任意)
  ```
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
  - `manage.py`の`runserver`コマンドでDjangoを起動<br>
  ※ `runserver`コマンド実行後、http://example.com:8080にアクセスし、ロケットが離陸している画像が表示されれば正常にDjangoが起動している。<br>
  ※ runserver は、開発モードでの起動であることに注意。
    ```
    $ /var/www/vops/ops/manage.py runserver example.com:8080
    ```

- 本番環境の起動確認<br>
`Apache`、`PostgresSQL`を再起動後、https://example.com にアクセスし、自身で作成したアプリが起動すれば成功。<br>
モデルを修正した場合は、、`manage.py`の`makemigrations`、`migrate`を忘れないこと。<br><br>
また、Django を単独で起動する`manage.py`の`runserver`や`runsslserver`は、あくまで開発モードなのでApacheと混同して両方起動しないように注意。<br><br>
※ Apacheもrunserverも単独で動くので双方起動した場合、別プロセスで動きつつApache、Djangoそれぞれでリスエストを解析するので設定次第でどちらかが先に動きおかしな挙動となる。<br>
