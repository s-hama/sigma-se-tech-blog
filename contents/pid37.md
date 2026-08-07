## タイトル
Python - 高階関数と畳込み：map・filter・reduceの使い方

## 概要
Pythonの高階関数として、map、filter、reduceの基本的な使い方を整理する。
高階関数は、関数を引数として受け取ったり、関数を戻り値として返したりする関数を指す。map、filter、reduceを理解すると、繰り返し処理を「変換」「抽出」「集約」という観点で整理できる。
ここでは、通常の関数、lambda式、畳込み処理を実行例で確認する。

## この記事の構成
- [高階関数とは](#高階関数とは)<br>
  高階関数の意味と基本的な考え方を整理。
- [map（要素別の演算）](#map要素別の演算)<br>
  map（要素別の演算）の仕組みと要点を具体例から整理。
- [filter（条件に合う要素の抽出）](#filter条件に合う要素の抽出)<br>
  条件を満たす元の要素だけを遅延評価で取り出す方法を整理。
- [reduce（畳込み演算）](#reduce畳込み演算)<br>
  reduce（畳込み演算）の仕組みと要点を具体例から整理。

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

- 上記の実装サンプルのmapを使用せず内包表記で記述
    ```python
    $ python
        >>> # map(triple, list_a) と同義
        >>> result = (triple(p) for p in list_a)
        >>> print(list(result))
        [3, 6, 9, 12, 15]
        >>>
    ```

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

- 上記の実装サンプルのfilterを使用せず内包表記で記述
    ```python
    $ python
        >>> # filter(is_plus, list_a) と同義
        >>> result = (p for p in list_a if is_plus(p))
        >>> print(list(result))
        [1, 2]
        >>>
    ```

### reduce（畳込み演算）

`reduce(function, iterable [, initializer])` は、**畳み込み演算** と呼ばれ、第 \\(2\\) 引数（iterable）に指定したイテレータの2つの要素に対して、左から順に第 \\(1\\) 引数（function）を実行していき、これをイテレータの最終要素まで繰り返し、1つの結果を返す。

そのため、第 \\(1\\) 引数（function）の引数は、**必ず2つ** であることが前提となる。

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


## まとめ
- 高階関数は関数を値として扱い、mapは変換、filterは抽出、reduceは集約に使う。
- mapやfilterの戻り値はイテレータなので、リストが必要な場合はlistへ変換。
- 複雑な処理はfor文や内包表記の方が読みやすい場合があり、集約にはsumなどの専用関数も含めて使い分ける。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 関数型プログラミング HOWTO（日本語・関数型処理の公式解説）](https://docs.python.org/ja/3/howto/functional.html)
- [Python公式ドキュメント - map（日本語・mapの公式仕様）](https://docs.python.org/ja/3/library/functions.html#map)
- [Python公式ドキュメント - filter（日本語・filterの公式仕様）](https://docs.python.org/ja/3/library/functions.html#filter)
- [Python公式ドキュメント - functools.reduce（日本語・reduceの公式仕様）](https://docs.python.org/ja/3/library/functools.html#functools.reduce)
