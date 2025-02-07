## タイトル
Python - 開発向けVim設定 : 基礎からコードチェックまで

## 目的
この記事では、Python開発向けのVim設定とコードチェックの手順について説明する。

## 実施内容
### Vimの共通設定
- ホームディレクトリに`.vimrc`ファイルを作成<br>
`.vimrc`に設定を追記することでVim に反映される。<br>
  ```
  touch ~/.vimrc
  ```

- Pythonを使う上で最低限必要な**自動インデント**と**シンタックスハイライト**のみ設定<br>
  ```
  $ vim ~/.vimrc
   filetype plugin indenton    " 自動インデントの設定
   syntax on    " シンタックスハイライトの設定
  ```
