## タイトル
Python - 標準デバッガー（Pdb）：基本操作とステップ実行

## 概要

Python標準デバッガーであるPdbの使い方を、ブレークポイント、ステップ実行、変数確認を中心に整理する。

Pdbを使うと、print文だけでは追いにくい処理の流れを、停止位置ごとに確認できる。関数の中へ入るのか、次の行へ進むのか、変数の値をどう見るのかを押さえると、原因調査がしやすくなる。

## この記事で扱うこと
- pdb.set_trace()で処理を止める方法。
- ステップ実行で処理の流れを追う方法。
- pコマンドで変数の値を確認する方法。
- step、next、return、continueの違い。
- listやargsで停止位置の情報を見る方法。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| サンプルコード | 小さな関数で停止位置と変数の変化を確認する。 |
| ブレークポイント | pdb.set_trace()を置いた直後から確認を始める。 |
| ステップ実行 | 関数内へ入るか、次行へ進むかを使い分ける。 |
| 変数確認 | p 変数名で現在値を表示する。 |
| 終了操作 | qでデバッガーを抜ける。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| stepとnext | stepは関数の中へ入り、nextは関数呼び出しを一行として進める。 |
| 停止位置 | set_trace()を書いた行そのものではなく、その次の実行行で止まる。 |
| 変数のスコープ | 現在停止している位置から見える変数だけを確認できる。 |
| 消し忘れ | pdb.set_trace()を本番コードへ残さない。 |

## 実施内容
### Pdbの使用例
- 説明用のサンプルプログラムを作成<br>
説明用に下記`debug_example.py`を作成する。<br>
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

## 実務とのつながり
- 不具合調査<br>
    条件分岐や関数呼び出しの流れを確認できる。
- 値の追跡<br>
    途中の変数が想定通りかを確認できる。
- 学習用途<br>
    Pythonコードがどの順番で実行されるかを理解しやすい。

## まとめ
- PdbはPython標準のデバッガーで、処理を止めながら変数や流れを確認できる。
- step、next、return、continueの違いを押さえると、調査しやすくなる。
- pdb.set_trace()は便利だが、確認後はコードから外す。
