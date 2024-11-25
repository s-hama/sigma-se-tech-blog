## タイトル
VPSで作るDjangoサイト構築手順 - Apache編 : 3/4 Django環境とサーバー設定のセットアップ

## 目的
この記事では、以下のVPS環境でDjangoサイトを構築するために必要な「Django環境とサーバー設定のセットアップ手順」について説明する。
- OS：CentOS 7,4
- 言語：Python
- WEBサーバー：Apache
- FW：Django
- DB：PostgresSQL
- ドメイン：example.com

## 実施内容
### CentOSにパッケージリポジトリを導入
- 開発パッケージのインストール<br>
EPELリポジトリを有効化する。<br>
※ EPELはCentOSやRHELにない便利なパッケージを提供する外部リポジトリ。
  ```
  $ yum -y install epel-release
  ```

- IUSリポジトリの追加<br>
Pythonの最新アップストリームバージョンを提供するリポジトリ。<br>
IUSリポジトリ経由 でPythonの最新バージョンをインストールできるようにする。<br>
  ```
  $ yum -y install https://centos7.iuscommunity.org/ius-release.rpm
  ```

### Pythonインストール
- Python3.6のインストール<br>
`python36u`、`python36u-devel`をインストールする。<br>
  ```
  $ yum -y install python36u
  $ yum -y install python36u-pip python36u-devel
  ```

- バージョン確認<br>
  ```
  $ python3.6 -V
  Python 3.6.4
  ```

### Djangoインストール
- venvで仮想環境を構築<br>
Pythonの仮想環境を作成するパッケージは、他にも`virtualenv`、`anaconda`、`pyenv`、`pyenv-virtualenv`など多数あるが、ここでは、Python3から標準搭載されている`venv`を使用する。<br>
<br>
※ `vops`は、仮想環境が入るディレクトリ名なので各自の環境に合わせること。
  ```
  $ python3.6 -m venv /var/www/vops
  ```

- 仮想環境上にDjangoをインストール<br>
`pip`で`Django`をインストールする。
  ```
  $ source /var/www/vops/bin/activate # 仮想環境起動
  $ pip install django # djangoインストール
  ```

- Djangoプロジェクトの雛形作成<br>
※ `ops`は、プロジェクト名なので、各自の環境に合わせること。
  ```
  $ django-admin startproject /var/www/vops/ops
  ```

### アプリケーション作成
実際にプログラムの成果物を配置することになるアプリケーションを作成する。
※ ここでは、`macuos`という名称のアプリケーションを作成する。
  ```
  $ source /var/www/vops/bin/activate    # 仮想環境起動
  $ python manage.py startapp /var/www/vops/ops/macuos    # アプリケーションを作成
  ```

### mod_wsgiインストール
Python3上では事前に`httpd-devel`をインストールする必要があるため、`mod_wsgi`の前に `httpd-devel`をインストールする。<br>
  ```
  $ source /var/www/vops/bin/activate # 仮想環境起動
  $ yum install -y httpd httpd-devel # httpd-develをインストール
  $ pip3.6 install mod_wsgi # pipでmod_wsgiをインストール
  ```

### WSGIと仮想ホストの設定ファイル作成
- Apache設定ファイルの確認<br>
Apacheの設定ファイル`httpd.conf`の設定内容を確認する。<br>
  ```
  $ cat /etc/httpd/conf/httpd.conf
  …
  Include conf.modules.d/*.conf  
  IncludeOptional conf.d/*.conf 
  …
  ```
上記`Include`は、`conf.modules.d`(module系の設定ファイル)配下の`*.conf`をロードする設定、`IncludeOptional`は、`conf.d`(その他設定系のファイル)配下の`*.conf`をロードする設定となる。<br>
<br>
そのため、次項で`WSGI設定ファイル`(django-wsgi.conf)と`仮想ホスト設定ファイル`(django.conf)を作成し、Apacheからmod_wsgiを介し、Djangoを起動できるよう、wsgi_module設定ファイルを作成する。<br>

- WSGI設定ファイル作成<br>
`/etc/httpd/conf.modules.d`配下に下記の内容で`django-wsgi.conf`を作成する。<br>
  ```
  LoadModule wsgi_module  /var/www/vops/lib64/python3.6/site-packages/mod_wsgi/server/mod_wsgi-py36.cpython-36m-x86_64-linux-gnu.so
  ```
※ wsgi_moduleのファイルパスは、findで確認。<br>
  ```
  $ find /var/www -name 'mod_*.so'
  ```
