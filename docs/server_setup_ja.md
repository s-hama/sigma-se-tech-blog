# 概要
このドキュメントでは、`sigma-se-tech-blog`を構築するサーバー側のセットアップ手順について下記前提元記載する  
- サーバーは、`XserverVPS`を利用することを前提に記載する
- OSは、`CentOS Stream9`を利用することを前提に記載する
- OSインストール直後の状態から実施した作業について自明であっても省略せずに記載する

## パケットフィルターの設定変更
XserverVPSからパケットフィルターの設定を変更する
- VPSパネルからパケットフィルターを有効(ON)にする
- VPSパネルからフィルタールールに下記設定を追加し、自身のIPのみ接続許可するように変更する
  ```
  プロトコル: TCP
  ポート番号: 22
  許可する送信元IPアドレス: 自身のIPアドレス/32
  ```

## VPS接続用の一般ユーザー作成
サーバー側作業
- rootでのログイン確認(初回)
  ```
  ssh root@[ホスト名]
  ```
- 一般ユーザー作成
  ```
  useradd vpsuser	
  passwd vpsuser
  ```

## OpenSSHのsshd_config設定変更
vpsuser(VPS接続用の一般ユーザー)かつ、公開鍵認証でしかログインできないように変更する

サーバー側作業
- 初期状態でバックアップしておく
  ```
  cp /etc/ssh/sshd_config /etc/ssh/sshd_config.default
  ```
- sshd_config編集
  - vim /etc/ssh/sshd_config
    - 変更前
      ```
      PermitRootLogin yes
      #PubkeyAuthentication yes
      PasswordAuthentication yes
      ```
    - 変更後
      ```
      # rootで直接ログインできないように変更
      PermitRootLogin no
      # 公開鍵認証を許可するように変更
      PubkeyAuthentication yes
      # パスワードでログインできないように変更
      PasswordAuthentication no
      ```
- SSHを再起動して設定を反映する
  ```
  systemctl restart sshd
  ```
  