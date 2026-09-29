## タイトル
Python - 高階関数と畳込み：map・filter・reduceの使い方

## 概要

高階関数とmap・filter・reduceを、変換・抽出・集約の操作として整理する。

mapやfilterを一度取り出した後の状態と、reduceが途中結果を次の計算へ渡す順序を確認する。結果を繰り返し使う必要があるか、空の入力をどう扱うかまで考えて関数を選ぶ。イテレータと畳込みの比較例はPython 3.12.2で確認。

## この記事の構成
- [高階関数とは](#高階関数とは)<br>
  高階関数の意味と基本的な考え方を整理。
- [map（要素別の演算）](#map要素別の演算)<br>
  変換が実行される時点と一度取り出した後の状態を確認。
- [filter（条件に合う要素の抽出）](#filter条件に合う要素の抽出)<br>
  元の要素を取り出す条件と結果を再利用する方法を確認。
- [reduce（畳込み演算）](#reduce畳込み演算)<br>
  減算の途中結果と初期値・空入力の関係を追う。

## 高階関数の説明と実装サンプル

### 高階関数とは

Pythonでは、関数もオブジェクトと同じように捉えるため、関数を引数や戻り値に指定したり、関数に対して別の関数やオブジェクトを代入することができる。

この性質を利用して、関数を引数に持ったり、関数を戻り値で返す関数を**高階関数**（higher-order function）という。

以下では、**関数を引数に持つ場合**、**戻り値に持つ場合**、**引数と戻り値の両方に持つ場合**それぞれの実装サンプルを確認する。

- 関数を引数に持つ高階関数
    ```python
    $ python
        >>> # 関数 p_func を引数に持つ、高階関数 h_order_func を定義
        >>> def h_order_func(p_func):
        ...     p_func()
        ...
        >>> # メッセージを出力する関数 print_msg を定義
        >>> def print_msg():
        ...     print('executed print_msg')
        ...
        >>> # 高階関数 h_order_func の引数に関数 print_msg を指定して実行
        >>> h_order_func(print_msg)
        executed print_msg
        >>>
    ```

- 関数を戻り値に持つ高階関数
    ```python
    $ python
        >>> # 関数 add_param を戻り値に持つ、高階関数 h_order_func を定義
        >>> def h_order_func(x):
        ...     def add_param(y):
        ...         return x + y
        ...     return add_param
        ...
        >>> # h_order_func(5)が返す関数を受け取り、10を指定して実行
        >>> add_five = h_order_func(5)
        >>> add_five(10)
        15
        >>>
    ```
    `h_order_func(5)`が返す関数は、外側の関数へ渡した`x = 5`を保持する。そのため、返された関数へ`10`を渡すと`5 + 10`が計算される。

- 関数を引数と戻り値の両方に持つ高階関数
    ```python
    $ python
        >>> # 関数 func を引数に持ち、戻り値に add_func 持つ、高階関数 h_order_func を定義
        >>> def h_order_func(func):
        ...     def add_func(x, y):
        ...         return func(x) + y
        ...     return add_func
        ...
        >>> # 5 を加算する関数 add_five を定義
        >>> def add_five(x):
        ...     return x + 5
        >>>
        >>> # h_order_func(add_five)が返す関数を受け取り、1と2を指定して実行
        >>> combined_func = h_order_func(add_five)
        >>> combined_func(1, 2)
        8
        >>>
    ```
    `h_order_func(add_five)`が返す関数では、`func(x)`として`add_five(x)`が呼ばれる。そのため、`combined_func(1, 2)`は`(1 + 5) + 2`となる。

以降、高階関数 `map`, `filter`, `reduce` を実装サンプルで解説する。

### map（要素別の演算）

`map(function, iterable)` は、第 \\(2\\) 引数に指定したイテラブルの各要素へ、第 \\(1\\)引数の関数を適用した結果を返す。戻り値は遅延評価されるmapイテレータとなる。

- 実装サンプル
    ```python
    $ python
        >>> # 第1引数の関数を定義（3倍にするだけ）
        >>> def triple(p):
        ...    return p * 3
        ...
        >>> # 第2引数のlist型を定義
        >>> list_a = [1, 2, 3, 4, 5]
        >>>
        >>> # mapを実行
        >>> result = map(triple, list_a)
        >>>
        >>> # map型のイテレータで返ってくる
        >>> print(result)
        <map object at 0x7f59b53cc5c0>
        >>>
        >>> # list型にキャストし、中身を確認
        >>> print(list(result))
        [3, 6, 9, 12, 15]
        >>>
    ```

- 上記の実装サンプルをラムダ式で記述
    ```python
    $ python
        >>> result = map(lambda x: x * 3, list_a)
        >>> print(list(result))
        [3, 6, 9, 12, 15]
        >>>
    ```

- 上記の実装サンプルをジェネレータ式で記述
    ```python
    $ python
        >>> # map(triple, list_a) と同義
        >>> result = (triple(p) for p in list_a)
        >>> print(list(result))
        [3, 6, 9, 12, 15]
        >>>
    ```

- mapを作る時点と結果を取り出す時点を分ける<br>
  ```python
  def to_number(raw):
      print("convert", raw)
      return int(raw)


  result = map(to_number, ["10", "20"])
  print("created")
  print(list(result))
  print(list(result))
  ```

  ```text
  created
  convert 10
  convert 20
  [10, 20]
  []
  ```

  `map()`を作っただけでは変換関数は呼ばれず、最初の`list(result)`が要素を取り出す時点で実行される。イテレータは読み進めた状態を持つので、取り出し終わった後の2回目は空になる。

  表示と集計などで結果を繰り返し使う場合は、最初に`numbers = list(map(int, raw_values))`のようにlistへ保存する。`numbers = [int(raw) for raw in raw_values]`でも同じ目的を表せる。一度ずつ順に処理する用途ではイテレータのまま扱える。

### filter（条件に合う要素の抽出）

`filter(function, iterable)` は、第 \\(2\\) 引数に指定したイテラブルの各要素を関数で判定し、結果がTrueとなる**元の要素**を返す。戻り値は遅延評価されるfilterイテレータとなる。

- 実装サンプル
    ```python
    $ python
        >>> # 第1引数の関数を定義（正であればTrueを返す）
        >>> def is_plus(p):
        ...    return p > 0
        ...
        >>> # 第2引数のlist型を定義
        >>> list_a = [-2, -1, 0, 1, 2]
        >>>
        >>> # filterを実行
        >>> result = filter(is_plus, list_a)
        >>>
        >>> # filter型のイテレータで返ってくる
        >>> print(result)
        <filter object at 0x7f59b53cc668>
        >>>
        >>> # list型にキャストし、中身を確認
        >>> print(list(result))
        [1, 2]
        >>>
    ```

- 上記の実装サンプルをラムダ式で記述
    ```python
    $ python
        >>> result = filter(lambda x: x > 0, list_a)
        >>> print(list(result))
        [1, 2]
        >>>
    ```

- 上記の実装サンプルをジェネレータ式で記述
    ```python
    $ python
        >>> # filter(is_plus, list_a) と同義
        >>> result = (p for p in list_a if is_plus(p))
        >>> print(list(result))
        [1, 2]
        >>>
    ```

- 抽出した結果を繰り返し使う<br>
  filterも一度取り出すと進むイテレータである。件数の確認と合計の両方に使うなら抽出結果を保存する。

  ```python
  values = [-2, -1, 0, 1, 2]
  positives = list(filter(lambda value: value > 0, values))
  print(positives)
  print(len(positives), sum(positives))
  ```

  ```text
  [1, 2]
  2 3
  ```

  この処理は`[value for value in values if value > 0]`というリスト内包表記でも書ける。変換するmapと異なり、filterが返すのは条件に合う元の要素である。

### reduce（畳込み演算）

`reduce(function, iterable [, initializer])`は**畳み込み演算**を行う関数である。入力を左から取り出し、累積した結果と次の要素に関数を適用して1つの結果を返す。

関数はこの2つの位置引数を受け取れる必要がある。

**第3引数**（initializer）は、初期値を指定することができる。
初期値を指定した場合、最初の演算は、**初期値** と第 \\(2\\) 引数（iterable）の先頭要素で第 \\(1\\) 引数（function）を実行する。

※ 内包表記には、複数要素を一つの値へ直接集約する構文はない。合計には`sum()`などの専用関数を優先し、一般的な畳込みが必要な場合に`reduce()`を検討する。

- 実装サンプル
    ```python
    $ python
        >>> # functoolsからインポート
        >>> from functools import reduce
        >>>
        >>> # 第1引数の関数を定義（差を返す）
        >>> def minus(p1, p2):
        ...     return p1 - p2
        ...
        >>> # 第2引数のlist型を定義
        >>> list_a = [-5, -4, -3, -2, -1]
        >>>
        >>> # minus と list_a で reduce を実行
        >>> print(reduce(minus, list_a))
        5
        >>>
        >>> # 第3引数に -6 を指定
        >>> result = reduce(minus, list_a, -6)
        >>> print(result)
        9
        >>>

    ```
- 上記の実装サンプルをラムダ式で記述
    ```python
    $ python
        >>> result = reduce(lambda x, y: x - y, list_a)
        >>> print(result)
        5
        >>>
    ```


- 減算の途中結果を追う<br>
  上の`[-5, -4, -3, -2, -1]`を使う例では、初期値なしなら先頭の-5が最初の累積値となる。

  | 手順 | 初期値なし | 初期値-6 |
  | --- | --- | --- |
  | 最初の計算 | -5 - (-4) = -1 | -6 - (-5) = -1 |
  | 次の計算 | -1 - (-3) = 2 | -1 - (-4) = 3 |
  | 次の計算 | 2 - (-2) = 4 | 3 - (-3) = 6 |
  | 次の計算 | 4 - (-1) = 5 | 6 - (-2) = 8 |
  | 最後の計算 | すでに終了 | 8 - (-1) = 9 |

  減算は括弧の位置で結果が変わる。reduceでは累積値を左側の引数にして計算を進めるため、初期値の有無は最初の計算だけでなく最終結果にも影響する。

- 空の入力と初期値<br>
  ```python
  from functools import reduce

  print(reduce(lambda total, value: total + value, [], 0))
  try:
      print(reduce(lambda total, value: total + value, []))
  except TypeError as error:
      print(type(error).__name__)
  print(sum([]))
  ```

  ```text
  0
  TypeError
  0
  ```

  初期値があれば空の入力でもその値を返せる。初期値なしでは最初の累積値が存在しないためエラーになる。合計なら`sum()`の方が意図を直接表せる。一般的な畳込みが必要な場合にreduceを選び、初期値と空入力で期待する結果を決める。

## まとめ

- mapは変換、filterは抽出、reduceは集約を表す。
- mapとfilterは要素を取り出すと処理が進む。結果を複数回使う場合はlistなどへ保存する。
- reduceは累積値と次の要素を左から順に計算する。初期値は結果と空入力の扱いに影響する。
- 合計にはsum()など目的を直接表す関数を選ぶ。変換・抽出は内包表記とも読みやすさを比較する。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 関数型プログラミング HOWTO（日本語・関数型処理の公式解説）](https://docs.python.org/ja/3/howto/functional.html)
- [Python公式ドキュメント - map（日本語・mapの公式仕様）](https://docs.python.org/ja/3/library/functions.html#map)
- [Python公式ドキュメント - filter（日本語・filterの公式仕様）](https://docs.python.org/ja/3/library/functions.html#filter)
- [Python公式ドキュメント - functools.reduce（日本語・reduceの公式仕様）](https://docs.python.org/ja/3/library/functools.html#functools.reduce)
