## タイトル
Python - 高階関数と畳込み : map, filter, reduce

## 目的
この記事では、Pythonで使用する高階関数（map, filter, reduce）の基本的な使い方について記載する。

## 高階関数の説明と実装サンプル

### 高階関数とは

Pythonでは、関数もオブジェクトと同じように捉えるため、関数を引数や戻り値に指定したり、関数に対して別の関数やオブジェクトを代入することができる。

この性質を利用して、関数を引数に持ったり、関数を戻り値で返す関数を**高階関数**（higher-order function）という。

以下、**関数を引数に持つ場合**、**戻り値に持つ場合**、**引数と戻り値の両方に持つ場合**それぞれの簡単な実装サンプルを記載する。

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
        >>> #  h_order_func(5)の戻り値である add_param(y) に 10 を指定して実行
        >>> h_order_func(5)(10)
        15
        >>>
        >>> #  ※ h_order_func(5) の 戻り値は、下記の add_param(y) の定義となり、x が 5 に置き換わっている状態となる
        ...     def add_param(y):
        ...         return 5 + y
        >>>
    ```

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
        >>> #  h_order_func(add_five)の戻り値である add_func(x, y) に 1, 2 を指定して実行
        >>> h_order_func(add_five)(1, 2)
        8
        >>>
        >>> #  ※ h_order_func(add_five) の 戻り値は、下記の add_func(x, y) の定義となり、関数 func(x) が 関数 add_five(x) に置き換えられた状態となる
        ...     def add_func(x, y):
        ...         return x + 5 + y
        >>>
    ```

以降、高階関数 `map`, `filter`, `reduce` を簡単な実装サンプルで解説する。

### map（要素別の演算）

`map(function, iterable)` は、第 \\(2\\) 引数（iterable）に指定したイテレータ（各要素の反復処理ができるインターフェース）の各要素に対して、第 \\(1\\)引数（function）を実行した結果をイテレータで返す。

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

### filter（指定要素の除外）

`filter(function, iterable)` は、第 \\(2\\) 引数（iterable）に指定したイテレータの各要素に対して、第 \\(1\\) 引数（function）の実行結果がTrueとなるイテレータを返す。

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

- 上記の実装サンプルのmapを使用せず内包表記で記述
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

※ **内包表記** は、**畳込み演算** に対応していないため、**reduce** は、内包表記で表現できない。

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

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
