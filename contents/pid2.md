## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：2/4 Apache・SSL/TLS初期設定

## 概要

VPS上でApacheを起動し、HTTP/HTTPS通信を許可し、Let's EncryptでSSL/TLS証明書を取得する流れを整理する。

Webサイトを公開するには、Webサーバーの起動だけでなく、firewalld、DocumentRoot、HTTPS、証明書更新までつなげて確認する必要がある。特にSSL/TLSは、一度取得して終わりではなく、期限管理まで含めて運用する。

※ 注意：この記事は、2018年当時のCentOS 7.4環境をもとにした構築記録である。<br>
CentOS 7は2024年6月30日にサポートを終了しているため、新規構築ではサポート中のOSと、そのOS向けにCertbot公式サイトが案内する手順を利用する。

## 前提環境

| 項目 | 内容 |
| --- | --- |
| OS | CentOS 7.4（サポート終了済み） |
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

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| HTTPとHTTPS | 80番ポートと443番ポートは別々に許可が必要になる。 |
| --permanent | 付けない設定は再起動後に消えることがある。 |
| 証明書取得失敗 | DNS未反映やApache起動中のポート競合を確認する。 |
| 自動更新 | 証明書の取得だけでなく、更新確認まで運用に含める。 |

## 実施内容
### Apache(httpd)インストール
- インストール後、Apacheを起動し、OS起動時にも自動起動するよう設定
  ```bash
  $ yum install httpd
  $ systemctl start httpd
  $ systemctl enable httpd
  ```

### ファイアウォールの設定
- `firewalld`でHTTPとHTTPSのサービスを恒久的に許可し、設定を再読込み<br>
後にSSL/TLS化するため、ここでHTTPSも一緒に許可しておく。
  ```bash
  $ firewall-cmd --zone=public --add-service=http --permanent
  $ firewall-cmd --zone=public --add-service=https --permanent
  $ firewall-cmd --reload
  $ firewall-cmd --zone=public --list-services
  ```

- httpでの接続確認<br>
httpで自身のドメイン(http://example.com)にアクセスし、`Testing 123`と表示されれば設定成功。

### httpd自動起動の確認
- インストール時に有効化した自<br>
`enabled`と表示されれば、OS起動時にhttpdも起動する。
  ```bash
  $ systemctl is-enabled httpd
  ```

### DocumentRootの権限変更
- 配置作業を行う`vpsuser`を所有者、Apacheをグループに設定
<br>静的ファイルを配信するだけならApacheに書込み権限は不要なので、DocumentRoot全体を`775`にはしない。
  ```bash
  $ cd /var/www
  $ chown vpsuser:apache html
  $ chmod 755 html
  ```

- 仮の`index.html`を`/var/www/html`直下へ配置した後、HTTPレスポンスを確認<br>
  ```bash
  $ curl -I http://example.com/
  ```

### HTTPS用ポートの確認
- `services`に`http`と`https`が表示されることを確認<br>
すでに「ファイアウォールの設定」で追加しているため、ここで同じ設定を重複して実行する必要はない。
  ```bash
  $ firewall-cmd --zone=public --list-all
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
`active (running)`であることを確認する。長いプロセス一覧を転載するより、サービス状態と設定構文を確認する方が切り分けやすい。
  ```bash
  $ apachectl configtest
  $ systemctl restart httpd
  $ systemctl status httpd
  ```

- EPELリポジトリのインストール<br>
**EPEL**は、CentOSで標準搭載されていないパッケージをyumでインストール可能にするためのリポジトリ。
  ```bash
  $ yum install epel-release
  ```

- Certbotのインストール<br>
**Certbot**は、**Let's Encrypt**で使用するクライアントソフトウェアで、SSL/TLSサーバー証明書の取得、及び更新作業を自動化してくれる。
  ```bash
  $ yum install certbot python2-certbot-apache
  ```
  ※ 上記はCentOS 7当時のパッケージ名である。現在はCertbot公式のインストール手順で、利用中のOSとWebサーバーを選択して確認する。

- CertbotでSSL証明書を取得する
  ```bash
  $ sudo certbot --apache -d example.com
  ```

- SSL/TLSの動作確認<br>
HTTPSで自身のドメイン（https://example.com）にアクセスできれば成功。<br>
※ HTTPからHTTPSへのリダイレクトは、Certbot実行時にリダイレクトを選択した場合、またはApache側で別途設定した場合に有効になる。

### Let's Encryptの定期更新
Let's Encryptの`classic`プロファイルで発行される既定の証明書有効期間は現在90日であり、期限前に自動更新できる状態を維持する必要がある。<br>
短期証明書のプロファイルや段階的な有効期間短縮も案内されているため、「3か月ごと」の固定スケジュールではなくCertbotの更新判定に任せる。<br>
Let's Encryptによる期限通知メールは2025年6月4日に終了したため、メールを更新確認の代わりにはできない。

- インストール方法に応じてsystemd timerまたはcronの自動更新設定を確認し、`--dry-run`で更新をテストする。通常の更新では、期限が近い証明書だけを対象とする`certbot renew`を使い、`--force-renewal`は常用しない。
  ```bash
  $ systemctl list-timers --all | grep certbot
  $ sudo certbot renew --dry-run
  $ sudo certbot renew
  $ openssl x509 -in /etc/letsencrypt/live/example.com/fullchain.pem -noout -dates
  ```

- 有効期限の確認<br>
`certbot renew --dry-run`が成功することに加え、外部監視や定期的な証明書確認を用意して更新失敗を検知する。

## まとめ
- Apacheを公開するには、httpd、firewalld、DocumentRootをまとめて確認する。
- HTTPS化では、mod_sslとSSL/TLS証明書の設定が必要になる。
- Let's Encryptは更新が必要なため、取得後の期限確認も運用に含める。

### 参考文献
- [The CentOS Project, CentOS Linux（CentOS Linux 7のEOL）](https://www.centos.org/centos-linux/)
- [Red Hat Enterprise Linux 7 Security Guide, Controlling Traffic](https://docs.redhat.com/en/documentation/red_hat_enterprise_linux/7/html/security_guide/sec-controlling_traffic)
- [Apache HTTP Server 2.4, SSL/TLS Encryption](https://httpd.apache.org/docs/2.4/ssl/)
- [Certbot Documentation, Renewing certificates](https://eff-certbot.readthedocs.io/en/stable/using.html#renewing-certificates)
- [Let's Encrypt, FAQ：証明書の有効期間](https://letsencrypt.org/docs/faq/#what-is-the-lifetime-for-lets-encrypt-certificates-for-how-long-are-they-valid)
- [Let's Encrypt, Decreasing Certificate Lifetimes to 45 Days](https://letsencrypt.org/2025/12/02/from-90-to-45.html)
- [Let's Encrypt, Ending Support for Expiration Notification Emails](https://letsencrypt.org/2025/01/22/ending-expiration-emails.html)
