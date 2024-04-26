# 概要
このドキュメントでは、`sigma-se-tech-blog`を構築するサーバー側のセットアップ手順について下記前提元記載する  
- サーバーは、`XserverVPS`を利用することを前提に記載する
- ドメインは、`sigma-se.com`(`お名前.com`で取得)を使用することを前提に記載する
- OSは、`CentOS Stream9`を利用することを前提に記載する
- OSインストール直後の状態から実施した作業について自明であっても省略せずに記載する

## パケットフィルターの設定変更
XserverVPSからパケットフィルターの設定を変更する
- VPSパネルからパケットフィルターを有効(ON)にする
- VPSパネルからフィルタールールに下記設定を追加し、自身のIPのみ接続許可するように変更する
  ```
  プロトコル: TCP
  ポート番号: 22
  許可する送信元IPアドレス: 自身のIPアドレス/32
  ```

## VPS接続用の一般ユーザー作成
サーバー側作業
- rootでのログイン確認(初回)
  ```
  ssh root@[ホスト名]
  ```
- 一般ユーザー作成
  ```
  useradd vpsuser	
  passwd vpsuser
  ```

## OpenSSHのsshd_config設定変更
vpsuser(VPS接続用の一般ユーザー)かつ、公開鍵認証でしかログインできないように変更する

サーバー側作業
- 初期状態でバックアップしておく
  ```
  cp /etc/ssh/sshd_config /etc/ssh/sshd_config.default
  ```
- sshd_config編集
    ```
    vim /etc/ssh/sshd_config
    ```
    - 変更前
      ```
      PermitRootLogin yes
      #PubkeyAuthentication yes
      PasswordAuthentication yes
      ```
    - 変更後
      ```
      # rootで直接ログインできないように変更
      PermitRootLogin no
      # 公開鍵認証を許可するように変更
      PubkeyAuthentication yes
      # パスワードでログインできないように変更
      PasswordAuthentication no
      ```
- SSHを再起動して設定を反映する
  ```
  systemctl restart sshd
  ```

## OpenSSHの公開鍵認証設定
公開鍵認証設定(SSHの鍵ペア設定)を行い、vpsuser(VPS接続用の一般ユーザー)からパスフレーズでログインできるようにする

- クライアント側から秘密鍵、公開鍵の生成
  ```
  ssh-keygen -f ~/.ssh/id_rsa_sigma
  ```

- クライアント側からサーバーに公開鍵を転送
  ```
  scp ~/.ssh/id_rsa_sigma.pub vpsuser@x162-43-85-169.static.xvps.ne.jp:/home/vpsuser/.ssh/
  ```

- サーバーで`id_rsa_sigma.pub`を`authorized_keys`にリネーム
  ```
  mv ~/.ssh/id_rsa_sigma.pub ~/.ssh/authorized_keys
  ```

- サーバーで権限変更
  ```
  chmod 600 ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  chmod 755 ~/
  ```

- クライアント側で権限変更
  ```
  chmod 755 /Users/s-hama
  chmod 700 /Users/s-hama/.ssh
  chmod 600 /Users/s-hama/.ssh/id_rsa_sigma
  chmod 644 /Users/s-hama/.ssh/id_rsa_sigma.pub
  ```

- クライアント側で`~/.ssh`配下に`config`ファイルを下記内容で作成する
  ```
  Host sigma-se-vps
    HostName 162.43.85.169
    User vpsuser
    IdentityFile ~/.ssh/id_rsa_sigma
    Port 22
    TCPKeepAlive yes
    IdentitiesOnly yes
  ```

- クライアント側で初回ログイン (`known_hosts`が自動生成される)
  ```
  ssh sigma-se-vps
    The authenticity of host 'x162-43-85-169.static.xvps.ne.jp (162.43.85.169)' can't be established.
    ED25519 key fingerprint is SHA256:sJ5+zzGjOV/uGBHz+ehjZEqlCJ9oT804bA2viP1pvn4.
    This key is not known by any other names
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

    Warning: Permanently added '162.43.85.169' (ED25519) to the list of known hosts.
    Enter passphrase for key '/Users/s-hama/.ssh/id_rsa_sigma': パスワードフレーズ入力
  ```
  ※ 以降、ssh sigma-se-vpsでログイン時にパスワードフレーズの入力を求められるようになる

## Vimインストールと初期設定
サーバー側作業
- DNFの更新
  ```
  sudo dnf update
  sudo dnf upgrade
  ```

- Vimインストール
  ```
  sudo dnf -y install vim-enhanced
  ```

- コマンドエイリアスを自身のユーザー固有環境として適用する

  最終行にalias vi='vim'を追記
  ```
  vi ~/.bashrc
  ```
  変更を反映
  ```
  source ~/.bashrc
  ```

- 自身のユーザー固有環境としてVimを設定する

  ※ ユーザー単位(rootとvpsuserそれぞれ)で行う
  .vimrcを新規作成
  ```
  vi ~/.vimrc
  ```
  下記の内容で追記し保存
  ```
  " vim の独自拡張機能を使用
  " - vi との互換性無し
  set nocompatible

  " 文字コードを指定
  set encoding=utf-8

  " ファイルエンコードを指定
  " 複数指定する場合はカンマ区切り
  " 複数指定の場合 先頭から順に成功するまで読み込む
  set fileencodings=utf-8

  " 自動認識させる改行コードを指定
  set fileformats=unix,dos

  " バックアップを取得
  " - 逆は [ set nobackup ]
  set backup

  " バックアップを取得するディレクトリを指定
  set backupdir=~/backup

  " 検索履歴を残す世代数
  set history=50

  " 検索時に大文字小文字を区別しない
  set ignorecase

  " 検索語に大文字を混ぜると検索時に大文字を区別する
  set smartcase

  " 検索語にマッチした単語をハイライト
  " - 逆は [ set nohlsearch ]
  set hlsearch

  " インクリメンタルサーチを使用
  " - 検索語の入力最中から随時マッチする文字列の検索を開始
  " - 逆は [ set noincsearch ]
  set incsearch

  " 行番号を表示
  " - 逆は [ set nonumber ]
  set number

  " 改行 ( $ ) やタブ ( ^I ) を可視化
  set list

  " 括弧入力時に対応する括弧を強調
  set showmatch

  " ファイルの末尾に改行を入れない
  set binary noeol

  " 自動インデントを有効にする
  " - 逆は [ noautoindent ]
  set autoindent

  " 構文ごとに色分け表示する
  " - 逆は [ syntax off ]
  syntax on

  " [ syntax on ] の場合のコメント文の色を変更
  highlight Comment ctermfg=LightCyan

  " ウィンドウ幅で行を折り返す
  set wrap
  ```

## ファイアーウォールの設定
サーバー側作業
  - ファイアーウォールの有効化
    - 有効化されているか確認
      ```
      systemctl is-enabled firewalld
      disabled
      ```
    - 無効になっているので有効化する
      ```
      systemctl enable --now firewalld
      Created symlink /etc/systemd/system/dbus-org.fedoraproject.firewalld1.service → /usr/lib/systemd/system/firewalld.service.
      Created symlink /etc/systemd/system/multi-user.target.wants/firewalld.service → /usr/lib/systemd/system/firewalld.service.
      ```
  - 設定確認/変更
    - どのゾーンが許可されているか確認
      ```
      firewall-cmd --get-default-zone
      public
      ```
    - ファイアーウォールの設定状況確認
      ```
      firewall-cmd --list-all
      public (active)
        target: default
        icmp-block-inversion: no
        interfaces: ens3
        sources: 
        services: cockpit dhcpv6-client ssh
        ports: 
        protocols: 
        forward: yes
        masquerade: no
        forward-ports: 
        source-ports: 
        icmp-blocks: 
        rich rules:
      ```
    - httpとhttpsを許可する(servicesにhttpとhttpsが許可されてないため)
      - httpのサービスを永続的に許可
      ```
      firewall-cmd --zone=public --add-service=http --permanent
      ```
      - httpsのサービスを永続的に許可
      ```
      firewall-cmd --zone=public --add-service=https --permanent
      ```
    - ファイアーウォールを再起動する
      ```
      firewall-cmd --reload
      ```
    - ファイアーウォールの設定状況確認
      ```
      firewall-cmd --list-all
      public (active)
        target: default
        icmp-block-inversion: no
        interfaces: ens3
        sources: 
        services: cockpit dhcpv6-client http https ssh
        ports: 
        protocols: 
        forward: yes
        masquerade: no
        forward-ports: 
        source-ports: 
        icmp-blocks: 
        rich rules:
      ```

## Nginxインストール
サーバー側作業
- インストール
  ```
  sudo dnf install -y nginx
  ```
- バージョン確認
  ```
  nginx -v
  nginx version: nginx/1.22.1
  ```
- ステータス確認
  ```
  sudo systemctl status nginx
  ```
- パケットフィルターの設定
  - XserverVPSからパケットフィルターの設定を変更する
    - VPSパネルからパケットフィルターを有効(ON)にする
    - VPSパネルからフィルタールールに下記設定を追加し、自身のIPのみ接続許可するように変更する
      ```
      プロトコル: TCP
      ポート番号: 80
      許可する送信元IPアドレス: 全て許可する
      ```
- ブラウザから起動確認
  ```
  http://サーバーのIPアドレス/
  ```
  デフォルトの`HTTP SERVER TEST PAGE`ページが表示されればOK

## Nginxの初期設定
サーバー側作業
- セキュリティ対策周りの対策

  Nginxの設定ファイル(`/etc/nginx/nginx.conf`)に対して以下の項目を変更する
  ```
  vim /etc/nginx/nginx.conf
  ```

  - ディレクトリリスティングの無効化

    `autoindex on;`があればコメントアウトまたは削除する
    ```
    # autoindex on;
    ```

  - Webサーバーのバージョン非表示化
    httpディレクティブの中に`server_tokens off;`を追記する
    ```
    server_tokens off;
    ```

  - ブラウザで実装されているセキュリティ対策の有効化

    `http > servet`ディレクティブの中に以下の項目を追記する

    クリックジャッキング対策
    ```
    add_header x-frame-options "SAMEORIGIN";
    ```
    XSS対策
    ```
    add_header x-xss-protection "1; mode=block";
    ```
    MIMEタイプのスニッフィング対策
    ```
    add_header x-content-type-options "nosniff";
    ```

  - その他のブラウザで実装されているセキュリティ対策

    http > servetディレクティブの中に以下の項目を追記する

    中間者攻撃対策
    ```
    add_header Strict-Transport-Security "max-age=63072000";
    ```

- Document Root(公開ディレクトリ)の変更
  - 変更後のディレクトリ作成
    ```
    sudo mkdir /var/www
    sudo mkdir /var/www/html
    ```
  - wwwディレクトリの所有者をnginxユーザーに変更、パーミッションを変更
    ```
    sudo chown -R nginx:nginx /var/www
    sudo chmod -R 755 /var/www
    ```
  - htmlディレクトリの所有者をnginxユーザーに変更、パーミッションを変更
    ```
    sudo chown -R nginx:nginx /var/www/html
    sudo chmod -R 755 /var/www/html
    ```
  - 仮のindex.htmlを作成
    ```
    sudo touch /var/www/html/index.html
    ```
    ※ 必要に応じてindex.htmlの中身を記載する
  - `index.html`の所有者をnginxユーザーに変更、パーミッションを変更
    ```
    sudo chown nginx:nginx /var/www/html/index.html
    sudo chmod 644 /var/www/html/index.html
    ```
  - デフォルトページの無効化
    - Document Root(公開ディレクトリ)を/var/www/htmlに変更する
      ```
      vim /etc/nginx/nginx.conf
      ```
      - 変更前
        ```
        root /usr/share/nginx/html;$
        ```
      - 変更後
        ```
        root /var/www/html;$
        index  index.html;$
        ```
    - その他
      - `/etc/nginx/conf.d/`配下など`alias /usr/share/nginx/html/`や`root /usr/share/nginx/html/`の設定があれば削除する

        ※ 本環境では、/etc/nginx/nginx.confに集約されているため対処不要

  - nginxを再起動する
    - Document Root(公開ディレクトリ)を`/var/www/html`に変更する
      ```
      sudo systemctl restart nginx
      ```

  - ブラウザから起動確認
    ```
    http://サーバーのIPアドレス/
    ```
    `/var/www/html`が表示されればOK

## 独自ドメインのネームサーバー設定とDNS設定
独自ドメインをVPSに向ける
- VPS側のネームサーバー設定
  - XserverのDNS設定からドメイン(`sigma-se.com`)の追加を行う  
※ 追加後は、標準で`種別: SOA`のDNSレコードが1つ、`種別: NS`のDNSレコードが3つ追加される
  - DNSレコードを追加するボタンから下記レコードを追加する
    ```
    ホスト名: sigma-se.com
    種別: A
    内容: XserverVPSのIPアドレス
    TTL: 3600
    ```
- ドメイン側のネームサーバー設定
  - Xserverのネームサーバーを登録する
  お名前.com Navi > ドメイン設定 > ネームサーバーの設定 > ネームサーバーの変更 > ドメイン一覧からsigma-se.comを選択し、下記Xserverのネームサーバーを登録する
    ```
    ns1.xvps.ne.jp
    ns2.xvps.ne.jp
    ```
    ※ 設定が反映されるまで数時間〜数日かかる
  
- ブラウザから起動確認
  ```
  http://sigma-se.com/
  ```
  `/var/www/html`が表示されればOK

## Python関連モジュールのインストール
- Python、pip、python3-develのインストール
    ```
    sudo dnf install python3 python3-pip python3-devel
    ```

## 仮想環境(virtualenv)のインストールと環境構築
- 前提
  Djangoプロジェクト及びアプリケーションと仮装環境分けた下記フォルダ構成とする
    ```
    var
    └── www
        ├── projs
        │   └── sweb
        │       ├── config
        │       └── tblog
        └── venvs
            └── sweb
    ```
    - `var/www/projs`: プロジェクトを格納する親フォルダ
    
      ※ 複数のプロジェクトを管理する目的

    - `var/www/projs/sweb`: プロジェクトを格納する親フォルダ

    - `var/www/projs/sweb/config`: Djangoプロジェクトのルートフォルダ

      ※ django-admin startprojectで生成されるものを置く

      ※ プロジェクトのルートフォルダだが結局設定ファイルが置かれるため見やすさを考慮して`config`でプロジェクト作成する
    - `var/www/projs/sweb/tblog`: Djangoアプリケーションのソースコードを格納するフォルダ

      ※ python manage.py startで生成されるものを置く

    - `var/www/venvs`: 仮想環境を作成する親フォルダ

      ※ Pythonの仮想環境をプロジェクト単位で管理する目的

    - `var/www/venvs/sweb`: Djangoプロジェクト`sweb`のための仮想環境フォルダ
    
      ※ プロジェクト独自の仮想環境を作成することで、プロジェクト間の依存関係を分離しする目的

- 仮想環境の構築
  - virtualenvのインストール
    ```
    sudo pip install virtualenv
    ```
  - プロジェクト達を格納する親フォルダを作成
    ```
    mkdir /var/www/projs
    ```
  - プロジェクト(sweb)を格納するを作成
    ```
    mkdir /var/www/projs/sweb
    ```
  - 仮装環境達を格納する親フォルダを作成
    ```
    mkdir /var/www/venvs
    ```
  - 仮想環境を構築
    ```
    virtualenv -p python3 /var/www/venvs/sweb
    ```

- 仮想環境内でDjangoをインストール
  - 仮想環境の起動
    ```
    source /var/www/venvs/sweb/bin/activate
    ```
  - Djangoのインストール
    ```
    pip install django
    ```
  - Djangoプロジェクトの作成
    ```
    cd /var/www/projs/sweb
    django-admin startproject config .
    ```
  - Djangoアプリケーションの作成
    ```
    python manage.py startapp tblog
    ```
- 仮想環境内でuWSGIをインストール
  - 仮想環境の起動
    ```
    pip install uwsgi
    ```

## Nginx, Django, uWSGIの連携設定
- Nginxの設定
  Nginxの設定ファイル(`nginx.conf`)に対して下記内容を変更する
  ```
  vim /etc/nginx/nginx.conf
  ```
  - server_nameにドメインを設定
    - 変更前
      ```
      server_name  _;
      ```
    - 変更後
      ```
      server_name sigma-se.com;
      ```
  - uwsgiとDjangoの連携設定 (serverディレクティブ内に追記)
    ```
    location / {
      include         uwsgi_params;
      uwsgi_pass      unix:/var/www/projs/sweb/sweb.sock;
    }
    ```

- uWSGIの設定
  uWSGIの設定ファイル(`uwsgi.ini`)を下記内容で新規作成する
  ```
  vim /var/www/projs/sweb/config/uwsgi.ini
  ```
  - uwsgiとDjangoの連携設定
    ```
    [uwsgi]
    chdir = /var/www/projs/sweb
    module = config.wsgi:application
    master = true
    processes = 5
    socket = /var/www/projs/sweb/sweb.sock
    chmod-socket = 666
    vacuum = true
    logto =/var/www/projs/sweb/config/uwsgi.ini
    env = PYTHONPATH=/var/www/venvs/sweb/lib/python3.9/site-packages
    ```
- uwsgi_paramsの配置
  ```
  sudo cp -ip /etc/nginx/uwsgi_params /var/www/projs/sweb/
  ```

- Djangoの設定
  Djangoの設定ファイル(`settings.py`)に対して下記内容を変更する
  ```
  vim /var/www/projs/sweb/config/settings.py
  ```
  - `ALLOWED_HOSTS`リストにNginxのサーバー名を追記
    - 変更前
      ```
      DEBUG = True
      ALLOWED_HOSTS = []
      ```
    - 変更後
      ```
      DEBUG = False
      ALLOWED_HOSTS = ['sigma-se.com', 'www.sigma-se.com']
      ```

- エラーページ作成
  404, 500, 502, 503, 504エラー用のページを作成する
  - 404のエラーページ作成
    ```
    vim /var/www/html/404.html
    ```
    ```
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>404 Not Found</title>
      </head>
      <body>
        <h1>404 Not Found</h1>
        <p>The page you requested could not be found.</p>
      </body>
    </html>
    ```
  - 500, 502, 503, 504のエラーページ作成
    ```
    vim /var/www/html/50x.html
    ```
    ```
    <!DOCTYPE html>
    <html lang="en">
      <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Server Error</title>
      </head>
      <body>
        <h1>Server Error</h1>
        <p>Sorry, something went wrong on the server. Please try again later.</p>
      </body>
    </html>
    ```

## PostgreSQLインストール/初期設定とDjangoの連携設定
- PostgreSQLのインストール
  - PostgreSQLを初期化
    ```
    sudo dnf install postgresql-server postgresql-contrib postgresql-devel
    ```
  - PostgreSQLの自動起動設定
    ```
    sudo systemctl enable postgresql
    ```

- PostgreSQLとDjangoの連携設定
  Nginxの設定ファイル(`settings.py`)に対して下記内容を変更する
  ```
  vim /var/www/projs/sweb/config/settings.py
  ```
  - `DATABASES`ディクショナリーにPostgreSQLの設定を追加
    - 変更前
      ```
      DATABASES = {
           'default': {
               'ENGINE': 'django.db.backends.sqlite3',
               'NAME': BASE_DIR / 'db.sqlite3',
           }
      }
      ```
    - 変更後
      ```
      DATABASES = {
          'default': {
              'ENGINE': 'django.db.backends.postgresql',
              'NAME': 'tbdb',
              'USER': 'psadmin',
              'PASSWORD': 'shahoma-se1234',
              'HOST': 'localhost',
              'PORT': '5432',
          }
      }
      ```

- PostgreSQLのユーザーとデータベースを作成
  - postgresでログイン
    ```
    sudo -u postgres psql
    ```
  - データベースの作成
    ```
    postgres=# CREATE DATABASE tbdb;
    ```
  - ユーザー、パスワードの作成
    ```
    postgres=# CREATE USER psadmin WITH PASSWORD '*****';
    ```

  - psadminの文字コードを設定
    ```
    postgres=# ALTER ROLE psadmin SET client_encoding TO 'utf8';
    ```
  - 実行された結果だけを見に行く
    ```
    postgres=# ALTER ROLE psadmin SET default_transaction_isolation TO 'read committed';
    ```

  - タイムゾーンを設定
    ```
    postgres=# ALTER ROLE psadmin SET timezone TO 'UTC+9';
    ```
  - psadminに権限を付与して終了
    ```
    postgres=# GRANT ALL PRIVILEGES ON DATABASE tbdb TO psadmin;
    postgres=# \q
    ```

- アクセス/認証周りの設定
  - `postgresql.conf`の`listen_addresses`を環境に合わせ変更
    ```
    vim /var/lib/pgsql/data/postgresql.conf
    ```
    - 変更前
      ```
      # listen_addresses = 'localhost'
      ```
    - 変更後
      ```
      listen_addresses = '*'
      ```
  - `pg_hba.conf` (認証設定ファイル) にドメイン情報を追加
    ```
    vim /var/lib/pgsql/data/pg_hba.conf
    ```
    - 変更前
      ```
      # "local" is for Unix domain socket connections only
      local   all             all                                     peer
      # IPv4 local connections:
      host    all             all             127.0.0.1/32            ident
      # IPv6 local connections:
      host    all             all             ::1/128                 ident
      ```
    - 変更後
      ```
      # "local" is for Unix domain socket connections only
      local   all             all                                     md5
      # IPv4 local connections:
      host    all             all             127.0.0.1/32            md5
      # IPv6 local connections:
      host    all             all             ::1/128                 md5
      # Allow all users to connect from localhost using md5 password authentication
      host    all             all             162.43.85.169/32        md5
      ```

## modelとデータベースの作成
- modelの定義
  models.pyにmodel定義を追記する
  ```
  vim /var/www/projs/sweb/tblog/models.py
  ```
- Djangoの settings.py ファイルを更新する
  INSTALLED_APPS ディクショナリーにアプリケーション名を追加する
  ```
  vim /var/www/projs/sweb/config/settings.py
  ```
  - 変更前
    ```
    INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',$
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]
    ```
  - 変更後
    ```
    INSTALLED_APPS = [
    'tblog'
    'django.contrib.admin',
    'django.contrib.auth',$
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    ]
    ```
- 仮想環境の起動
  ```
  source /var/www/venvs/sweb/bin/activate
  ```
- psycopg2-binary、psycopg、Pillowパッケージをインストール
  ※ models.pyにてImageFieldを使用するため
  ```
  pip install psycopg2-binary psycopg
  python -m pip install Pillow
  ```
- migrationsの作成
  ※ config=プロジェクト名
  ```
  cd /var/www/projs/sweb
  python manage.py makemigrations tblog
  ```
- Datebaseの作成と更新
  ```
  python manage.py migrate
  ```
- PostgresSQLのスーパーユーザーの作成
  ```
  python manage.py createsuperuser
  ```
- admin.pyの登録
  ```
  vim /var/www/projs/sweb/tblog/admin.py
  ```
    - models.pyで定義したmodelを登録する
    ```
    from django.contrib import admin
    from models import Post, SmallCategory, BigCategory, Tag

    admin.site.register(Post)
    dmin.site.register(SmallCategory)
    admin.site.register(BigCategory)
    admin.site.register(Tag)
    ```
- uwsgiのログファイルの作成
  ```
  touch /var/www/projs/sweb/config/uwsgi.log
  ```

- 一般ユーザー(vpsuser)の所有者/権限に変更
  ```
  sudo chown vpsuser:vpsuser /var/www/projs/sweb
  sudo chmod 775 /var/www/projs/sweb
  sudo chown vpsuser:vpsuser /var/www/projs/sweb/sweb.sock
  sudo chmod 666 /var/www/projs/sweb/sweb.sock
  sudo chown vpsuser:vpsuser /var/www/projs/sweb/config/uwsgi.ini
  sudo chmod 666 /var/www/projs/sweb/config/uwsgi.ini
  sudo chown vpsuser:vpsuser /var/www/projs/sweb/config/uwsgi.log
  sudo chmod 666 /var/www/projs/sweb/config/uwsgi.log
  ```

## 静的ファイルの収集
- staticディレクトリ作成
  ```
  mkdir /var/www/projs/sweb/static
  ```

- 一般ユーザー(vpsuser)の所有者/権限に変更
  ```
  sudo chown vpsuser:vpsuser /var/www/projs/sweb/static
  sudo chmod 755 /var/www/projs/sweb/static ※ 実行権限も必要
  ```

- Djangoのsettings.pyにSTATIC_ROOTを追記
  ```
  vim /var/www/projs/sweb/config/settings.py
  STATIC_ROOT = '/var/www/projs/sweb/static'
  ```

- Nginxの設定ファイルにstaticを定義
  ```
  vim /etc/nginx/nginx.conf
  ```
    - 変更前
      ```
      STATIC_URL = 'static/
      ```
    - 変更後
      ```
      STATIC_URL = '/static/
      location /static/ {
        root /var/www/projs/sweb;	
      }
      ```

- 静的ファイルの収集
  ```
  python manage.py collectstatic
  ```

- Django管理画面の接続確認
  ```
  http://sigma-se.com/admin/
  ```
  PostgresSQLのスーパーユーザー(psadmin)でログインできること

## Let's EncryptのSSL/TLS導入
- EPELインストール
  ```
  sudo dnf config-manager --set-enabled crb
  sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-release-latest-9.noarch.rpm
  sudo dnf install https://dl.fedoraproject.org/pub/epel/epel-next-release-latest-9.noarch.rpm
  ```

- Snappy インストール
  ※ デバイスを初期化するのでしばらくまってから以降のインストールを行うこと
  ```
  sudo dnf --enablerepo=epel -y install snapd
  sudo systemctl enable --now snapd.socket
  sudo ln -s /var/lib/snapd/snap /snap
  ```

- core インストール
  ```
  sudo snap install core
  ```

- cerbot インストール	
  ```
	sudo snap install --classic certbot
	sudo ln -s /snap/bin/certbot /usr/bin/certbot #シンボリックリンク作成
  ```

- `/var/www/html`の権限変更

	証明書を取得するため、/var/www/htmlディレクトリのパーミッション権限に実行権限を加える
  ```
	sudo chmod -R 775 /var/www
	sudo chmod -R 775 /var/www/html
  ```

- 証明書を取得
  ```
	certbot certonly --nginx -d sigma-se.com -m s-hama@sigma-se.jp
  ```

## 起動確認
- PostgreSQLの再起動
  ```
  systemctl restart postgresql
  ```
- Nginxの再起動
  ```
  sudo systemctl restart nginx
  ```
- uWSGIの起動
  ※ 一般ユーザー(vpsuser)で実行する
  ```
  source /var/www/venvs/sweb/bin/activate
  uwsgi --ini /var/www/projs/sweb/config/uwsgi.ini
  ```
- ブラウザから起動確認
  ```
  http://sigma-se.com/
  ```
  `/var/www/html`が表示されればOK
