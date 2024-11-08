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

### DocumentRootの権限変更
- vpsuser(所有者グループ)やapache(所有者)でもDocumentRoot配下(/var/www/html) が編集できるように権限変更する。
  ```
  $ cd /var/www
  $ chown apache:vpsuser html 
  $ chmod 775 html
  ```

- 仮のindexで表示確認<br>
/var/www/htmlの直下にindex.htmlを新規作成後、httpで自身のドメイン(http://example.com)にアクセスし表示されれば設定成功。
  ```
  $ systemctl list-unit-files -t service
  ```

### httpsの解放設定
- httpsのサービス解放<br>
「--permanent」でOSを再起動しても設定が変わらないように設定を恒久化する。
「--zone=public」で明示的にzoneをpublicに割当てる。<br>
  ```
  $ firewall-cmd --permanent --zone=public --add-service=https
  ```

- 設定を反映させるためfirewalldを再起動する
  ```
  $ systemctl restart firewalld
  ```

- httpsの解放確認<br>
servicesにhttpsと表示されれば解放成功。
  ```
  $ firewall-cmd --list-all
   public (active)
    target: default
    icmp-block-inversion: no
    interfaces: eth0
    sources:
    services: dhcpv6-client ssh http https
    ports:
    protocols:
    masquerade: no
    forward-ports:
    source-ports:
    icmp-blocks:
    rich rules:
  ```

### SSL/TLS証明書設定
ここでは、SSL/TLS証明書が無料取得できる`Let's Encrypt`を使用する。
以降、Certbot をインストールし、SSL/TLS証明書を取得して定期更新まで実施する。

- mod_sslインストール<br>
`Apache`を`SSL/TLS`に対応させる。
  ```
  $ yum install mod_ssl # mod_sslインストール
  ```