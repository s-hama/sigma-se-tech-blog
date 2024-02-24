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

## Vimインストールと初期設定
サーバー側作業
- DNFの更新
  ```
  sudo dnf update
  sudo dnf upgrade
  ```

- Vimインストール
  ```
  sudo dnf -y install vim-enhanced
  ```

- コマンドエイリアスを自身のユーザー固有環境として適用する

  最終行にalias vi='vim'を追記
  ```
  vi ~/.bashrc
  ```
  変更を反映
  ```
  source ~/.bashrc
  ```

- 自身のユーザー固有環境としてVimを設定する

  ※ ユーザー単位(rootとvpsuserそれぞれ)で行う
  .vimrcを新規作成
  ```
  vi ~/.vimrc
  ```
  下記の内容で追記し保存
  ```
  " vim の独自拡張機能を使用
  " - vi との互換性無し
  set nocompatible

  " 文字コードを指定
  set encoding=utf-8

  " ファイルエンコードを指定
  " 複数指定する場合はカンマ区切り
  " 複数指定の場合 先頭から順に成功するまで読み込む
  set fileencodings=utf-8

  " 自動認識させる改行コードを指定
  set fileformats=unix,dos

  " バックアップを取得
  " - 逆は [ set nobackup ]
  set backup

  " バックアップを取得するディレクトリを指定
  set backupdir=~/backup

  " 検索履歴を残す世代数
  set history=50

  " 検索時に大文字小文字を区別しない
  set ignorecase

  " 検索語に大文字を混ぜると検索時に大文字を区別する
  set smartcase

  " 検索語にマッチした単語をハイライト
  " - 逆は [ set nohlsearch ]
  set hlsearch

  " インクリメンタルサーチを使用
  " - 検索語の入力最中から随時マッチする文字列の検索を開始
  " - 逆は [ set noincsearch ]
  set incsearch

  " 行番号を表示
  " - 逆は [ set nonumber ]
  set number

  " 改行 ( $ ) やタブ ( ^I ) を可視化
  set list

  " 括弧入力時に対応する括弧を強調
  set showmatch

  " ファイルの末尾に改行を入れない
  set binary noeol

  " 自動インデントを有効にする
  " - 逆は [ noautoindent ]
  set autoindent

  " 構文ごとに色分け表示する
  " - 逆は [ syntax off ]
  syntax on

  " [ syntax on ] の場合のコメント文の色を変更
  highlight Comment ctermfg=LightCyan

  " ウィンドウ幅で行を折り返す
  set wrap
  ```

## ファイアーウォールの設定
  - ファイアーウォールの有効化
    - 有効化されているか確認
      ```
      systemctl is-enabled firewalld
      disabled
      ```
    - 無効になっているので有効化する
      ```
      systemctl enable --now firewalld
      Created symlink /etc/systemd/system/dbus-org.fedoraproject.firewalld1.service → /usr/lib/systemd/system/firewalld.service.
      Created symlink /etc/systemd/system/multi-user.target.wants/firewalld.service → /usr/lib/systemd/system/firewalld.service.
      ```
  - 設定確認/変更
    - どのゾーンが許可されているか確認
      ```
      firewall-cmd --get-default-zone
      public
      ```
    - ファイアーウォールの設定状況確認
      ```
      firewall-cmd --list-all
      public (active)
        target: default
        icmp-block-inversion: no
        interfaces: ens3
        sources: 
        services: cockpit dhcpv6-client ssh
        ports: 
        protocols: 
        forward: yes
        masquerade: no
        forward-ports: 
        source-ports: 
        icmp-blocks: 
        rich rules:
      ```
    - httpとhttpsを許可する(servicesにhttpとhttpsが許可されてないため)
      - httpのサービスを永続的に許可
      ```
      firewall-cmd --zone=public --add-service=http --permanent
      ```
      - httpsのサービスを永続的に許可
      ```
      firewall-cmd --zone=public --add-service=https --permanent
      ```
    - ファイアーウォールを再起動する
      ```
      firewall-cmd --reload
      ```
    - ファイアーウォールの設定状況確認
      ```
      firewall-cmd --list-all
      public (active)
        target: default
        icmp-block-inversion: no
        interfaces: ens3
        sources: 
        services: cockpit dhcpv6-client http https ssh
        ports: 
        protocols: 
        forward: yes
        masquerade: no
        forward-ports: 
        source-ports: 
        icmp-blocks: 
        rich rules:
      ```
