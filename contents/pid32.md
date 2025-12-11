## タイトル
Python - 組込みデータ型まとめ : set, bytes, bytearray, fileobject

## 目的
この記事では、Pythonが扱う組込みデータ型（set、bytes、bytearray、fileobject）の基本的な操作方法について記載する。

## 各データ型の操作方法

### set型 : 集合

set型は、**重複した要素**がなく、要素に**順番を**持たない配列のような集合。

記述は、dict型と同じ中カッコ**{}**で囲み、**キーが無い状態**（値のみ）で定義する。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: 同一アドレスで変更可](<https://sigma-se.com/detail/29/#:~:text=%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88mutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)

- 定義例
    ```python
    $ python
    >>> # 1 ～ 5 の数値を昇順で定義
    >>> set_a = {1, 2, 3, 4, 5}
    >>> print(set_a)
    {1, 2, 3, 4, 5}
    >>> type(set_a)
    <class 'set'>
    >>>
    >>> # 1 ～ 5 の数値を順不同、重複ありで定義
    >>> set_b = {5, 2, 3, 4, 1, 2, 3}
    >>> print(set_b)     # 重複は無視される
    {1, 2, 3, 4, 5}
    >>> type(set_b)
    <class 'set'>
    >>>
    >>> # イミュータブルな型であれば、異なる型でも定義できる
    >>> set_c = {1, 'one', ('two', 2)}
    >>> print(set_c)
    {'one', 1, ('two', 2)}
    >>> type(set_c)
    <class 'set'>
    >>>
    >>> # 【注意】空集合 {} で定義するとdict型となる
    >>> set_d = {}
    >>> print(set_d)
    {}
    >>> type(set_d)
    <class 'dict'>
    >>>
    >>> # コンストラクタを用いて空集合を定義
    >>> set_e = set()
    >>> print(set_e)
    set()
    >>> type(set_e)
    <class 'set'>
    >>>
    ```

- set型要素の追加、削除<br>
※ 他の型とは違い**pop**は、ランダムで要素を削除することに注意。
    ```python
    $ python
    >>> # 要素を追加
    >>> set_a = {1, 2, 3, 4}
    >>> set_a.add(5)    # int型で追加
    >>> set_a.add('str add')    # str型で追加
    >>> print(set_a)
    {1, 2, 3, 4, 5, 'str add'}
    >>>
    >>> # 指定した要素を削除
    >>> # ※要素が存在しない場合はエラー
    >>> set_b = {1, 2, 3, 4, 5}
    >>> set_b.remove(3)
    >>> print(set_b)
    {1, 2, 4, 5}
    >>>
    >>> set_c = {1, 2, 3, 4, 5}
    >>> set_c.remove(100)    # 要素がないためエラー
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    KeyError: 100
    >>>
    >>> # 指定した要素を削除（要素が存在しない場合も正常終了）
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_d.discard(2)
    >>> print(set_d)
    {1, 3, 4, 5}
    >>> set_d.discard(100)    # 要素が存在しない場合もエラーにならずなにもしない
    >>> print(set_d)
    {1, 3, 4, 5}
    >>>
    >>> # すべての要素を削除
    >>> set_e = {1, 2, 3, 4, 5}
    >>> set_e.clear()
    >>> print(set_e)
    set()
    >>>
    >>> # ランダムで要素を削除
    >>> set_f = {1, 2, 3, 4, 5}
    >>> print(set_f.pop())
    1
    >>> print(set_f)
    {2, 3, 4, 5}
    >>>
    ```

- 集合演算
  - 和集合（| 演算子 or union）
    ```python
    $ python
    >>> # | 演算子を用いた和集合
    >>> set_a = {1, 2, 3}
    >>> set_b = {3, 4, 5}
    >>> set_c = set_a | set_b
    >>> print(set_c)
    {1, 2, 3, 4, 5}
    >>>
    >>> # unionを用いた和集合
    >>> set_d = {1, 2, 3}
    >>> set_e = {3, 4, 5}
    >>> set_f = set_d.union(set_e)
    >>> print(set_f)
    {1, 2, 3, 4, 5}
    >>>
    >>> # unionを用いた和集合（複数の引数を指定できる）
    >>> set_g = {1, 2, 3}
    >>> set_h = {3, 4, 5}
    >>> set_i = {5, 6, 7}
    >>> set_j = set_g.union(set_h, set_i)
    >>> print(set_j)
    {1, 2, 3, 4, 5, 6, 7}
    >>>
    ```

  - 積集合（& 演算子 or intersection）
    ```python
    $ python
    >>> # & 演算子を用いた積集合
    >>> set_a = {1, 2, 3}
    >>> set_b = {3, 4, 5}
    >>> set_a = set_a & set_b
    >>> print(set_a)
    {3}
    >>>
    >>> # intersectionを用いた積集合
    >>> set_c = {1, 2, 3}
    >>> set_d = {3, 4, 5}
    >>> set_c = set_c.intersection(set_d)
    >>> print(set_c)
    {3}
    >>>
    >>> # intersectionを用いた積集合（複数の引数を指定できる）
    >>> set_e = {1, 2, 3}
    >>> set_f = {3, 4, 5}
    >>> set_g = {1, 3, 5}
    >>> set_h = set_e.intersection(set_f, set_g)
    >>> print(set_h)
    {3}
    >>>
    ```

  - 差集合（- 演算子 or difference）
    ```python
    $ python
    >>> # - 演算子を用いた差集合
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5}
    >>> set_c = set_a - set_b
    >>> print(set_c)
    {1, 2, 3}
    >>>
    >>> # differenceを用いた差集合
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {4, 5}
    >>> set_f = set_d.difference(set_e)
    >>> print(set_f)
    {1, 2, 3}
    >>>
    >>> # differenceに複数パラメータを指定
    >>> set_g = {1, 2, 3, 4, 5}
    >>> set_h = {4, 5}
    >>> set_i = {1}
    >>> set_j = set_g.difference(set_h, set_i)
    >>> print(set_j)
    {2, 3}
    >>>
    ```

  - 対象差集合（^ 演算子 or symmetric_difference）<br>
  積集合の逆（どちらか一方にあるものを取得する）で排他的論理和（XOR）と同義。
    ```python
    $ python
    >>> # ^ 演算子を用いた対象差集合
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5, 6, 7}
    >>> set_c = set_a ^ set_b
    >>> print(set_c)
    {1, 2, 3, 6, 7}
    >>>
    >>> # symmetric_differenceを用いた対象差集合
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {4, 5, 6, 7}
    >>> set_f = set_d.symmetric_difference(set_e)
    >>> print(set_f)
    {1, 2, 3, 6, 7}
    >>>
    >>> # symmetric_differenceに複数のパラメータは指定できない
    >>> set_g = {1, 2, 3, 4, 5}
    >>> set_h = {4, 5, 6, 7}
    >>> set_j = {8, 9, 10}
    >>> set_k = set_g.symmetric_difference(set_h, set_j)
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: symmetric_difference() takes exactly one argument (2 given)
    >>>
    ```

  - 部分集合の判定（<=演算子 or issubset）<br>
  ※ 以下、サンプルコードでは集合`set_b`が集合`set_a`の部分集合であるかを判定している。
    ```python
    $ python
    >>> # <= を用いた判定
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5}
    >>> set_c = set_b <= set_a
    >>> print(set_c)
    True
    >>>
    >>> # issubsetを用いた判定
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {4, 5}
    >>> set_f = set_e.issubset(set_d)
    >>> print(set_f)
    True
    >>>
    ```

  - 上位集合か判定（>= or issuperset）<br>
  ※ 以下、サンプルコードでは、集合`set_b`が集合`set_a`の上位集合であるかを判定している。
    ```python
    $ python
    >>> # >= を用いた判定
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5}
    >>> set_c = set_a >= set_b
    >>> print(set_a)
    True
    >>>
    >>> # issupersetを用いた判定
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {4, 5}
    >>> set_f = set_d.issuperset(set_e)
    >>> print(set_f)
    True
    >>>
    ```

  - 真部分集合の判定（< 演算子 or > 演算子）<br>
    双方が完全一致でする集合である場合、**部分集合**であり、**上位集合**でもあるが、**真部分集合**ではない。<br>
    真部分集合であるかの判定は <演算子 または、>演算子を使う。<br>
    ```python
    $ python
    >>> # 完全一致する場合、部分集合の判定は真となる
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {1, 2, 3, 4, 5}
    >>> set_c = set_a <= set_b
    >>> print(set_c)
    True
    >>>
    >>> # 完全一致する場合、上位集合の判定は真となる
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {1, 2, 3, 4, 5}
    >>> set_f = set_e >= set_d
    >>> print(set_f)
    True
    >>>
    >>> # 完全一致する場合、真部分集合の判定は偽となる
    >>> set_g = {1, 2, 3, 4, 5}
    >>> set_h = {1, 2, 3, 4, 5}
    >>> set_i = set_h < set_g
    >>> print(set_i)
    False
    >>>
    >>> set_k = {1, 2, 3, 4, 5}
    >>> set_l = {1, 2, 3, 4, 5}
    >>> set_m = set_l > set_k
    >>> print(set_m)
    False
    >>>
    ```

  - 重複要素の有無を判定（isdisjoint）
    ```python
    $ python
    >>> # 重複要素がある場合
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {1, 3, 5}
    >>> set_c = set_a.isdisjoint(set_b)
    >>> print(set_c)
    False
    >>>
    >>> # 重複要素がない場合
    >>> set_d = {1, 2, 3, 4, 5}
    >>> set_e = {6, 7}
    >>> set_f = set_d.isdisjoint(set_e)
    >>> print(set_f)
    True
    >>>
    ```
