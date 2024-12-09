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
