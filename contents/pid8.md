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

- 対話モードの実行<br>
例えば、`sys.path`を確認したい場合、実際のコーディングと同じ要領で`sys`をインポート後、`sys.path`を実行することで、結果（pathの一覧）が表示される。<br>
  ```
  $ python　# 対話モード起動 (マイナーバージョンまで指定した python3.6 でも同じ動作)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import sys
   >>> sys.path
   ['', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', 
   '/var/www/vops/lib64/python3.6/site-packages','/var/www/vops/lib/python3.6/site-packages']
   >>>
  ```

- 対話モードの終了<br>
「Ctrl」+「D」押下または、`exit()`を実行する。<br>
  ```
  $ python
   Python 3.6.4 (default, Dec 19 2017, 14:48:12)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()
  ```

### 環境変数（PYTHONSTARTUP）の設定
対話モードでは、環境変数`PYTHONSTARTUP`に指定したスクリプトを最初に実行する。<br>
以下は、簡単な例として上記、**対話モードの実行**で記述した`sys.path`を`import sys`なしで実行できるように事前に環境変数`PYTHONSTARTUP`に設定する手順。<br>

- 確環境変数未設定で`sys.path`を実行<br>
  ```
  $ python
   Python 3.6.4 (default, Dec 19 2017, 14:48:12)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> sys.path
   Traceback (most recent call last):
     File "", line 1, in 
   NameError: name 'sys' is not defined
   >>>
  ```
  `sys`をインポートしていないので当然エラーが発生する。

- **PYTHONSTARTUP**に`import sys`を追記<br>
ホームディレクトりに`.pythonstartup`を作成後、環境変数「PYTHONSTARTUP」に`.pythonstartup`を設定し、`import sys`を追記する。<br>
  ```
  $ touch  ~/.pythonstartup    # 空ファイル新規作成
  $ vim  ~/.pythonstartup    # import sys を追記
   import sys
  $ export PYTHONSTARTUP=~/.pythonstartup    # 環境変数「PYTHONSTARTUP」に .pythonstartup を設定
  ```

- 再度対話モードで`sys.path`を実行<br>
  ```
  $ python
   Python 3.6.4 (default, Dec 19 2017, 14:48:12)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> sys.path
   ['', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', 
   '/var/www/vops/lib64/python3.6/site-packages', '/var/www/vops/lib/python3.6/site-packages']
   >>>
  ```
  `.pythonstartup`を読み込んで`sys`をインポート後、正常に`sys.path`の結果が表示されている。

上記の要領で、Pythonの標準ライブラリなどの共通モジュールを環境変数(PYTHONSTARTUP)に設定しておくと対話モードのコーディングが簡潔になる。
