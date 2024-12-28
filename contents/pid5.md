## タイトル
Git - 状態管理の概念と基本操作 : add, commit, diff, checkout, reset

## 目的
この記事では、Gitにおける状態管理モデルの概念について説明する。

## 項目説明
### 状態管理の概念
- ワーキングツリー（working tree）
現在チェックアウトしているローカルディレクトリを指す。
実際に修正、追加、削除を行う作業場所のこと。

- インデックス / ステージ（index / staging area）
`commit`前に`working tree`の変更を一時的に保存する場所。
変更が`index`として表示される。
`commit`準備ができた変更を`staging area`に移動して`commit`対象を管理する。

- ローカルリポジトリ（local repository）
ローカルマシン上にある個別リポジトリ。
`commit`されたすべての履歴やバージョンが保存される場所。
`branch`単位の`push`によって`commit`を`remote repository`に反映する。

- リモートリポジトリ（remote repository）
ネットワーク上にある共有リポジトリ。
通常は、`GitHub`や`GitLab`などのホスティングサービス上に存在する。
