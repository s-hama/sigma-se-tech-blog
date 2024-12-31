## タイトル
Git - 状態管理の概念と基本操作 : status, add, commit, diff, reset, push, pull, checkout

## 目的
この記事では、Gitにおける状態管理の概念と基本操作について説明する。

## 項目説明
### 状態管理の概念
- ワーキングツリー（working tree）<br>
現在チェックアウトしているローカルディレクトリを指す。
実際に修正、追加、削除を行う作業場所のこと。

- インデックス / ステージ（index / staging area）<br>
`commit`前に`ワーキングツリー（working tree）`の変更を一時的に保存する場所。
変更が`index`として表示される。
`commit`準備ができた変更を`ステージ（staging area）`に移動して`commit`対象を管理する。

- ローカルリポジトリ（local repository）<br>
ローカルマシン上にある個別リポジトリ。
`commit`されたすべての履歴やバージョンが保存される場所。
`branch`単位の`push`によって`commit`を`リモートリポジトリ（remote repository）`に反映する。

- リモートリポジトリ（remote repository）<br>
ネットワーク上にある共有リポジトリ。
通常は、`GitHub`や`GitLab`などのホスティングサービス上に存在する。

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

### [git add] : インデックスへ反映
- 前項の警告に従い`git add`を実行<br>
`git add`により、変更が`ワーキングツリー`から`インデックス`へ反映される。<br>
  ```
  $ git add example-src.txt
  ```

- ステータス確認<br>
  ```
  $ git status
  On branch master

  No commits yet

  Changes to be committed:
    (use "git rm --cached ..." to unstage)

        new file:   example-src.txt
  ```

- `git add`のその他使用例
  ```
  $ git add [FILE]  # ファイルパス指定
  $ git add [FILE1]  [FILE2]  [FILE3]  .... # ファイル複数指定
  $ git add [DIR]  # ディレクトリ指定
   git add [DIR1]  [DIR2]  [DIR3]  .... # ディレクトリ複数指定
   git add .    # カレントディレクト以下すべてを追加する
   git add -A   # Git管理内のすべての変更する (--allと同じ)
   git add --all  # Git管理内のすべての変更する (--Aと同じ)
   git add -u   # Git管理内で変更があったファイルをすべて追加する (--updateと同じ)
   git add --update    # Git管理内で変更があったファイルをすべて追加する (--uと同じ)
   git add -f     # .gitignoreにある管理対象外に設定したファイルも強制的に追加する(.-forceと同じ)
   git add --force   # .gitignoreにある管理対象外に設定したファイルも強制的に追加る (-と同)
   git add -p    # Git管理内のすべてのファイルを対象に対話形式 (Y or N)で追加す(--patchとじ)
   git add --patch   # Git管理内のすべてのファイルを対象に対話形式 (Y or N)で追加る (-同じ)
   git add -n    # addコマンド実行後のどういった結果になるか確認できる (--dry-rn同じ)
  $ git add --dry-run  # addコマンド実行後のどういった結果になるか確認できる (-nとじ)
  ```
