## タイトル
Git - 開発準備 : GitHub登録からブランチ作成まで

## 目的
この記事では、GitHubへの新規登録からローカルブランチを作成するまでの開発準備について説明する。

##　事前説明
###　Git、GitHubのリポジトリ構成イメージ
- Gitリポジトリ<br>
Gitリポジトリは、Gitで管理される変更履歴を記録するローカルのデータベースで開発者のPCやローカル環境に保存される。<br>
個人やチームでバージョン管理をローカル環境で行う場合に使用され、オフラインでも利用可能。<br>
他の開発者との共有には、別途リモートリポジトリが必要となる。<br>
リモートリポジトリを利用する場合は、**GitHub**や**GitLab**、**Bitbucket**などのGitリポジトリをホスティングするWebサービスを利用する。

- GitHubリポジトリ<br>
GitHubは、Gitの機能を拡張し、共有やコラボレーションを行うためのWebサービスでチームやオープンソースプロジェクトで開発する場合に使用する。<br>
GitHubリポジトリは、GitリポジトリをGitHubプラットフォーム上でホストしたもので単に**リモートリポジトリ**と呼ばれることが多い。<br><br>
オンラインでホストされ、他の開発者とリポジトリを共有でき、pullリクエストやIssue管理、アクションの自動化など、GitHub独自の機能が利用可能。<br>
GitHubリポジトリをリモートリポジトリとして利用し、ローカルと同期しながらソース管理する。<br><br>
一般的に開発者がローカル管理しているリポジトリを**ローカルリポジトリ**、GitHubやGitLab、BitbucketなどのVCS(Version Control System)を介してネットワーク上で管理しているリポジトリを**リモートリポジトリ**という。<br>

###　Gitブランチと運用
- Gitブランチ<br>
**Gitブランチ**とは、複数の開発者が同時に修正しても互いに影響を受けないよう**機能単位または、開発者もしくはグループ単位に割り当てる開発領域**のこと。<br>
ブランチ上で行った変更履歴もそれぞれ記録され変更後、**ブランチ同士のマージ**を行いソース管理していく。<br>
初期状態では、Gitリポジトリの作成と同時に作られるmaster(※)ブランチのみ存在し、このmaster(※)ブランチがすべての起点となる。<br>
※ 2020年10月1日以降、デフォルトブランチ名が**mastar**から**main**に変更されている。

- 統合ブランチとトピックブランチ<br>
通常運用の**master**ブランチは、リリース可能なリビジョンが常に切ってある**統合ブランチ**として使用される。<br>
また、**統合ブランチ**を起点とし、不具合修正、仕様変更などの課題単位に作成するブランチを**トピックブランチ**という。<br>
変更後は、課題単位に作成された**トピックブランチ**を統合ブランチにマージする。<br>
統合ブランチにマージ後、不要となったトピックブランチは削除する。<br><br>
トピックブランチ名は、改修内容が分かりやすいようにプロジェクト内の課題管理方法に準じた名前にするのが一般的。<br>
※ 課題管理番号を含めた短い名前にすることが多い。

## 実施内容
### GitHubのアカウント準備
- Githubのアカウント登録
https://github.com からアカウント登録(Sign up)する。

- メール認証<br>
登録したメールアドレス宛にメール「**[GitHub] Please verify your email**」が来るので、本文内のURLにアクセスしメール認証を完了させる。

- 有料プラン変更<br>
(1) 右上のプロフィールアイコンから**Settings**リンクをクリック。<br>
(2) 左側のサイドメニューから**Billing**リンクをクリック。<br>
(3) **Billing overviewセクション**の**Plan**にある**Get private repositories**ボタンをクリック。<br>
(4) **Upgrade summaryセクション**の**Pay monthly / Pay yearly**ラジオボタンを選択。<br>
(5) **Billing informationセクション**の**Add a Payment Method**リンクから支払い方法を指定。<br>
(6) 必須情報の入力後、**Upgrade plan**ボタンをクリックする。<br>
(7) (6)の後、**Billing overviewセクション**の**Plan**に**Personal - Unlimited private repositories**と表示されていれば、有料版へプラン変更が正常に完了。<br>

### SSHの公開鍵、秘密鍵の生成
通信手段は、SSHを利用する。
- id_rsa(秘密鍵)、id_rsa.pub(公開鍵)の生成<br>
homeディレクトリに`.ssh`フォルダを作成後、そのフォルダに移動し、`ssh-keygen`を実行。
  ```
  $ mkdir ~/.ssh
  $ cd ~/.ssh
  $ ssh-keygen -t rsa -C "GitHubに登録したメールアドレス"
  Generating public/private rsa key pair.
  Enter file in which to save the key (/root/.ssh/id_rsa):        # Enter押下
  Enter passphrase (empty for no passphrase):        # 新規のパスワードを入力
  Enter same passphrase again:        # 確認用のパスワードを入力
  Your identification has been saved in /root/.ssh/id_rsa.
  Your public key has been saved in /root/.ssh/id_rsa.pub.
  The key fingerprint is:
  …
  ```

- 秘密鍵、公開鍵の生成確認<br>
  ```
  $ ls ~/.ssh
  id_rsa  id_rsa.pub
  ```

- 秘密鍵、パスフレーズの登録<br>
`ssh-add`で、SSH接続時に**パスワード入力を省略する**設定を行う。
`ssh-add`は、OSによって実行方法が若干違うので注意。
  ```
  $ eval `ssh-agent`    # ssh-agent起動（evalなしだと環境変数の設定が必要）
  $ ssh-add ~/.ssh/id_rsa
  $ ssh-add -l    # 登録確認
  2048 ********** /root/.ssh/id_rsa (RSA)   # このように表示されば正常に登録されている。
  ```

- GitHubに公開鍵を登録<br>
(1) 右上のプロフィールアイコンから**Settings**リンクをクリックする。<br>
(2) 左側のサイドメニューから**SSH and GPG Keys**リンクをクリックする。<br>
(3) **SSH Keysセクション**の右側にある**add SSH Key**ボタンをクリックする。<br>
(4) **Title**テキストボックスに任意の端末認識ができるような分かりやすいタイトルを記入する。<br>
(5) 上記 秘密鍵、パスフレーズの登録で生成された id_rsa.pub(公開鍵) ファイル内すべてを**Key**にコピー＆ペーストする。<br>
(6) **Add key**をクリックして保存する。<br>
(7) GitHubのログインパスワードの入力を求められるので入力する。<br>
(8) (3) で表示した画面に切り替わり**SSH keysセクション**に上記 (4)で設定した**Title**が表示されていれば成功。<br>

- 接続確認<br>
最後の2行は、GitHubはシェルアクセスを提供しない(許可しない)旨のメッセージなので問題なし、正常に接続できている。
  ```
  $ ssh -l git -i ~/.ssh/id_rsa github.com
  The authenticity of host 'github.com (192.30.255.113)' can't be established.
  RSA key fingerprint is **********.
  RSA key fingerprint is **********.
  Are you sure you want to continue connecting (yes/no)? yes    # 接続を継続するかの確認（yesを入力）
  Warning: Permanently added 'github.com,192.30.255.113' (RSA) to the list of known hosts.
  Enter passphrase for key '/root/.ssh/id_rsa':    # 上記、[ ssh-keygen ]で登録したパスワードを入力
  PTY allocation request failed on channel 0
  Hi ! You've successfully authenticated, but GitHub does not provide shell access.
  Connection to github.com closed.
  ```

### GitHubのリポジトリ作成
- id_rsa(秘密鍵)、id_rsa.pub(公開鍵)の生成<br>
`home`ディレクトリに`.ssh`フォルダを作成後、そのフォルダに移動し、`ssh-keygen`を実行する。<br>
(1) GitHubトップの右上「＋」をクリックし、**New Repository**リンクから**Create a new repository**画面に遷移する。<br>
(2) 画面上部にある**Repository name**に任意のリポジトリ名を入力する。<br>
(3) リポジトリの公開 / 非公開を設定する**Public / Private**ラジオボタンを選択する。<br>
(4) (2)、(3) の入力に間違いがないことを確認し**Create repository**ボタンをクリックする。<br>
(5) **Quick setup**画面の表示後、そのすぐ下にある**SSH**ボタンをクリックする。<br>

### [git clone] : リモートリポジトリの複製
上記で作成したリモートリポジトリをclone(複製)する。
- Gitの作業フォルダ作成
  ```
  $ mkdir ~/gitlocalrep
  $ cd gitlocalrep
  ```

- リモートリポジトリをclone 
  ```
  $ git clone git@github.com:sigma-se/exrep.git    # 下記※のパスを入力
  Cloning into 'exrep'...
  Enter passphrase for key '/root/.ssh/id_rsa':    # パスフレーズを入力
  warning: You appear to have cloned an empty repository.   # 空のディレクトリである警告
  $ ls    # 確認
  exrep
  ```
  ※ リモートリポジトリの**Quick setup**画面の**SSH**ボタン右側にあるURL「git@github.com:\<username\>/\<repositoryname\>.git」。<br>
  上記の通り`clone`によってGitリポジトリが`clone`され**exrep**ディレクトリが作成される。
