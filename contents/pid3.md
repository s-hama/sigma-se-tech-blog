## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：3/4 Python・Django・mod_wsgi設定

## 概要

VPS上にPython、Django、mod_wsgiを導入し、ApacheからDjangoアプリケーションを起動するための設定を整理する。

Djangoを本番環境で動かす場合、開発用のrunserverではなく、ApacheなどのWebサーバーからWSGI経由でアプリケーションを呼び出す構成を理解することが重要になる。

※ 注意：この記事は、2018年当時のCentOS 7.4、Python 3.6環境の構築記録をもとに、手順同士の互換性を確認しやすい後年の旧バージョン（Django 2.2、mod_wsgi 4.9.4）へ置き換えて再構成した例である。<br>2018年当時のパッケージ構成を厳密に再現するものではない。<br>CentOS 7、Python 3.6、ここで扱うDjangoとmod_wsgiはいずれもサポート終了済みで、IUSリポジトリも現在の新規構築には使用できない。<br>新規構築ではサポート中の環境を選び、ここではApacheとmod_wsgiを接続する考え方を中心に参照する。

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
PostgreSQL
- ドメイン<br>
example.com

## この記事で扱うこと
- EPEL/IUSリポジトリを利用していた当時の背景。
- Pythonとvenvによる仮想環境の作成。
- Djangoプロジェクトとアプリケーションの作成。
- mod_wsgiを使ってApacheとDjangoを接続する流れ。
- VirtualHostとWSGI設定の役割。

## 作業時の注意点

- venvとシステムPython<br>
どちらにDjangoやmod_wsgiを入れたかを混同しない。
- WSGIファイルパス<br>
wsgi.pyとmod_wsgiモジュールのパスを取り違えやすい。
- 静的ファイル<br>
DjangoアプリのstaticとApacheのAlias設定を対応させる。
- VirtualHost<br>
80番はHTTPSリダイレクト、443番はDjango起動という役割を分ける。

## 実施内容
### CentOSにパッケージリポジトリを導入
- 開発パッケージのインストール<br>
EPELリポジトリを有効化する。<br>
※ EPELはCentOSやRHELにない便利なパッケージを提供する外部リポジトリ。
  ```bash
  $ yum -y install epel-release
  ```

- IUSリポジトリの追加<br>
当時は、CentOS標準より新しいPythonを導入するためにIUSリポジトリを利用していた。次のURLとパッケージは現在の新規構築には利用せず、履歴として示す。<br>
  ```bash
  # 旧環境で使用していた例（現在は実行しない）
  $ yum install https://centos7.iuscommunity.org/ius-release.rpm
  ```

### Pythonインストール
- Python3.6のインストール<br>
旧IUS環境では`python36u`、`python36u-devel`をインストールしていた。以下も再現用の履歴であり、現在の構築手順ではない。<br>
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
`pip`で**Django**をインストールする。無指定で最新版を入れるとPython 3.6では動作しないため、この旧環境を再現する場合は対応するバージョンへ固定する。Django 2.2自体もサポート終了済みである。
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ python -m pip install "Django==2.2.*"
  ```

- Djangoプロジェクトの雛形作成<br>
※ `ops`は、プロジェクト名なので、各自の環境に合わせること。
  ```bash
  $ mkdir -p /var/www/vops/ops
  $ django-admin startproject ops /var/www/vops/ops
  ```

### アプリケーション作成
- 実際にプログラムを配置するDjangoアプリケーションを作成する。<br>
※ ここでは、例として**webapp**という名称にする。
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ cd /var/www/vops/ops
  $ python manage.py startapp webapp
  ```

### mod_wsgiインストール
- `httpd-devel`、Cコンパイラ、`mod_wsgi`をインストール
`mod_wsgi`をソースからビルドするため、Apacheの開発ファイル`httpd-devel`とCコンパイラ`gcc`を先にインストールする。Pythonの開発ファイルは前述の`python36u-devel`で導入済みとなる。<br>
  ```bash
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ yum install -y httpd httpd-devel gcc    # mod_wsgiのビルドに必要な開発環境をインストール
  $ python -m pip install "mod_wsgi==4.9.4"    # Python 3.6対応版へ固定
  ```
  mod_wsgiはビルド時に使用したPythonへ結び付くため、仮想環境とmod_wsgiのPython実装・バージョンを一致させる。

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
`mod_wsgi-express module-config`で、現在の環境に対応する`LoadModule`と`WSGIPythonHome`を確認する。ハードコードした共有ライブラリ名はPythonやCPUアーキテクチャによって変わるため、コマンドの出力を`/etc/httpd/conf.modules.d/django-wsgi.conf`へ反映する。<br>
  ```bash
  $ /var/www/vops/bin/mod_wsgi-express module-config
  LoadModule wsgi_module "/var/www/vops/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so"
  WSGIPythonHome "/var/www/vops"
  ```

- 仮想ホスト設定ファイル作成<br>
前記事で`certbot --apache`を実行した場合は、Certbotが同じ`ServerName`のVirtualHostを生成または編集していることがある。<br>
`httpd -S`で現在の定義を確認し、同じホスト名・ポートのVirtualHostを重複作成せず、既存のHTTPS用設定へWSGIと静的ファイルの設定を統合する。<br>
該当する定義がない場合は、`/etc/httpd/conf.d`配下に**django.conf**を作成する。<br>
以下は一つに統合した設定例であり、記号を含まないApache設定として記述している。<br>
  ```apache
  <VirtualHost *:443>
      ServerName example.com
      SSLEngine On
      SSLCertificateFile /etc/letsencrypt/live/example.com/cert.pem
      SSLCertificateChainFile /etc/letsencrypt/live/example.com/chain.pem
      SSLCertificateKeyFile /etc/letsencrypt/live/example.com/privkey.pem

      WSGIDaemonProcess example.com processes=2 threads=15 python-home=/var/www/vops python-path=/var/www/vops/ops
      WSGIProcessGroup example.com
      WSGIScriptAlias / /var/www/vops/ops/ops/wsgi.py

      Alias /static/ /var/www/vops/ops/static/
      <Directory /var/www/vops/ops/static>
          Require all granted
      </Directory>

      <Directory /var/www/vops/ops/ops>
          <Files wsgi.py>
              Require all granted
          </Files>
      </Directory>
  </VirtualHost>
  <VirtualHost *:80>
      ServerName example.com
      Redirect permanent / https://example.com/
  </VirtualHost>
  ```
  - 設定項目の補足<br>
  `<VirtualHost *:443>`はSSL/TLS用、`<VirtualHost *:80>`はHTTPからHTTPSへのリダイレクト用となる。`ServerName`には自身のドメインを設定する。<br><br>
  証明書設定はCentOS 7.4標準のApache 2.4.6を前提に、`cert.pem`と`chain.pem`を別々に指定している。Apache 2.4.8以降では`SSLCertificateFile`に`fullchain.pem`を指定し、`SSLCertificateChainFile`は省略できる。`httpd -v`でバージョンを確認し、Certbotが生成した設定を優先する。秘密鍵の読取り権限は必要最小限にする。<br><br>
  `WSGIDaemonProcess`の`python-home`は仮想環境のルート、`python-path`はDjangoプロジェクトをimportできるディレクトリを指定する。`WSGIProcessGroup`には同じプロセスグループ名を設定し、`WSGIScriptAlias`には`wsgi.py`へのパスを指定する。<br><br>
  `Alias /static/`は`collectstatic`で`STATIC_ROOT`へ集約した静的ファイルを配信する設定で、URLとファイルパスの末尾の`/`を対応させる。<br>

## まとめ
- Django本番構成では、Apacheからmod_wsgiを介してアプリケーションを起動する。
- Pythonの仮想環境、Djangoプロジェクト、WSGI設定のパスをそろえることが重要となる。
- VirtualHostではHTTPからHTTPSへのリダイレクトとDjango起動設定を分けて考える。

### 参考文献
- [The CentOS Project, CentOS Linux（CentOS Linux 7のEOL）](https://www.centos.org/centos-linux/)
- [Python Documentation, venv — Creation of virtual environments](https://docs.python.org/3/library/venv.html)
- [Django Documentation, How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/modwsgi/)
- [Django 2.2 Documentation, How to use Django with Apache and mod_wsgi](https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/modwsgi/)
- [mod_wsgi Documentation, Virtual Environments](https://modwsgi.readthedocs.io/en/develop/user-guides/virtual-environments.html)
- [Apache HTTP Server 2.4, Virtual Host Documentation](https://httpd.apache.org/docs/2.4/vhosts/)
- [Apache HTTP Server 2.4, mod_ssl：SSLCertificateFileとSSLCertificateChainFile](https://httpd.apache.org/docs/2.4/mod/mod_ssl.html)
