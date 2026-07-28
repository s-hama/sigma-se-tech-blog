## タイトル
Python - 対話モード：PYTHONSTARTUPと起動時設定の使い方

## 概要

Pythonの対話モードの基本操作と、PYTHONSTARTUPを使った起動時スクリプトの設定方法を整理する。

対話モードは、短いコードの確認、ライブラリの挙動確認、環境変数やパスの調査に便利な実験場所になる。<br>PYTHONSTARTUPを使うと、毎回使うimportや補助関数を起動時に読み込める。

## この記事で扱うこと
- `python`または`python3`コマンドで対話モードを起動する方法。
- sys.pathなどを対話的に確認する流れ。
- exit()やCtrl+Dで終了する方法。
- PYTHONSTARTUPで起動時スクリプトを読み込む方法。
- IPythonやimport thisなどの補足的な使い方。

## 作業時の注意点

- pythonとpython3<br>
環境によって起動するバージョンが違うことがある。
- sys未定義エラー<br>
importしていないモジュールは対話モードでも使えない。
- PYTHONSTARTUPの範囲<br>
通常のスクリプト実行ではなく、対話モード起動時に効く。
- アンダーバー<br>
直前に表示された式の結果を保持するため、通常変数名として代入すると混乱しやすい。

## 実施内容
### 対話モードの使用例
- 対話モードの起動<br>
引数なしで`python`または`python3`コマンドを実行すると、**対話モード**が起動する。どちらのコマンド名を使うかはOSや環境によって異なるため、先にバージョンを確認する。<br>
対話モードでは、入力待ち状態を表す「>>>」の後に直接コードを書いて実行することができる。<br>
以下の表示例はPython 3.6.4当時の実行結果であり、現在のPythonではバージョン表記、起動メッセージ、`sys.path`の内容などが異なる。基本操作は同じとなる。<br>
  ```bash
  $ python -V    # バージョン確認
   Python 3.6.4
  $ python    # 対話モード起動 (マイナーバージョンまでを指定しても可)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>>
  ```

- 対話モードの実行<br>
例えば、`sys.path`を確認したい場合、実際のコーディングと同じ要領で`sys`をインポート後、`sys.path`を実行することで、結果（pathの一覧）が表示される。<br>
  ```bash
  $ python    # 対話モード起動 (マイナーバージョンまで指定した python3.6 でも同じ動作)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import sys
   >>> sys.path
   ['', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', 
   '/var/www/vops/lib64/python3.6/site-packages','/var/www/vops/lib/python3.6/site-packages']
   >>>
  ```

- 対話モードの終了<br>
`exit()`を実行する。Unix系OSでは「Ctrl」+「D」、Windowsでは「Ctrl」+「Z」を押してから「Enter」でも終了できる。<br>
  ```bash
  $ python
   Python 3.6.4 (default, Dec 19 2017, 14:48:12)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> exit()
  ```

### 環境変数（PYTHONSTARTUP）の設定
対話モードでは、環境変数`PYTHONSTARTUP`に指定したスクリプトを最初に実行する。<br>
以下は、簡単な例として上記、**対話モードの実行**で記述した`sys.path`を`import sys`なしで実行できるように事前に環境変数`PYTHONSTARTUP`に設定する手順。<br>

- 環境変数未設定で`sys.path`を実行<br>
  ```bash
  $ python
   Python 3.6.4 (default, Dec 19 2017, 14:48:12)
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> sys.path
   Traceback (most recent call last):
     File "<stdin>", line 1, in <module>
   NameError: name 'sys' is not defined
   >>>
  ```
  `sys`をインポートしていないので当然エラーが発生する。

- **PYTHONSTARTUP**に`import sys`を追記<br>
ホームディレクトリに`.pythonstartup`を作成後、環境変数「PYTHONSTARTUP」に`.pythonstartup`を設定し、`import sys`を追記する。<br>
  ```bash
  $ touch  ~/.pythonstartup    # 空ファイル新規作成
  $ vim  ~/.pythonstartup    # import sys を追記
   import sys
  $ export PYTHONSTARTUP="$HOME/.pythonstartup"    # 起動時スクリプトのパスを設定
  ```
  `export`の効果は現在のシェルに限られる。常に有効にする場合は、利用しているシェルに応じて`.zshrc`や`.bashrc`などへ同じ設定を記述する。

- 再度対話モードで`sys.path`を実行<br>
  ```bash
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

### その他、対話モードの補足
- 直前に表示された式の結果を参照する<br>
対話モードでは、最後に**表示された式の結果**が`_`（アンダーバー）に保持される。<br>`_`を評価しても直前のコードを再実行するわけではなく、保存されている値を参照する。<br>明示的に`_`へ代入するとこの用途で扱いにくくなるため、通常の変数名には使わない。<br>
  ```bash
  $ python
   [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
   Type "help", "copyright", "credits" or "license" for more information.
   >>> import sys
   >>> sys.path
   ['', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', 
   '/var/www/vops/lib64/python3.6/site-packages', '/var/www/vops/lib/python3.6/site-packages']
   >>> _
   ['', '/usr/lib64/python36.zip', '/usr/lib64/python3.6', '/usr/lib64/python3.6/lib-dynload', 
   '/var/www/vops/lib64/python3.6/site-packages', '/var/www/vops/lib/python3.6/site-packages']
   >>>
  ```

- 任意のファイルを実行後、対話モードを起動<br>
**-i**オプションでファイルパスを指定すると、対話モードに入る前に任意のファイルを実行できる。<br>
  ```bash
  $ python -i example.py
  >>>
  ```
  `-i`でスクリプト実行後に対話モードへ入る場合、`PYTHONSTARTUP`のファイルは読み込まれない点に注意する。

- **IPython**の導入<br>
標準の対話モードを拡張した**IPython**というパッケージもある。<br>
  IPythonをインストールすると、TABキーによる補完、入力履歴、シェルコマンド、Pythonデバッガー（Pdb）との連携などを利用できる。<br>
  ```bash
  $ python -m pip install ipython
  ```

- Pythonの設計原則（The Zen of Python）<br>
対話モードで`import this`を実行すると、Tim Petersがまとめた「The Zen of Python」を確認できる。<br>全文を覚えるものではなく、可読性、明示性、単純さ、名前空間など、Pythonコードを設計・レビューするときの判断軸として読むと役立つ。背景と原文はPEP 20で確認できる。

## まとめ
- Pythonの対話モードは、小さなコードをすぐ試すための実験環境になる。
- PYTHONSTARTUPを使うと、起動時に共通処理を読み込める。
- バージョンや環境変数の違いに注意すると、環境調査にも使いやすい。

### 参考文献
- [Python公式ドキュメント - コマンドラインと環境：PYTHONSTARTUP](https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONSTARTUP)
- [Python公式チュートリアル - Pythonを電卓として使う](https://docs.python.org/ja/3/tutorial/introduction.html#using-python-as-a-calculator)
- [Python公式ドキュメント - sys.path](https://docs.python.org/ja/3/library/sys.html#sys.path)
- [IPython公式ドキュメント - Using IPython for interactive work](https://ipython.readthedocs.io/en/stable/interactive/index.html)
- [Python Enhancement Proposals - PEP 20：The Zen of Python](https://peps.python.org/pep-0020/)
