## タイトル
VPSで作るDjangoサイト構築手順 - Apache編：1/4 ドメイン・DNS・SSH初期設定

## 概要

VPS上でDjangoサイトを公開する前段階として、VPS契約、OSインストール、独自ドメイン、DNS設定、SSH初期設定を整理する。

この段階では、アプリケーションの実装よりも「安全にサーバーへ接続できること」と「ドメイン名でサーバーへ到達できること」が重要になる。後続のApache、Django、PostgreSQL設定の土台になるため、SSHとDNSの確認を丁寧に行う。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [前提環境](#前提環境)<br>
  手順で使用するOS、ソフトウェア、構成などの前提条件を確認。
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [VPS契約](#vps契約)<br>
  VPS事業者とプランを選び、契約する際の確認ポイントを整理。
- [OSインストール](#osインストール)<br>
  OSインストールの手順と確認ポイントを整理。
- [独自ドメインの契約](#独自ドメインの契約)<br>
  独自ドメインとサービスを選び、契約する際の確認ポイントを整理。
- [ドメインのDNS設定](#ドメインのdns設定)<br>
  ドメインのDNS設定の手順と確認ポイントを整理。
- [SSHの初期設定](#sshの初期設定)<br>
  SSHの初期設定の手順と確認ポイントを整理。

## 対象環境と利用上の注意

- 本文記載時の環境<br>
2018年当時のCentOS 7.4、さくらのVPS、お名前.comの管理画面を利用した構築記録。
- 確認時期<br>
2026年8月にVPS事業者、CentOS、SSH、DNSの公式資料と照合。<br>
現在の環境で一連の手順は再実行していない。
- 現在そのまま利用できない箇所<br>
CentOS 7は2024年6月30日にサポートを終了しているため、新規構築には使用しない。<br>
VPS・ドメイン事業者の画面や初期設定も変更されるため、サポート中のOSを選び、契約中の事業者が公開する現行手順と併せて確認する。

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

## 作業時の注意点

- ドメイン契約とDNS設定<br>
契約しただけでは接続できず、DNSレコードの設定が必要になる。
- Aレコードとネームサーバー<br>
どこで名前解決を管理するかと、どのIPへ向けるかを分けて考える。
- rootログイン禁止<br>
一般ユーザーでログインできることを確認してから無効化。
- パスワード認証の無効化<br>
公開鍵で接続できることを確認してから切り替える。

## 実施内容
### VPS契約
- 価格に見合ったスペック（容量、メモリ、CPUなど）、安全性、操作性など、何を重視するかの基準をもとにVPS提供会社を決める。
- ここでは、コストパフォーマンスとサポートの充実、プラン変更の柔軟性に基準を置き「さくらのVPS」で契約。

### OSインストール
- OSの選択<br>
開発環境(Apache, Django, PostgreSQL)がインストール可能で管理しやすいOSに絞る。<br>
ここでは、構築当時に英語圏のコミュニティが大きく、日本語情報が豊富で個人的に使い慣れているCentOSを選んだ。
- CentOS7_x86_64(標準)をインストール<br>
インストールは、SAKURA VPS管理者用のコントロールパネルからGUI操作でインストール。
  ```bash
  $ cat /etc/redhat-release
  CentOS Linux release 7.4.1708 (Core)
  ```

### 独自ドメインの契約
- ドメインの維持費、サーバー同時契約などの機能性、サポート体制など、何を重視するかの基準をもとにサービスを選ぶ。
- ここでは、Whois情報の公開代行、自動更新の有無、サポートの充実に基準を置き「お名前.com」で独自ドメインを取得した。
- 以降、この独自ドメインを**example.com**と表記。

### ドメインのDNS設定
※ 契約したサービスによって操作方法が初期状態が異なるので設定方法については割愛する。
- VPS側のネームサーバー設定（さくらのVPS）<br>
  DNS設定からドメインの追加を行う。
  ```
  ホスト名: example.com
  種別: A
  内容: VPSのIPアドレス
  TTL: 3600
  ```

- ドメイン側のネームサーバー設定（お名前.com）<br>
  **example.com**のドメイン設定でVPSのネームサーバーを登録。<br>
  ※ 設定が反映されるまで数時間〜数日かかるので注意。

- 設定確認
`nslookup`等で上記の設定が反映されているか確認すること。

### SSHの初期設定
- rootログインの無効化<br>
  ログイン用の一般ユーザーを作成し、管理作業に必要な場合は`wheel`グループへ追加。
  ```bash
  $ adduser vpsuser
  $ passwd vpsuser
  $ usermod -aG wheel vpsuser
  ```

  手元のPCで鍵を作成し、公開鍵だけをVPSへ登録。秘密鍵は手元のPCから外へ出さない。
  ```bash
  $ ssh-keygen -t ed25519 -C "vpsuser@example.com"
  $ ssh-copy-id vpsuser@example.com
  $ ssh vpsuser@example.com
  ```
  `ssh-copy-id`を利用できない場合は、公開鍵の内容をVPS側の`~/.ssh/authorized_keys`へ登録し、`.ssh`を`700`、`authorized_keys`を`600`に設定。

- SSHの設定変更<br>
  **別のターミナルから一般ユーザーの公開鍵認証に成功することを確認してから**、rootログインとパスワード認証を無効化。
  ```bash
  $ vim /etc/ssh/sshd_config
  PermitRootLogin no
  PubkeyAuthentication yes
  PasswordAuthentication no
  ```
  設定の構文を確認してから再読込みし、確認中のSSHセッションは新しい接続に成功するまで閉じない。
  ```bash
  $ sshd -t
  $ systemctl reload sshd
  ```

上記の設定により、登録済み公開鍵に対応する秘密鍵を持つ`vpsuser`だけがSSH認証できる。鍵の登録前に`PasswordAuthentication no`へ変更するとサーバーへ入れなくなるため、順序が重要となる。

## まとめ
- VPS構築の最初の段階では、OS、ドメイン、DNS、SSHを整える。
- DNSはドメイン名をVPSのIPアドレスへ向ける仕組みとなる。
- SSHはrootログインを避け、公開鍵認証を使うことで安全性を高める。

### 参考文献
- [JPRS「インターネットでもやっぱり『名前』が大切！ドメイン名とDNSの基礎知識」（日本語・DNS基礎資料）](https://jprs.jp/related-info/event/pdf/Interop2025-jprs-seminarA.pdf)
- [The CentOS Project, CentOS Linux（英語・CentOS Linux 7のEOL案内）](https://www.centos.org/centos-linux/)
- [RFC Editor, RFC 1034：Domain names - concepts and facilities（英語・DNS仕様原文）](https://www.rfc-editor.org/rfc/rfc1034.html)
- [OpenBSD Manual Pages, sshd_config(5)（英語・SSH設定仕様）](https://man.openbsd.org/sshd_config)
