## タイトル
Python - 標準デバッガー（Pdb）: 使用例と基本操作方法

## 目的
この記事では、Pythonの標準デバッガー（Pdb）の使用例と基本操作方法について説明する。

## 実施内容
### Pdbの使用例
- 説明用のサンプルプログラムを作成<br>
説明用に下記`debug_sample.py`を作成する。<br>
  ```python
  1 def add(a, b, c):
  2     return a + b + c
  3 
  4 step = 0
  5
  6 step = add(1, 2, 3)
  7 step = add(4, 5, 6)
  ```

- 4行目に`import pdb; pdb.set_trace()`を挿入<br>
この状態で4行目の直後となる6行目の`step = 0`がブレイクポイントとなる。
  ```python
  1 def add(a, b, c):
  2     return a + b + c
  3
  4 import pdb; pdb.set_trace()
  5
  6 step = 0
  7
  8 step = add(1, 2, 3)
  9 step = add(4, 5, 6)
  ```

- `debug_example.py`を実行<br>
6行目の`step = 0`で止まり、入力待ちを表す`(Pdb)`が表示される。
  ```bash
  $ python /var/www/vops/ops/macuos/debug_example.py
   > /var/www/vops/ops/macuos/debug_example.py(6)()
   -> step = 0
   (Pdb)
  ```

- ステップ実行でそれぞれ変数の値を確認<br>
以下、6行目～9行目までステップ実行し、最後に変数`step`の値を確認する。<br>
ステップ実行は、`s`、変数の確認は、**p <変数名>**を入力する。<br>
ステップ実行毎に`>`でどの行であるか、`->`で実行コードが確認できる。
  ```bash
  $ python /var/www/vops/ops/macuos/debug_example.py
   > /var/www/vops/ops/macuos/debug_example.py(6)()
   -> step = 0
   (Pdb) s    # ステップ実行のsを入力
   > /var/www/vops/ops/macuos/debug_example.py(8)()
   -> step = add(1, 2, 3)
   (Pdb) s    # ステップ実行のsを入力
   --Call--
   > /var/www/vops/ops/macuos/debug_example.py(1)add()
   -> def add(a, b, c):
   (Pdb) s    # ステップ実行のsを入力
   > /var/www/vops/ops/macuos/debug_example.py(2)add()
   -> return a + b + c
   (Pdb) s    # ステップ実行のsを入力
   --Return--
   > /var/www/vops/ops/macuos/debug_example.py(2)add()->6
   -> return a + b + c
   (Pdb) s    # ステップ実行のsを入力
   > /var/www/vops/ops/macuos/debug_example.py(9)()
   -> step = add(4, 5, 6)
   (Pdb) s    # ステップ実行のsを入力
   (Pdb) p step    # 変数「step」の確認
   15
  ```

### Pdbの基本操作方法
以下、よく使用するPdbコマンド。
- [`s`] or [`step`]<br>
ステップイン : **行単位**でステップ実行する。

- [`n`] or [`next`]<br>
ステップオーバー : **行単位**で実行する。
※ 関数の中は停止しない。

- [`r`] or [`return`]<br>
ステップアウト : 関数単位で実行する。
※ 実行中の関数が返るまで実行する。

- [`c`] or [`continue`]<br>
次回の**ブレークポイントまで停止せず**実行する。

- [`l`] or [`list`]<br>
現在停止行の**前後のソース**を表示する。

- [`a`] or [`largs`]<br>
現在停止している**関数の引数**を表示する。

- [**p <変数名>**]<br>
**変数の値**を表示する。

- [`q`] or [`quit`]<br>
**Pdbデバッガー**を終了する。
