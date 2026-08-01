## タイトル
Python - 標準デバッガー（Pdb）：基本操作とステップ実行

## 概要

Python標準デバッガーであるPdbの使い方を、ブレークポイント、ステップ実行、変数確認を中心に整理する。

Pdbを使うと、print文だけでは追いにくい処理の流れを、停止位置ごとに確認できる。<br>関数の中へ入るのか、次の行へ進むのか、変数の値をどう見るのかを押さえると、原因調査がしやすくなる。

## この記事の構成
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [Pdbの使用例](#pdbの使用例)<br>
  Pdbの使用例をコードや具体例で確認。
- [Pdbの基本操作方法](#pdbの基本操作方法)<br>
  Pdbの基本操作方法をコードや具体例で確認。

## 作業時の注意点

- stepとnext<br>
stepは関数の中へ入り、nextは関数呼び出しを一行として進める。
- 停止位置<br>
set_trace()を書いた行そのものではなく、その次の実行行で止まる。
- 変数のスコープ<br>
現在停止している位置から見える変数だけを確認できる。
- 消し忘れ<br>
breakpoint()やpdb.set_trace()を本番コードへ残さない。

## 実施内容
### Pdbの使用例
- 説明用のサンプルプログラムを作成<br>
説明用に下記`debug_example.py`を作成。<br>
  ```python
  def add(a, b, c):
      return a + b + c


  breakpoint()
  step = 0
  step = add(1, 2, 3)
  step = add(4, 5, 6)
  print(step)
  ```
  `breakpoint()`はPython 3.7以降で利用でき、既定では`pdb.set_trace()`を呼び出す。<br>Python 3.6以前では、`import pdb; pdb.set_trace()`を同じ位置へ記述。

- `debug_example.py`を実行<br>
`breakpoint()`が実行されると、その次に実行する`step = 0`の行で止まり、入力待ちを表す`(Pdb)`が表示される。
  ```bash
  $ python debug_example.py
   > /path/to/debug_example.py(6)<module>()
   -> step = 0
   (Pdb)
  ```

- `next`と`step`を使い分けて値を確認<br>
`n`は現在の関数内の次の行まで進み、`s`は呼び出した関数の内部へ入る。<br>`a`で現在の関数の引数を、`p <式>`で式の評価結果を確認できる。<br>以下は操作の流れを抜粋した例となる。
  ```bash
  (Pdb) n       # step = 0を実行し、次の行へ進む
  (Pdb) s       # add(1, 2, 3)の内部へ入る
   --Call--
   > /path/to/debug_example.py(1)add()
   -> def add(a, b, c):
  (Pdb) a       # 現在の関数の引数を表示
  a = 1
  b = 2
  c = 3
  (Pdb) r       # 現在のadd関数がreturnするまで実行
   --Return--
   > /path/to/debug_example.py(2)add()->6
   -> return a + b + c
  (Pdb) n       # 呼び出し元へ戻り、次の行まで進む
  (Pdb) p step
  6
  (Pdb) n       # 2回目のaddは内部へ入らず実行
  (Pdb) p step
  15
  ```

### Pdbの基本操作方法
以下、よく使用するPdbコマンド。
- [`s`] or [`step`]<br>
現在行を実行し、呼び出した関数の内部を含む、次に停止可能な位置で止まる。

- [`n`] or [`next`]<br>
現在行を実行し、現在の関数内の次の行、または現在の関数が戻る位置で止まる。<br>呼び出した関数の内部では停止しない。

- [`r`] or [`return`]<br>
現在の関数が戻るまで実行。

- [`c`] or [`continue`]<br>
次回の**ブレークポイントまで停止せず**実行。

- [`l`] or [`list`]<br>
現在停止行の**前後のソース**を表示。

- [`a`] or [`args`]<br>
現在停止している**関数の引数**を表示。

- [**p <式>**]<br>
現在のコンテキストで式を評価し、結果を表示。

- [`q`] or [`quit`]<br>
デバッグ中のプログラムを終了。

## まとめ
- PdbはPython標準のデバッガーで、処理を止めながら変数や流れを確認できる。
- step、next、return、continueの違いを押さえると、調査しやすくなる。
- breakpoint()やpdb.set_trace()は便利だが、確認後はコードから外す。

### 参考文献
- [Python 3 ドキュメント「pdb：Pythonデバッガー」（日本語・公式操作仕様）](https://docs.python.org/ja/3/library/pdb.html)
- [Python 3 ドキュメント「breakpoint()」（日本語・組込み関数仕様）](https://docs.python.org/ja/3/library/functions.html#breakpoint)
- [Python 3 ドキュメント「PYTHONBREAKPOINT」（日本語・環境変数仕様）](https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONBREAKPOINT)
