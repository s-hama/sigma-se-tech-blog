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
  ```
  $ touch example-src.txt
  ```
- `git status`でステータス確認<br>
`Untracked files`に表示されるファイル達は、Git管理下にないファイルが表示される。<br>
上記で新規作成した`example-src.txt`がバージョン管理下にないため`git add`を促す警告が表示されている。<br>
  ```
  $ git status
  On branch master

  No commits yet

  Untracked files:
  (use "git add ..." to include in what will be committed)

          example-src.txt

  nothing added to commit but untracked files present (use "git add" to track)
  ```

- `git status`のその他使用例
  ```
  $ git status [FILE]   # ファイルパス指定
  $ git status [DIR]   # ディレクトリ指定
  ```
