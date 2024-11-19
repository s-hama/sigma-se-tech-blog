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
