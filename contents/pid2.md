## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：2/4 Apache・SSL/TLS初期設定

## 概要

VPS上でApacheを起動し、HTTP/HTTPS通信を許可し、Let's EncryptでSSL/TLS証明書を取得する流れを整理する。

Webサイトを公開するには、Webサーバーの起動だけでなく、firewalld、DocumentRoot、HTTPS、証明書更新までつなげて確認する必要がある。特にSSL/TLSは、一度取得して終わりではなく、期限管理まで含めて運用する。

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
- Apacheのインストールと起動確認。
- HTTP/HTTPSをfirewalldで許可する手順。
- DocumentRootの権限設定。
- mod_sslとCertbotによるSSL/TLS証明書取得。
- Let's Encrypt証明書の更新確認。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| Apache | httpdをインストールし、サービスとして起動できる状態にする。 |
| firewalld | httpとhttpsの通信を恒久的に許可する。 |
| DocumentRoot | 配置先ディレクトリの所有者と権限を確認する。 |
| ドメイン | 証明書取得前にDNSがVPSへ向いている必要がある。 |
| 証明書更新 | Let's Encryptの期限と更新手順を確認する。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| HTTPとHTTPS | 80番ポートと443番ポートは別々に許可が必要になる。 |
| --permanent | 付けない設定は再起動後に消えることがある。 |
| 証明書取得失敗 | DNS未反映やApache起動中のポート競合を確認する。 |
| 自動更新 | 証明書の取得だけでなく、更新確認まで運用に含める。 |

## 実施内容
### Apache(httpd)インストール
- インストール実行後、`Complete!`で正常終了。
  ```bash
  $ yum install httpd
  ```

### ファイアウォールの設定
- CentOS7は、デフォルトでファイアウォールが有効なため、http、httpsも遮断されている状態なのでこの通信を許容するように設定変更する。<br>
後にSSL/TSL化するため、ここでhttpsも一緒に許容しておく。
  ```bash
  $ systemctl start httpd    # Apacheの起動
  $ firewall-cmd --add-service=http --zone=public --permanent    # http通信の許容
  $ firewall-cmd --add-service=https --zone=public --permanent    # https通信の許容
  $ systemctl restart firewalld    # ファイアウォールの再起動
  ```

- httpでの接続確認<br>
httpで自身のドメイン(http://example.com)にアクセスし、`Testing 123`と表示されれば設定成功。

### httpd自動起動の設定
- サーバー起動時にhttpdも自動で起動するように設定する。
  ```bash
  $ systemctl enable httpd
  ```
- 自動起動の設定確認<br>
`httpd.service enabled`と表示されれば設定成功。
  ```bash
  $ systemctl list-unit-files -t service
  ```

### DocumentRootの権限変更
- vpsuser(所有者グループ)やapache(所有者)でもDocumentRoot配下(/var/www/html) が編集できるように権限変更する。
  ```bash
  $ cd /var/www
  $ chown apache:vpsuser html 
  $ chmod 775 html
  ```

- 仮のindexで表示確認<br>
/var/www/htmlの直下にindex.htmlを新規作成後、httpで自身のドメイン(http://example.com)にアクセスし表示されれば設定成功。
  ```bash
  $ systemctl list-unit-files -t service
  ```

### httpsの解放設定
- httpsのサービス解放<br>
「--permanent」でOSを再起動しても設定が変わらないように設定を恒久化する。
「--zone=public」で明示的にzoneをpublicに割当てる。<br>
  ```bash
  $ firewall-cmd --permanent --zone=public --add-service=https
  ```

- 設定を反映させるためfirewalldを再起動する
  ```bash
  $ systemctl restart firewalld
  ```

- httpsの解放確認<br>
servicesにhttpsと表示されれば解放成功。
  ```bash
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
ここでは、SSL/TLS証明書が無料取得できる**Let's Encrypt**を使用する。<br>
以降、Certbot をインストールし、SSL/TLS証明書を取得して定期更新まで実施する。

- mod_sslインストール<br>
**Apache**を**SSL/TLS**に対応させる。
  ```bash
  $ yum install mod_ssl    # mod_sslインストール
  ```

- 起動確認
`active(running)`であることを確認する。<br>
  ```bash
  $ systemctl restart httpd
  $ systemctl status httpd
  * httpd.service - The Apache HTTP Server
     Loaded: loaded (/usr/lib/systemd/system/httpd.service; enabled; vendor preset: disabled)
     Active: active (running) since Fri 2018-09-14 21:54:42 JST; 1h 40min ago
       Docs: man:httpd(8)
             man:apachectl(8)
    Process: 3887 ExecStop=/bin/kill -WINCH ${MAINPID} (code=exited, status=0/SUCCESS)
    Process: 24271 ExecReload=/usr/sbin/httpd $OPTIONS -k graceful (code=exited, status=0/SUCCESS)
   Main PID: 3895 (httpd)
     Status: "Total requests: 49; Current requests/sec: 0; Current traffic:   0 B/sec"
     CGroup: /system.slice/httpd.service
             |-3895 /usr/sbin/httpd -DFOREGROUND
             |-3896 /usr/sbin/httpd -DFOREGROUND
             |-3897 /usr/sbin/httpd -DFOREGROUND
             |-3898 /usr/sbin/httpd -DFOREGROUND
             |-3899 /usr/sbin/httpd -DFOREGROUND
             |-3900 /usr/sbin/httpd -DFOREGROUND
             |-3902 /usr/sbin/httpd -DFOREGROUND
             |-3903 /usr/sbin/httpd -DFOREGROUND
             |-3979 /usr/sbin/httpd -DFOREGROUND
             |-3982 /usr/sbin/httpd -DFOREGROUND
             |-3995 /usr/sbin/httpd -DFOREGROUND
             |-3996 /usr/sbin/httpd -DFOREGROUND
             |-4089 /usr/sbin/httpd -DFOREGROUND
             `-4536 /usr/sbin/httpd -DFOREGROUND
  ```

- EPELリポジトリのインストール<br>
**EPEL**は、CentOSで標準搭載されていないパッケージをyumでインストール可能にするためのリポジトリ。
  ```bash
  $ yum install epel-release
  ```

- Certbotのインストール<br>
**Certbot**は、**Let's Encrypt**で使用するクライアントソフトウェアで、SSL/TLSサーバー証明書の取得、及び更新作業を自動化してくれる。
  ```bash
  $ yum install epel-release
  ```

- CertbotでSSL証明書を取得する
  ```bash
  $ sudo certbot --authenticator standalone --installer apache -d example.com --pre-hook "apachectl stop" --post-hook "apachectl start"
  ```

- SSL/TLSの動作確認<br>
httpsで自身のドメイン(https://example.com)にアクセスできれば成功。<br>
※ httpでアクセスしてもhttpsにリダイレクトされる。

### Let's Encryptの定期更新
3か月単位で定期的な証明書の再発行が必要。
期限が近づくと**Let's Encrypt certificate expiration notice for domain "example.com"**というメールが送られてくるため、期限以内に**certbot**から証明書を再発行する必要がある。

- Apacheを停止して現在の証明書を強制的に再発行する。
  ```bash
  $ sudo systemctl stop httpd    # Apache停止
  $ sudo certbot renew --force-renewal --dry-run    # 仮実施
  $ openssl x509 -in /etc/letsencrypt/live/example.com/fullchain.pem -noout -dates    # 有効期限の確認
  $ sudo certbot renew --force-renewal    # 本番実施：証明書再発行
  $ sudo systemctl start httpd    # Apache起動
  ```

- 有効期限の確認<br>
ブラウザの証明書情報の有効期限が**3か月**伸びていれば再発行成功。

## 実務とのつながり
- HTTPS化<br>
    ログイン情報や管理画面を扱うサイトでは基本的な保護になる。
- firewalld<br>
    公開するポートを必要最小限にする考え方につながる。
- 証明書更新<br>
    期限切れによるサイト停止を防ぐため、監視や定期確認が重要になる。

## まとめ
- Apacheを公開するには、httpd、firewalld、DocumentRootをまとめて確認する。
- HTTPS化では、mod_sslとSSL/TLS証明書の設定が必要になる。
- Let's Encryptは更新が必要なため、取得後の期限確認も運用に含める。
