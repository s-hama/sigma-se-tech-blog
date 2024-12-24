## タイトル
Git - 状態管理概念 : working tree, index, stage, local repository, remote repository

## 目的
この記事では、Gitにおける状態管理モデルの概念について説明する。

## 項目説明
### ワーキングツリー（working tree）
現在チェックアウトしているローカルディレクトリを指す。
実際に修正、追加、削除を行う作業場所のこと。

### インデックス / ステージ（index / staging area）
`commit`前に`working tree`の変更を一時的に保存する場所。
変更が`index`として表示される。
`commit`準備ができた変更を`staging area`に移動して`commit`対象を管理する。
