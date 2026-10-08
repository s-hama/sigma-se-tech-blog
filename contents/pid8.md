## タイトル
Python - 対話モード：PYTHONSTARTUPと起動時設定の使い方

## 概要

Pythonの対話モードとPYTHONSTARTUPによる起動時設定を整理する。

対話モードで使えた名前がスクリプトでは未定義になる例を、起動方法を変えて確かめる。自動で読み込まれた設定とファイル自身に必要なimportを分け、別の起動方法でも再現できるコードにする。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [対話モードの使用例](#対話モードの使用例)<br>
  対話モードの使用例をコードや具体例で確認。
- [環境変数（PYTHONSTARTUP）の設定](#環境変数pythonstartupの設定)<br>
  設定手順と通常起動・スクリプト実行・-iによる違いを比較。
- [その他、対話モードの補足](#その他対話モードの補足)<br>
  直前の実行結果や組込みヘルプなど、対話モードの便利な機能を確認。

## 対象環境と利用上の注意

- 本文記載時の環境<br>
掲載した出力はCentOS 7上のPython 3.6.4を利用した当時の例。
- 確認時期<br>
2026年9月にPythonの公式資料と照合。起動方法の比較例はPython 3.12.2で確認。<br>
CentOS 7・Python 3.6.4当時の起動表示は履歴として残しており、同じ環境では再実行していない。
- 現在そのまま利用できない箇所<br>
起動メッセージ、実行コマンド名、`sys.path`、シェルの起動設定はOS・Python・仮想環境で異なる。<br>
出力値やパスは現在の環境で読み替える。

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
引数なしで`python`または`python3`コマンドを実行すると、**対話モード**が起動。どちらのコマンド名を使うかはOSや環境によって異なるため、先にバージョンを確認。<br>
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
`exit()`を実行。Unix系OSでは「Ctrl」+「D」、Windowsでは「Ctrl」+「Z」を押してから「Enter」でも終了できる。<br>
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
  `sys`をインポートしていないので当然エラーが発生。

- **PYTHONSTARTUP**に`import sys`を追記<br>
ホームディレクトリに`.pythonstartup`を作成後、環境変数「PYTHONSTARTUP」に`.pythonstartup`を設定し、`import sys`を追記する。<br>
  ```bash
  $ touch  ~/.pythonstartup    # 空ファイル新規作成
  $ vim  ~/.pythonstartup    # import sys を追記
   import sys
  $ export PYTHONSTARTUP="$HOME/.pythonstartup"    # 起動時スクリプトのパスを設定
  ```
  `export`の効果は現在のシェルに限られる。常に有効にする場合は、利用しているシェルに応じて`.zshrc`や`.bashrc`などへ同じ設定を記述。

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

- 対話モードで使えたsysがスクリプトでは未定義になる理由<br>
  普段の設定と分けて確認するため、作業ディレクトリに次の2ファイルを作る。`startup_check.py`は起動時スクリプトである。

  ```python
  import sys
  print("startup loaded")
  ```

  `check_script.py`は、名前`sys`が現在のグローバル名前空間にあるかを調べる。

  ```python
  print("sys available:", "sys" in globals())
  ```

  Unix系シェルで次のように起動する。環境変数は各コマンドの実行時だけ指定する。以下はPythonの起動メッセージを省いた操作例である。

  ```text
  $ PYTHONSTARTUP="$PWD/startup_check.py" python3
  startup loaded
  >>> "sys" in globals()
  True
  >>> exit()

  $ PYTHONSTARTUP="$PWD/startup_check.py" python3 check_script.py
  sys available: False

  $ PYTHONSTARTUP="$PWD/startup_check.py" python3 -i check_script.py
  sys available: False
  >>> "sys" in globals()
  False
  >>> exit()
  ```

  | 起動方法 | PYTHONSTARTUPの実行 | この例のsys |
  | --- | --- | --- |
  | 通常の対話起動 | 実行される | 起動時スクリプトが定義する |
  | ファイルを指定して実行 | 実行されない | 未定義 |
  | -iでファイル実行後に対話へ移行 | 実行されない | ファイルにもimportがないので未定義 |

  対話中に`sys.path`が使えても、その行だけをファイルへ移せば同じ条件で動くとは限らない。`check_script.py`でsysを使うなら先頭に`import sys`を記述する。必要なimportをファイル自身にそろえ、新しいプロセスで実行して確認する。

### その他、対話モードの補足
- 直前に表示された式の結果を参照する<br>
対話モードでは、最後に**表示された式の結果**が`_`（アンダーバー）に保持される。<br>`_`を評価しても直前のコードを再実行するわけではなく、保存されている値を参照。<br>明示的に`_`へ代入するとこの用途で扱いにくくなるため、通常の変数名には使わない。<br>
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
  `-i`でスクリプト実行後に対話モードへ入る場合、`PYTHONSTARTUP`のファイルは読み込まれない点に注意。

- **IPython**の導入<br>
標準の対話モードを拡張した**IPython**というパッケージもある。<br>
  IPythonをインストールすると、TABキーによる補完、入力履歴、シェルコマンド、Pythonデバッガー（Pdb）との連携などを利用できる。<br>
  ```bash
  $ python -m pip install ipython
  ```

- Pythonの設計原則（The Zen of Python）<br>
対話モードで`import this`を実行すると、Tim Petersがまとめた「The Zen of Python」を確認できる。<br>全文を覚えるものではなく、可読性、明示性、単純さ、名前空間など、Pythonコードを設計・レビューするときの判断軸として読むと役立つ。背景と原文はPEP 20で確認できる。

## まとめ

- PYTHONSTARTUPは通常の対話起動時に実行される。ファイルの実行時や-iによる実行後の対話移行では読み込まれない。
- 対話環境で使える名前がスクリプトにもあるとは限らない。必要なimportをファイル自身に記述し、新しいプロセスで確認する。
- 対話モードの_は直前に表示した式の結果を参照する。コードを再実行する機能とは区別する。

### 参考文献
- [Python 3 ドキュメント「コマンドラインと環境：PYTHONSTARTUP」（日本語・公式仕様）](https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONSTARTUP)
- [Python 3 チュートリアル「Pythonを電卓として使う」（日本語・公式入門）](https://docs.python.org/ja/3/tutorial/introduction.html#using-python-as-a-calculator)
- [Python 3 ドキュメント「sys.path」（日本語・モジュール検索パス仕様）](https://docs.python.org/ja/3/library/sys.html#sys.path)
- [IPython Documentation, Using IPython for interactive work（英語・対話環境の公式解説）](https://ipython.readthedocs.io/en/stable/interactive/index.html)
- [Python Enhancement Proposals, PEP 20：The Zen of Python（英語・設計指針原文）](https://peps.python.org/pep-0020/)
