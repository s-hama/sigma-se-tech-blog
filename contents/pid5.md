## タイトル
Git - GitHub登録・SSH鍵設定・ブランチ作成までの開発準備

## 概要

GitHubアカウントの準備、SSH鍵の作成と登録、リモートリポジトリの作成、clone、ブランチ作成までを整理する。

Gitを使った開発では、ローカルリポジトリとリモートリポジトリの関係を理解しておくと、clone、branch、pushの意味が分かりやすくなる。この記事は、開発を始める前の初期設定に焦点を当てる。

## この記事で扱うこと
- GitリポジトリとGitHubリポジトリの違い。
- ローカルリポジトリとリモートリポジトリの関係。
- SSH鍵を使ってGitHubへ接続する流れ。
- リモートリポジトリをcloneする手順。
- ブランチを作成して切り替える基本操作。

## 作業時の注意点

- 公開鍵と秘密鍵<br>
GitHubに登録するのは公開鍵であり、秘密鍵は外へ出さない。
- masterとmain<br>
GitHubで新しく作るリポジトリは通常mainが既定となる。既存リポジトリでは異なる場合があるため確認する。
- clone後の作業場所<br>
cloneで作成されたディレクトリ内でgitコマンドを実行する。
- ブランチ作成と切り替え<br>
現在は`git switch -c`で作成と切り替えを同時に行える。古いGitでは`git checkout -b`を使う。

## 事前説明
### Git、GitHubのリポジトリ構成イメージ
- Gitリポジトリ<br>
Gitリポジトリは、Gitがコミットやブランチなどの履歴を管理するデータベースである。開発者のPCに置くローカルリポジトリだけでも、コミットや履歴参照などの操作はオフラインで利用できる。<br>
他の開発者とネットワーク経由で共有する場合は、リモートリポジトリを用意する。<br>
リモートリポジトリを利用する場合は、**GitHub**や**GitLab**、**Bitbucket**などのGitリポジトリをホスティングするWebサービスを利用する。

- GitHubリポジトリ<br>
GitHubは、Gitの機能を拡張し、共有やコラボレーションを行うためのWebサービスでチームやオープンソースプロジェクトで開発する場合に使用する。<br>
GitHubリポジトリは、GitリポジトリをGitHubプラットフォーム上でホストしたもので単に**リモートリポジトリ**と呼ばれることが多い。<br><br>
オンラインでホストされ、他の開発者とリポジトリを共有でき、pullリクエストやIssue管理、アクションの自動化など、GitHub独自の機能が利用可能。<br>
GitHubリポジトリをリモートリポジトリとして利用し、ローカルと同期しながらソース管理する。<br><br>
一般的に開発者の端末で管理するリポジトリを**ローカルリポジトリ**、GitHubやGitLab、Bitbucketなどのホスティングサービス上で管理するリポジトリを**リモートリポジトリ**という。GitはVCS（Version Control System）であり、GitHubはGitリポジトリのホスティングサービスという違いがある。<br>

### Gitブランチと運用
- Gitブランチ<br>
**Gitブランチ**とは、コミットを指す移動可能な名前である。ブランチを分けると、機能追加や不具合修正の履歴をmainの履歴から分離して進められる。<br>
作業が完了したら、必要に応じて**ブランチ同士をマージ**する。<br>
最初のコミットが作成されると、mainまたはmasterなどの既定ブランチが履歴の起点となる。コミットが一つもない空のリポジトリでは、ブランチはまだ実体化していない。<br>
※ 現在は、デフォルトブランチ名として**main**が使われることが多い。

- 統合ブランチとトピックブランチ<br>
チームの運用ルールとして、**main**ブランチをリリース可能な状態に保つ統合ブランチとして扱うことが多い。これはGit自体が強制する規則ではない。<br>
また、統合ブランチを起点とし、不具合修正や仕様変更などの課題単位に作成するブランチを**トピックブランチ**という。<br>
変更後は、課題単位に作成された**トピックブランチ**を統合ブランチにマージする。<br>
統合ブランチにマージ後、不要となったトピックブランチは削除する。<br><br>
トピックブランチ名は、改修内容が分かりやすいようにプロジェクト内の課題管理方法に準じた名前にするのが一般的。<br>
※ 課題管理番号を含めた短い名前にすることが多い。

## 実施内容
### GitHubのアカウント準備
- GitHubのアカウント登録
[GitHub](https://github.com)からアカウント登録（Sign up）する。

- メール認証<br>
登録したメールアドレス宛にメール「**[GitHub] Please verify your email**」が届くので、本文内のURLにアクセスしメール認証を完了させる。

GitHub Freeでも非公開リポジトリを作成できるため、開発準備のためだけに有料プランへ変更する必要はない。<br>組織機能や高度な機能が必要になった時点でプランを比較する。

### SSHの公開鍵、秘密鍵の生成
通信手段は、SSHを利用する。
- Ed25519形式の秘密鍵と公開鍵を生成<br>
既存の鍵を誤って上書きしないよう`~/.ssh`の内容を確認してから、`ssh-keygen`を実行する。<br>GitHubはEd25519を推奨しており、Ed25519を利用できない古い環境では4096ビットのRSA鍵を選択する。
  ```bash
  $ install -d -m 700 ~/.ssh
  $ ls -la ~/.ssh
  $ ssh-keygen -t ed25519 -C "GitHubに登録したメールアドレス"
  Enter file in which to save the key (/home/user/.ssh/id_ed25519):    # Enter押下
  Enter passphrase (empty for no passphrase):    # 十分に強いパスフレーズを入力
  Enter same passphrase again:
  ```

- 秘密鍵、公開鍵の生成確認<br>
  ```bash
  $ ls ~/.ssh
  id_ed25519  id_ed25519.pub
  ```

- 秘密鍵をssh-agentへ登録<br>
`ssh-add`で秘密鍵をssh-agentへ登録すると、エージェントが起動している間はパスフレーズを毎回入力せずに済む。<br>パスフレーズそのものを削除する操作ではない。<br>
`ssh-add`は、OSによって実行方法が若干違うので注意。
  ```bash
  $ eval "$(ssh-agent -s)"
  $ ssh-add ~/.ssh/id_ed25519
  $ ssh-add -l    # 登録確認
  ```

- GitHubに公開鍵を登録

  1. 右上のプロフィールアイコンから**Settings**リンクをクリックする。
  2. **SSH and GPG keys**をクリックする。
  3. **New SSH key**をクリックする。
  4. **Title**テキストボックスに任意の端末認識ができるような分かりやすいタイトルを記入する。
  5. 生成した`id_ed25519.pub`（公開鍵）の内容を**Key**にコピー＆ペーストする。秘密鍵`id_ed25519`は登録しない。
  6. **Add key**をクリックして保存する。
  7. GitHubのログインパスワードの入力を求められるので入力する。
  8. 手順3で表示した画面に切り替わり、**SSH keysセクション**に手順4で設定した**Title**が表示されていれば成功。

- 接続確認<br>
初回接続時は、表示されたホスト鍵フィンガープリントをGitHub公式ドキュメントの値と照合してから続行する。<br>認証成功時は、GitHubがシェルアクセスを提供しない旨のメッセージが表示され、コマンドの終了コードは`1`となるが問題はない。
  ```bash
  $ ssh -T git@github.com
  Hi USERNAME! You've successfully authenticated, but GitHub does not provide shell access.
  ```

### GitHubのリポジトリ作成
1. GitHubトップの右上「＋」をクリックし、**New Repository**リンクから**Create a new repository**画面に遷移する。
2. 画面上部にある**Repository name**に任意のリポジトリ名を入力する。
3. リポジトリの公開 / 非公開を設定する**Public / Private**ラジオボタンを選択する。
4. この後の例と同じく`main`ブランチをすぐ利用できるよう、**Add a README file**を選択する。空のリポジトリにはまだブランチが存在しない点に注意する。
5. 入力内容を確認し、**Create repository**ボタンをクリックする。
6. リポジトリ画面の**Code**から**SSH**を選択する。

### [git clone] : リモートリポジトリの複製
上記で作成したリモートリポジトリをclone(複製)する。
- Gitの作業フォルダ作成
  ```bash
  $ mkdir ~/gitlocalrep
  $ cd ~/gitlocalrep
  ```

- リモートリポジトリをclone 
  ```bash
  $ git clone git@github.com:YOUR_USERNAME/exrep.git
  Cloning into 'exrep'...
  $ ls    # 確認
  exrep
  ```
  ※ `YOUR_USERNAME`は実際のユーザー名へ置き換える。ここではリポジトリ名を`exrep`としているが、作成した名前が異なる場合は`exrep`も置き換え、リモートリポジトリの**Code**画面に表示されるSSH URLを使用する。<br>山括弧（`< >`）をコマンドへそのまま入力すると、シェルではリダイレクトとして解釈される。<br>
  上記の通り`clone`によってGitリポジトリが`clone`され**exrep**ディレクトリが作成される。

### ブランチの確認・作成・切り替え
- 現在のブランチ確認<br>
アスタリスク（`*`）があるブランチが現在の作業ブランチとなる。<br>ここではGitHubの標準設定とREADME付きで作成したため、`main`が存在する。GitHub側で既定ブランチ名を変更している場合は、その名前に読み替える。
  ```bash
  $ cd ~/gitlocalrep/exrep    # cloneしたディレクトリに移動
  $ git branch    # ブランチの確認
  * main
  ```

- topicbranchブランチの作成と切り替え<br>
`git switch -c`を使うと、新しいブランチの作成と切り替えを同時に実行できる。
  ```bash
  $ git switch -c topicbranch
  Switched to a new branch 'topicbranch'
  $ git branch    # ブランチの確認
    main
  * topicbranch
  ```

- （補足）古いGitでの操作<br>
`git switch`を利用できない古いGitでは、`git checkout -b`で同じ操作を行う。
  ```bash
  $ git checkout -b topicbranch
  Switched to branch 'topicbranch'
  $ git branch
    main
  * topicbranch
  ```

以上で開発準備完了。<br><br>
以降は、必要に応じてリモートの変更をpullし、ローカルでadd、commitした変更をpushする流れとなる。<br><br>
参考 : [Git - 状態管理の概念と基本操作 : status, add, commit, diff, reset, push, pull, checkout](https://sigma-se.com/detail/6/)

## まとめ
- GitHubを使う開発準備では、アカウント、SSH鍵、リポジトリ作成、cloneを順番に行う。
- ローカルリポジトリとリモートリポジトリの関係を理解すると、pushやpullの意味が分かりやすい。
- 作業はブランチを分けて進めると、変更範囲を管理しやすくなる。

### 参考文献
- [GitHub Docs, About repositories](https://docs.github.com/en/repositories/creating-and-managing-repositories/about-repositories)
- [GitHub Docs, Generating a new SSH key and adding it to the ssh-agent](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
- [GitHub Docs, Adding a new SSH key to your GitHub account](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/adding-a-new-ssh-key-to-your-github-account)
- [GitHub Docs, Testing your SSH connection](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/testing-your-ssh-connection)
- [GitHub Docs, Creating a new repository](https://docs.github.com/en/repositories/creating-and-managing-repositories/creating-a-new-repository)
- [Git Documentation, git-switch](https://git-scm.com/docs/git-switch)
