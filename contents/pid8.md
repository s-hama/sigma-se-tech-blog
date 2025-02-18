## タイトル
Python - 対話モード（インタプリタ）: 使用例と環境変数（PYTHONSTARTUP）の設定方法

## 目的
この記事では、Pythonの対話モード（インタプリタ）の使用例と環境変数（PYTHONSTARTUP）の設定方法について説明する。

## 実施内容
### 対話モードの使用例
- 対話モードの起動<br>
Pythonのバージョン問わず、`python`コマンドを実行することで**対話モード**が起動する。<br>
対話モードでは、入力待ち状態を表す「>>>」の後に直接コードを書いて実行することができる。<br>
  ```
  $ python -V    # バージョン確認
   Python 3.6.4
  $ python　# 対話モード起動 (マイナーバージョンまでを指定しても可)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
  ```
