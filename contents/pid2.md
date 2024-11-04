## タイトル
VPSで作るDjangoサイト構築手順 - Apache編 : 1/4 Apache&SSL/TLSの初期設定

## 目的
この記事では、以下のVPS環境でDjangoサイトを構築するために必要な「ApacheとSSL/TLSの初期設定手順」を説明する。
- OS：CentOS 7,4
- 言語：Python
- WEBサーバー：Apache
- FW：Django
- DB：PostgresSQL
- ドメイン：example.com

## 実施内容
### Apache(httpd)インストール
- インストール実行後、`Complete!`で正常終了。
  ```
  $ yum install httpd
  ```

### ファイアウォールの設定
- CentOS7は、デフォルトでファイアウォールが有効なため、http、httpsも遮断されている状態なのでこの通信を許容するように設定変更する。<br>
後にSSL/TSL化するため、ここでhttpsも一緒に許容しておく。
  ```
  $ systemctl start httpd # Apacheの起動
  $ firewall-cmd --add-service=http --zone=public --permanent # http通信の許容
  $ firewall-cmd --add-service=https --zone=public --permanent # https通信の許容
  $ systemctl restart firewalld # ファイアウォールの再起動
  ```

- httpでの接続確認<br>
httpで自身のドメイン(http://example.com)にアクセスし、`Testing 123`と表示されれば設定成功。

### httpd自動起動の設定
- サーバー起動時にhttpdも自動で起動するように設定する。
  ```
  $ systemctl enable httpd
  ```
- 自動起動の設定確認<br>
`httpd.service enabled`と表示されれば設定成功。
  ```
  $ systemctl list-unit-files -t service
  ```
