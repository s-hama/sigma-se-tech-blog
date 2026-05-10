## タイトル
Git - 状態管理と基本操作：status・add・commit・diff・reset・push・pull・checkout

## 概要

Gitの状態管理の考え方と、よく使う基本コマンドを整理する。

Gitでは、ワーキングツリー、インデックス、ローカルリポジトリ、リモートリポジトリのどこに変更があるかを理解することが重要になる。コマンドを丸暗記するより、変更がどこからどこへ移動するかを追うと操作ミスを減らせる。

## この記事で理解できること
- ワーキングツリー、インデックス、ローカルリポジトリ、リモートリポジトリの違い。
- status、add、commit、diffの基本的な流れ。
- resetで何が戻るかの考え方。
- pushとpullでリモートと同期する流れ。
- checkoutでブランチや特定コミットへ移動する操作。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| 作業場所 | Git管理下のディレクトリでコマンドを実行する。 |
| 状態確認 | 変更前後でgit statusを確認する習慣を付ける。 |
| ステージング | commit対象に含める変更だけをgit addする。 |
| 履歴操作 | resetは影響範囲を理解してから使う。 |
| リモート操作 | push/pull前に作業ブランチを確認する。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| addとcommit | addはコミット候補へ載せる操作、commitは履歴として保存する操作。 |
| diffの対象 | ワーキングツリー、インデックス、HEADのどこと比較するかで結果が変わる。 |
| reset --hard | 作業中の変更も消えるため、慎重に使う。 |
| pushとpull | pushは送る、pullは取り込む操作として方向を意識する。 |

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
  $ git add [FILE]    # ファイルを指定して追加する
  $ git add [FILE1] [FILE2] [FILE3]    # 複数ファイルを指定して追加する
  $ git add [DIR]    # ディレクトリを指定して追加する
  $ git add [DIR1] [DIR2] [DIR3]    # 複数ディレクトリを指定して追加する
  $ git add .    # カレントディレクトリ以下の変更を追加する
  $ git add -A    # Git管理下の変更をすべて追加する（--all と同じ）
  $ git add --all    # Git管理下の変更をすべて追加する（-A と同じ）
  $ git add -u    # 追跡済みファイルの変更と削除を追加する（--update と同じ）
  $ git add --update    # 追跡済みファイルの変更と削除を追加する（-u と同じ）
  $ git add -f [FILE]    # .gitignore対象のファイルを強制的に追加する（--force と同じ）
  $ git add --force [FILE]    # .gitignore対象のファイルを強制的に追加する（-f と同じ）
  $ git add -p    # 差分を対話形式で確認しながら追加する（--patch と同じ）
  $ git add --patch    # 差分を対話形式で確認しながら追加する（-p と同じ）
  $ git add -n    # 実際には追加せず、追加対象を確認する（--dry-run と同じ）
  $ git add --dry-run    # 実際には追加せず、追加対象を確認する（-n と同じ）
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
  $ git show HEAD    # HEADのコミット内容を確認
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
不要になったリモートブランチを`origin`から削除する。<br>
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
developブランチに切り替える。<br>
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

## 実務とのつながり
- 状態管理<br>
    レビュー前に変更範囲を確認する基本になる。
- 差分確認<br>
    意図しない変更をコミットに混ぜないために重要になる。
- ブランチ操作<br>
    複数の修正を並行して進めるときの土台になる。

## 要約
- Gitの基本は、変更がワーキングツリー、インデックス、リポジトリのどこにあるかを理解すること。
- status、diffで確認し、add、commitで履歴に残す流れを押さえる。
- resetやpush/pullは影響範囲が大きいため、操作前にブランチと状態を確認する。
