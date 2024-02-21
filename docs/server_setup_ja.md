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

## OpenSSHの公開鍵認証設定
公開鍵認証設定(SSHの鍵ペア設定)を行い、vpsuser(VPS接続用の一般ユーザー)からパスフレーズでログインできるようにする

- クライアントから秘密鍵、公開鍵の生成
  ```
  ssh-keygen -f ~/.ssh/id_rsa_sigma
  ```

- クライアントからサーバーに公開鍵を転送
  ```
  scp ~/.ssh/id_rsa_sigma.pub vpsuser@x162-43-85-169.static.xvps.ne.jp:/home/vpsuser/.ssh/
  ```

- サーバーでid_rsa_sigma.pubをauthorized_keysにリネーム
  ```
  mv ~/.ssh/id_rsa_sigma.pub ~/.ssh/authorized_keys
  ```

- サーバーで権限変更
  ```
  chmod 600 ~/.ssh/authorized_keys
  chmod 700 ~/.ssh
  chmod 755 ~/
  ```

- クライアントで権限変更
  ```
  chmod 755 /Users/s-hama
  chmod 700 /Users/s-hama/.ssh
  chmod 600 /Users/s-hama/.ssh/id_rsa_sigma
  chmod 644 /Users/s-hama/.ssh/id_rsa_sigma.pub
  ```

- クライアントで~/.ssh配下にconfigファイルを下記内容で作成する
  ```
  Host sigma-se-vps
    HostName 162.43.85.169
    User vpsuser
    IdentityFile ~/.ssh/id_rsa_sigma
    Port 22
    TCPKeepAlive yes
    IdentitiesOnly yes
  ```

- クライアントで初回ログイン (known_hostsが自動生成される)
  ```
  ssh sigma-se-vps
    The authenticity of host 'x162-43-85-169.static.xvps.ne.jp (162.43.85.169)' can't be established.
    ED25519 key fingerprint is SHA256:sJ5+zzGjOV/uGBHz+ehjZEqlCJ9oT804bA2viP1pvn4.
    This key is not known by any other names
    Are you sure you want to continue connecting (yes/no/[fingerprint])? yes

    Warning: Permanently added '162.43.85.169' (ED25519) to the list of known hosts.
    Enter passphrase for key '/Users/s-hama/.ssh/id_rsa_sigma': パスワードフレーズ入力
  ```
  ※ 以降、ssh sigma-se-vpsでログイン時にパスワードフレーズの入力を求められるようになる

