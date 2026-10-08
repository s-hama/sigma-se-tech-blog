## タイトル
Python - 標準デバッガー（Pdb）：基本操作とステップ実行

## 概要

Python標準デバッガーPdbのブレークポイント、ステップ実行、変数確認を整理する。

基本操作を確認した後、合計が期待値と一致しないプログラムを調べる。関数へ渡された値と実際にループへ渡る範囲を比べ、原因を特定して修正後の結果を確認する。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [Pdbの使用例](#pdbの使用例)<br>
  基本操作から合計の取りこぼしを調べる手順へ進む。
- [Pdbの基本操作方法](#pdbの基本操作方法)<br>
  Pdbの基本操作方法をコードや具体例で確認。

## 対象環境と利用上の注意

- 本文記載時の環境<br>
Python 3.7以降の`breakpoint()`と標準デバッガーPdbを利用する例。<br>
Python 3.6以前の代替方法も併記。
- 確認時期<br>
2026年9月にPythonの公式資料と照合。合計の取りこぼしを調べる比較例はPython 3.12.2で実行確認。
- 現在そのまま利用できない箇所<br>
停止位置のパス、行番号、Pdbの表示形式はPythonのバージョンや対象ファイルで変わる。<br>
出力を固定値として使わず、操作コマンドと処理の流れを参照する。

## 作業時の注意点

- stepとnext<br>
stepは関数の中へ入り、nextは関数呼び出しを一行として進める。
- 停止位置<br>
この記事のPython 3.12.2の例では呼び出しの次の実行行で止まる。停止タイミングや表示はバージョンにより異なるため、矢印で示された行を確認する。
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
以下の表示例では`breakpoint()`の次に実行する`step = 0`の行で止まり、入力待ちを表す`(Pdb)`が表示される。
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

- 合計が600になるはずなのに300になる場合を調べる<br>
  次の`subtotal_bug.py`は末尾の要素を取りこぼす確認用プログラムである。100・200・300の合計を600と予想して実行する。

  ```python
  def subtotal(prices):
      total = 0
      for price in prices[:-1]:
          total += price
      return total


  prices = [100, 200, 300]
  breakpoint()
  actual = subtotal(prices)
  print(actual)
  ```

  `python subtotal_bug.py`で起動し、`actual = subtotal(prices)`の行で止まったら入力データを調べる。次は停止位置の表示を一部省いた操作例である。Pdbのコマンドにコメントを付けず順に入力する。

  ```text
  (Pdb) p prices
  [100, 200, 300]
  (Pdb) s
  (Pdb) a
  prices = [100, 200, 300]
  (Pdb) p prices[:-1]
  [100, 200]
  (Pdb) r
  --Return--
  > /path/to/subtotal_bug.py(5)subtotal()->300
  -> return total
  (Pdb) n
  (Pdb) p actual
  300
  (Pdb) c
  300
  ```

  呼び出し元のlistにも関数の引数にも300があるため、受け渡し時には失われていない。`prices[:-1]`は末尾を除くスライスなので、ループに渡った段階で300が外れている。`r`で戻り値が300であることを確認できる。

  関数を次のように直し、ブレークポイントを外して再実行する。

  ```python
  def subtotal(prices):
      total = 0
      for price in prices:
          total += price
      return total


  for prices in ([100, 200, 300], [300], []):
      print(subtotal(prices))
  ```

  ```text
  600
  300
  0
  ```

  複数要素に加え、1要素と空のlistでも期待値を確認する。Pdbでは「入力は正しいか」「どの式で期待とずれたか」を順に調べ、修正後はデバッガーなしでも結果を再現できる状態にする。

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

- Pdbでは停止位置の入力や途中結果を調べ、期待値との差が最初に現れる式を絞り込める。
- stepは関数へ入り、nextは現在の関数内を進める。argsで引数、pで式、returnで戻り値を確認する。
- 原因を修正した後はブレークポイントを外し、通常の入力と境界となる入力で結果を再確認する。

### 参考文献
- [Python 3 ドキュメント「pdb：Pythonデバッガー」（日本語・公式操作仕様）](https://docs.python.org/ja/3/library/pdb.html)
- [Python 3 ドキュメント「breakpoint()」（日本語・組込み関数仕様）](https://docs.python.org/ja/3/library/functions.html#breakpoint)
- [Python 3 ドキュメント「PYTHONBREAKPOINT」（日本語・環境変数仕様）](https://docs.python.org/ja/3/using/cmdline.html#envvar-PYTHONBREAKPOINT)
