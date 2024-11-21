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
