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

### その他、対話モードの補足
- 最後に実行されたコードを再度実行する<br>
最後に実行したコードは、変数_（アンダーバー）に格納されているため、_（アンダーバー）を実行することで再実行できる。<br>
  ```
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
  ```
  $ python -i example.py
  >>>
  ```

- **IPython**の導入<br>
対話モードをデバッガーのように利用できる**IPython**というパッケージもある。<br>
IPythonをインストールするとTABキーでの補完、シェルコマンドの使用、pythonデバッガー(pdb)との連携ができるようになる。<br>
  ```
  $ pip install ipython
  ```

- Python開発者の心構え（The Zen of Python）<br>
対話モードでも`import this`で原文確認できる。<br>
以下は、**The Zen of Python**は、Pythonの開発者の一人「Tim Peters」によって書かれた**Pythonらしさ**を端的にまとめた文章。<br>
  - 原文
    ```
    $ python
    Python 3.6.4 (default, Dec 19 2017, 14:48:12)
    [GCC 4.8.5 20150623 (Red Hat 4.8.5-16)] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>> import this
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    Explicit is better than implicit.
    Simple is better than complex.
    Complex is better than complicated.
    Flat is better than nested.
    Sparse is better than dense.
    Readability counts.
    Special cases aren't special enough to break the rules.
    Although practicality beats purity.
    Errors should never pass silently.
    Unless explicitly silenced.
    In the face of ambiguity, refuse the temptation to guess.
    There should be one-- and preferably only one --obvious way to do it.
    Although that way may not be obvious at first unless you're Dutch.
    Now is better than never.
    Although never is often better than *right* now.
    If the implementation is hard to explain, it's a bad idea.
    If the implementation is easy to explain, it may be a good idea.
    Namespaces are one honking great idea -- let's do more of those!
    ```

  - 和訳
    ```
    The Zen of Python, by Tim Peters

    Beautiful is better than ugly.
    醜いより美しいほうがいい。
    Explicit is better than implicit.
    暗示するより明示するほうがいい。
    Simple is better than complex.
    複雑であるよりは平易であるほうがいい。
    Complex is better than complicated.
    それでも、込み入っているよりは複雑であるほうがまし。
    Flat is better than nested.
    ネストは浅いほうがいい。
    Sparse is better than dense.
    密集しているよりは隙間があるほうがいい。
    Readability counts.
    読みやすいことは善である。
    Special cases aren't special enough to break the rules.
    特殊であることはルールを破る理由にならない。
    Although practicality beats purity.
    しかし、実用性を求めると純粋さが失われることがある。
    Errors should never pass silently.
    エラーは隠すな、無視するな。
    Unless explicitly silenced.
    ただし、わざと隠されているのなら見逃せ。
    In the face of ambiguity, refuse the temptation to guess.
    曖昧なものに出逢ったら、その意味を適当に推測してはいけない。
    There should be one-- and preferably only one --obvious way to do it.
    何かいいやり方があるはずだ。誰が見ても明らかな、たったひとつのやり方が。
    Although that way may not be obvious at first unless you're Dutch.
    そのやり方は一目見ただけではわかりにくいかもしれない。オランダ人にだけわかりやすいなんてこともあるかもしれない。
    Now is better than never.
    ずっとやらないでいるよりは、今やれ。
    Although never is often better than *right* now.
    でも、今"すぐ"にやるよりはやらないほうがマシなことが多い。
    If the implementation is hard to explain, it's a bad idea.
    コードの内容を説明するのが難しいのなら、それは悪い実装である。
    If the implementation is easy to explain, it may be a good idea.
    コードの内容を容易に説明できるのなら、おそらくそれはよい実装である。
    Namespaces are one honking great idea -- let's do more of those!
    名前空間は優れたアイデアであるため、積極的に利用すべきである。
    ```
