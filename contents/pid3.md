## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：3/4 Python・Django・mod_wsgi設定

## 概要

VPS上にPython、Django、mod_wsgiを導入し、ApacheからDjangoアプリケーションを起動するための設定を整理する。

Djangoを本番環境で動かす場合、開発用のrunserverではなく、ApacheなどのWebサーバーからWSGI経由でアプリケーションを呼び出す構成を理解することが重要になる。

## 前提環境

| 項目 | 内容 |
| --- | --- |
| OS | CentOS 7.4 |
| 言語 | Python |
| Webサーバー | Apache |
| フレームワーク | Django |
| データベース | PostgreSQL |
| ドメイン | example.com |

## この記事で扱うこと
- EPEL/IUSリポジトリの導入意図。
- Pythonとvenvによる仮想環境の作成。
- Djangoプロジェクトとアプリケーションの作成。
- mod_wsgiを使ってApacheとDjangoを接続する流れ。
- VirtualHostとWSGI設定の役割。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| Python環境 | 利用するPythonバージョンと仮想環境の場所を決める。 |
| Django構成 | プロジェクト名、アプリケーション名、配置ディレクトリを整理する。 |
| Apache設定 | conf.modules.d と conf.d の読み込み関係を確認する。 |
| mod_wsgi | Pythonバージョンに合ったモジュールパスを確認する。 |
| HTTPS設定 | 前段のSSL/TLS設定とVirtualHostの関係を確認する。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| venvとシステムPython | どちらにDjangoやmod_wsgiを入れたかを混同しない。 |
| WSGIファイルパス | wsgi.pyとmod_wsgiモジュールのパスを取り違えやすい。 |
| 静的ファイル | DjangoアプリのstaticとApacheのAlias設定を対応させる。 |
| VirtualHost | 80番はHTTPSリダイレクト、443番はDjango起動という役割を分ける。 |

## 実施内容
### CentOSにパッケージリポジトリを導入
- 開発パッケージのインストール<br>
EPELリポジトリを有効化する。<br>
※ EPELはCentOSやRHELにない便利なパッケージを提供する外部リポジトリ。
  ```bash
  $ yum -y install epel-release
  ```

- IUSリポジトリの追加<br>
Pythonの最新アップストリームバージョンを提供するリポジトリ。<br>
IUSリポジトリ経由 でPythonの最新バージョンをインストールできるようにする。<br>
  ```bash
  $ yum -y install https://centos7.iuscommunity.org/ius-release.rpm
  ```

### Pythonインストール
- Python3.6のインストール<br>
`python36u`、`python36u-devel`をインストールする。<br>
  ```bash
  $ yum -y install python36u
  $ yum -y install python36u-pip python36u-devel
  ```

- バージョン確認<br>
  ```bash
  $ python3.6 -V
  Python 3.6.4
  ```

### Djangoインストール
- venvで仮想環境を構築<br>
Pythonの仮想環境を作成するパッケージは、他にも**virtualenv**、**anaconda**、**pyenv**、**pyenv-virtualenv**など多数あるが、ここでは、Python3から標準搭載されている**venv**を使用する。<br>
<br>
※ `vops`は、仮想環境が入るディレクトリ名なので各自の環境に合わせること。
  ```bash
  $ python3.6 -m venv /var/www/vops
  ```

- 仮想環境上にDjangoをインストール<br>
`pip`で**Django**をインストールする。
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ pip install django    # djangoインストール
  ```

- Djangoプロジェクトの雛形作成<br>
※ `ops`は、プロジェクト名なので、各自の環境に合わせること。
  ```bash
  $ django-admin startproject /var/www/vops/ops
  ```

### アプリケーション作成
- 実際にプログラムの成果物を配置することになるアプリケーションを作成
※ ここでは、**macuos**という名称のアプリケーションを作成する。
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ python manage.py startapp /var/www/vops/ops/macuos    # アプリケーションを作成
  ```

### mod_wsgiインストール
- `httpd-devel`と`mod_wsgi`をインストール
Python3上では事前に`httpd-devel`をインストールする必要があるため、`mod_wsgi`の前に `httpd-devel`をインストールする。<br>
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ yum install -y httpd httpd-devel    # httpd-develをインストール
  $ pip3.6 install mod_wsgi    # pipでmod_wsgiをインストール
  ```

### WSGIと仮想ホストの設定ファイル作成
- Apache設定ファイルの確認<br>
Apacheの設定ファイル**httpd.conf**の設定内容を確認する。<br>
  ```bash
  $ cat /etc/httpd/conf/httpd.conf
  …
  Include conf.modules.d/*.conf  
  IncludeOptional conf.d/*.conf 
  …
  ```
  - 補足<br>
上記`Include`は、`conf.modules.d`(module系の設定ファイル)配下の`*.conf`をロードする設定、`IncludeOptional`は、`conf.d`(その他設定系のファイル)配下の`*.conf`をロードする設定となる。<br><br>
そのため、次項で**WSGI設定ファイル(django-wsgi.conf)**と**仮想ホスト設定ファイル(django.conf)**を作成し、Apacheからmod_wsgiを介し、Djangoを起動できるよう、wsgi_module設定ファイルを作成する。<br>

- WSGI設定ファイル作成<br>
`/etc/httpd/conf.modules.d`配下に下記の内容で**django-wsgi.conf**を作成する。<br>
  ```bash
  LoadModule wsgi_module  /var/www/vops/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so
  ```
  - 補足<br>
※ wsgi_moduleのファイルパスは、findで確認。<br>
    ```bash
    $ find /var/www -name 'mod_*.so'
    ```

- 仮想ホスト設定ファイル作成<br>
`/etc/httpd/conf.d`配下に下記の内容で**django.conf**を作成する。<br>
  ```apache
  NameVirtualHost *:80
  NameVirtualHost *:443
  WSGISocketPrefix run/wsgi

  <VirtualHost *:443>… (※1)
      ServerName example.com … (※2)
      SSLEngine On … (※3)
      SSLCertificateFile /etc/letsencrypt/live/example.com/cert.pem … (※4)
      SSLCertificateKeyFile  /etc/letsencrypt/live/example.com/privkey.pem … (※4)

      WSGIDaemonProcess example.com processes=2 threads=15 python-home=/var/www/vops python-path=/var/www/vops/lib64/python3.6/site-packages … (※5)
      WSGIProcessGroup example.com … (※6)
      WSGIScriptAlias / /var/www/vops/ops/ops/wsgi.py … (※7)

      Alias /static /var/www/vops/ops/macuos/static … (※8)
      <Directory /var/www/vops/ops/macuos/static> 
          Require all granted
      </Directory>

      <Directory /var/www/vops/ops/ops> … (※9)
          <Files wsgi.py>
              Require all granted
          </Files>
      </Directory>
  </VirtualHost>
  <VirtualHost *:80>… (※10)
      ServerName example.com
      RewriteEngine on
      RewriteCond %{HTTPS} off
      RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [R=301,L]
  </VirtualHost>
  ```
  - 上記注釈<br>
  ※1 SSL/TLSポートのVirtualHost。<br>
  ※2 ServerName：自身のドメイン、サブドメイン、IP等を設定。<br>
  ※3 SSLEngine：SSL/TLSエンジンの有効化。<br>
  ※4 SSL/TLSサーバー証明書と秘密鍵の設定。Apache2.4では、上記のSSLCertificateFile、SSLCertificateKeyFileの設定になるが、Apache2.2だとSSLCertificateFile、SSLCertificateKeyFile、SSLCertificateChainFileの3つに設定が必要でさらに内容も若干違うため、バージョンが古い場合は、注意が必要。<br>
  ※5 マルチプロセスかつ、デーモンモードでの起動設定。<br>
  ※6 WSGIDaemonProcessと同じ、example.comを設定する必要あり。<br>
  ※7 wsgi.pyエイリアスと起動直後のトップ画面をhttps://example.comで表示したい場合の設定。 例えば、トップ画面から"XXX"というサブフォルダを掘りたい場合は、WSGIScriptAliasの第一パラメータに"/XXX"を指定する。<br>
  ※8 静的ファイルへの（アイコンや画像など）エイリアスを設定 及び、静的フォルダまでのパスを設定。<br>
  ※9 wsgi.pyまでのパスを設定。(起動直後にwsgi.pyを実行するよに設定)<br>
  ※10 httpデフォルトの80ポートのVirtualHost。httpsにリダイレクトするように設定。<br>

## 実務とのつながり
- WSGI構成<br>
    Djangoを本番Webサーバーで動かす基本構成の理解につながる。
- 仮想環境<br>
    プロジェクトごとに依存関係を分離する実務上の基本になる。
- Apache設定分割<br>
    設定ファイルを役割ごとに分けると、保守や障害調査がしやすくなる。

## まとめ
- Django本番構成では、Apacheからmod_wsgiを介してアプリケーションを起動する。
- Pythonの仮想環境、Djangoプロジェクト、WSGI設定のパスをそろえることが重要となる。
- VirtualHostではHTTPからHTTPSへのリダイレクトとDjango起動設定を分けて考える。
