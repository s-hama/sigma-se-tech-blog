## タイトル
Git - 状態管理の概念と基本操作 : status, add, commit, diff, reset, push, pull, checkout

## 目的
この記事では、Gitにおける状態管理の概念と基本操作について説明する。

## 項目説明
### 状態管理の概念
- ワーキングツリー（working tree）<br>
現在チェックアウトしているローカルディレクトリを指す。<br>
実際に修正、追加、削除を行う作業場所のこと。

- インデックス / ステージ（index / staging area）<br>
`commit`前に**ワーキングツリー（working tree）**の変更を一時的に保存する場所。<br>
変更が**index**として表示される。<br>
`commit`準備ができた変更を**ステージ（staging area）**に移動して`commit`対象を管理する。

- ローカルリポジトリ（local repository）<br>
ローカルマシン上にある個別リポジトリ。<br>
`commit`されたすべての履歴やバージョンが保存される場所。<br>
`branch`単位の`push`によって`commit`を**リモートリポジトリ（remote repository）**に反映する。

- リモートリポジトリ（remote repository）<br>
ネットワーク上にある共有リポジトリ。<br>
通常は、**GitHub**や**GitLab**などのホスティングサービス上に存在する。

### [git status] : ステータス確認
- 確認用に`touch`でファイルを新規作成
  ```bash
  $ touch example-src.txt
  ```
- `git status`でステータス確認<br>
`Untracked files`に表示されるファイル達は、Git管理下にないファイルが表示される。<br>
上記で新規作成した`example-src.txt`がバージョン管理下にないため`git add`を促す警告が表示されている。<br>
  ```bash
  $ git status
  On branch master

  No commits yet

  Untracked files:
  (use "git add ..." to include in what will be committed)

          example-src.txt

  nothing added to commit but untracked files present (use "git add" to track)
  ```

- `git status`のその他使用例
  ```bash
  $ git status [FILE]    # ファイルパス指定
  $ git status [DIR]    # ディレクトリ指定
  ```

### [git add] : インデックスへ反映
- 前項の警告に従い`git add`を実行<br>
`git add`により、変更が**ワーキングツリー**から**インデックス**へ反映される。<br>
  ```bash
  $ git add example-src.txt
  ```

- ステータス確認<br>
  ```bash
  $ git status
  On branch master

  No commits yet

  Changes to be committed:
    (use "git rm --cached ..." to unstage)

        new file:   example-src.txt
  ```

- `git add`のその他使用例
  ```bash
  $ git add [FILE]    # ファイルパス指定
  $ git add [FILE1]  [FILE2]  [FILE3] ....    # ファイル複数指定
  $ git add [DIR]  # ディレクトリ指定
   git add [DIR1]  [DIR2]  [DIR3] ....    # ディレクトリ複数指定
   git add .    # カレントディレクト以下すべてを追加する
   git add -A    # Git管理内のすべての変更する (--allと同じ)
   git add --all    # Git管理内のすべての変更する (--Aと同じ)
   git add -u    # Git管理内で変更があったファイルをすべて追加する (--updateと同じ)
   git add --update    # Git管理内で変更があったファイルをすべて追加する (--uと同じ)
   git add -f    # .gitignoreにある管理対象外に設定したファイルも強制的に追加する(.-forceと同じ)
   git add --force    # .gitignoreにある管理対象外に設定したファイルも強制的に追加る (-と同)
   git add -p    # Git管理内のすべてのファイルを対象に対話形式 (Y or N)で追加す(--patchとじ)
   git add --patch    # Git管理内のすべてのファイルを対象に対話形式 (Y or N)で追加る (-同じ)
   git add -n    # addコマンド実行後のどういった結果になるか確認できる (--dry-rn同じ)
  $ git add --dry-run    # addコマンド実行後のどういった結果になるか確認できる (-nとじ)
  ```

### [git commit] : ローカルリポジトリへ反映
- 上記の変更をメッセージ付きでコミット
`git commit`により、変更が**インデックス**から**ローカルリポジトリ**へ反映される。<br>
  ```bash
  $ git commit -m 'Add example-src.txt'
  [master (root-commit) 304a1cd] Add example-src.txt
  Committer: root 
  Your name and email address were configured automatically based
  on your username and hostname. Please check that they are accurate.
  You can suppress this message by setting them explicitly. Run the
  following command and follow the instructions in your editor to edit
  your configuration file:

      git config --global --edit

  After doing this, you may fix the identity used for this commit with:

      git commit --amend --reset-author

  1 file changed, 0 insertions(+), 0 deletions(-)
  create mode 100644 example-src.txt
  ```

- `git commit`のその他使用例<br>
  ```bash
  $ git commit  -m "コミットメッセージ"    # コミットメッセージを指定
  $ git commit  --amend    # 直前のコミットを上書き
  $ git commit  [FILE]    # ファイルパス指定
  ```

### [git diff] : 差分確認
- コミット後の編集<br>
ファイルを編集後、再度ステータス確認を行うと下記の通り、コミット後に編集があったことを示す`modified: example-src.txt`が表示されるようになる。<br>
  ```bash
  $ echo "test input" > example-src.txt
  $ git status
  On branch master
  Changes not staged for commit:
  (use "git add ..." to update what will be committed)
  (use "git checkout -- ..." to discard changes in working directory)

          modified:   example-src.txt

  no changes added to commit (use "git add" and/or "git commit -a")
  ```

- `git diff`で差分確認<br>
差分結果として`test input`が追記されていることが分かる。<br>
  ```bash
  $ git diff
  diff --git a/example-src.txt b/example-src.txt
  index e69de29..c2cbb36 100644
  --- a/example-src.txt
  +++ b/example-src.txt
  @@ -0,0 +1 @@
  +test input
  ```

- `git diff`のその他使用例
  ```bash
  $ git diff HEAD    # 最新コミットとの差分確認
  $ git diff --cached    # HEADとインデックスの差分確認
  $ git diff --name-only    # 差分が発生しているファイル名の一覧を表示する
  $ git diff HEAD^ HEAD    # 直前のコミット内容を確認
  $ git diff show    # HEADのコミット内容を確認
  ```

### [git reset] : コミットの取り消し
- 最新コミット（HEAD）だけを取り消し、**ワーキングツリー**はそのまま<br>
  ```bash
  git reset --soft HEAD~1
  ```

- 最新コミット（HEAD）だけを取り消し、変更を**ステージ**から外す<br>
  ```bash
  git reset --mixed HEAD~1
  ```

- 最新のコミット（HEAD）だけを取り消し、**HEADの位置**、**インデックス / ステージ**、**ワーキングツリー**も全て取り消す<br>
  ```bash
  git reset --hard HEAD~1
  ```

### [git push] : リモートリポジトリへ反映
- 新規ブランチを**リモートリポジトリ**に反映し、追跡を設定<br>
ローカルの`feature/new-feature`をリモートリポジトリの`origin`に作成し、`-u(--set-upstream)`オプションの指定によって、**ローカルリポジトリ**と**リモートリポジトリ**が紐付けられるため、次回以降は`git push`のみでpush可能となる。<br>
  ```bash
  git push -u origin feature/new-feature
  ```

- 特定のリモートブランチを指定して**リモートリポジトリ**へ反映<br>
ローカルの`develop`ブランチをリモートリポジトリの`origin`に反映する。<br>
  ```bash
  git push origin develop
  ```

- **リモートリポジトリ**から特定のブランチを削除<br>
ローカルの`develop`ブランチをリモートリポジトリの`origin`に反映する。<br>
  ```bash
  git push origin --delete branch_name
  ```

### [git pull] : リモートリポジトリの変更を取込む
- **リモートリポジトリ**の変更を**ローカルリポジトリ**に取り込む（リモートとブランチを明示的に指定）<br>
`git pull`は、`git fetch`と`git merge`の操作をまとめて行っている。<br>
  ```bash
  git pull origin main
  ```

### [git checkout] : チェックアウト
- ブランチの切り替え<br>
developブランチに切り替る。<br>
  ```bash
  git checkout develop
  ```

- 新規ブランチ作成と切り替え<br>
新規ブランチを作成し、同時にそのブランチに切り替える。<br>
  ```bash
  git checkout -b feature/develop-1
  ```

- 特定のコミットをチェックアウト<br>
**コミットハッシュ**を指定し、**ワーキングツリー**を特定のコミットに変更する。<br>
  ```bash
  git checkout a1b2c3d
  ```
