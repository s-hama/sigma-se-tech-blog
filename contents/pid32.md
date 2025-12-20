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

### bytes型 : バイト

bytes型は、**byte**のイミュータブルオブジェクト（同一アドレスで変更不可）。

str型の表記と似ているが先頭に**b**が付き、bytes型をエンコードするとstr型となり、bytes型をデコードするとstr型に戻る。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%B7%E3%83%BC%E3%82%B1%E3%83%B3%E3%82%B9%EF%BC%88sequence%EF%BC%89%3A%20%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E6%8C%87%E5%AE%9A%E5%8F%AF>)

- 定義例
    ```python
    $ python
    >>> # シングルクォーテーションで定義
    >>> byte_a = b'abcde'
    >>> print(byte_a)
    b'abcde'
    >>> type(byte_a)
    <class 'bytes'>
    >>>
    >>> # ダブルクォーテーションで定義
    >>> byte_b = b"abcde"
    >>> print(byte_b)
    b'abcde'
    >>> type(byte_b)
    <class 'bytes'>
    >>>
    >>> # トリプルクォーテーションで定義
    >>> byte_c = b"""abcde
    ... fghij"""
    >>> print(byte_c)
    b'abcde\nfghij'
    >>> type(byte_c)
    <class 'bytes'>
    >>>
    >>> # コンストラクタで定義
    >>> byte_d = bytes(b'abc')
    >>> print(byte_d)
    b'abc'
    >>> type(byte_d)
    <class 'bytes'>
    >>>
    >>> # コンストラクタで文字コードを指定
    >>> byte_f = bytes('abc', 'utf-8')
    >>> print(byte_f)
    b'abc'
    >>> type(byte_f)
    <class 'bytes'>
    >>>
    >>> # ※ 上記でbを付加すると、デフォルトASCIIとなるのでUTF-8でないとエラーが発生する。
    >>> byte_f = bytes(b'abc', 'utf-8')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    TypeError: encoding without a string argument
    >>>
    ```

- bytesとstrの変換<br>
    ※ 文字コードを指定し、**encode**でbytes型に、**decode**でstr型に変換できる。
    ```python
    $ python
    >>> # str型の文字列をUTF-8でエンコード(bytes型に変換)
    >>> str_a = 'abcde'
    >>> byte_a = str_a.encode('utf-8')
    >>> print(byte_a)
    b'abcde'
    >>> type(byte_a)
    <class 'bytes'>
    >>>
    >>> # 上記に続き、bytes型の文字列をUTF-8でデコード(str型に変換)
    >>> str_b = byte_a.decode('utf-8')
    >>> print(str_b)
    'abcde'
    >>> type(str_b)
    <class 'str'>
    >>>
    ```

### bytearray型 : バイト配列

bytearray型は、bytes型の配列版で文字コードを指定しない場合（デフォルト）は、ASCIIでエンコードされる。

各要素の入れ替えを前提としたミュータブルオブジェクト（同一アドレスで変更可）。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: 同一アドレスで変更可](<https://sigma-se.com/detail/29/#:~:text=%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88mutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%B7%E3%83%BC%E3%82%B1%E3%83%B3%E3%82%B9%EF%BC%88sequence%EF%BC%89%3A%20%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E6%8C%87%E5%AE%9A%E5%8F%AF>)

- 定義例
    ```python
    $ python
    >>> # 要素一つで定義
    >>> bytearray_a = bytearray(b'abc')
    >>> print(bytearray_a)
    bytearray(b'abc')
    >>> type(bytearray_a)
    <class 'bytearray'>
    >>> list(bytearray_a)
    [97, 98, 99]
    >>>
    >>> # 要素一つと文字コードを指定して定義
    >>> bytearray_b = bytearray('abc', 'utf-8')
    >>> bytearray_b
    bytearray(b'abc')
    >>> type(bytearray_b)
    <class 'bytearray'>
    >>> list(bytearray_b)
    [97, 98, 99]
    >>>
    >>> # 要素一つと文字コードを指定して定義（ひらがな）
    >>> bytearray_c = bytearray('あいえうお', 'UTF-8')
    >>> list(bytearray_c)
    [227, 129, 130, 227, 129, 132, 227, 129, 136, 227, 129, 134, 227, 129, 138]
    >>>
    ```

- 要素の追加、変更、削除
    ```python
    $ python
    >>> # 要素を一つ追加
    >>> bytearray_a = bytearray(b'abc')
    >>> bytearray_a.append(100)
    >>> print(bytearray_a)
    bytearray(b'abcd')
    >>> list(bytearray_a)
    [97, 98, 99, 100]
    >>>
    >>> # 指定した要素を追加（複数）
    >>> bytearray_b = bytearray(b'abc')
    >>> bytearray_b.extend([100, 101])
    >>> print(bytearray_b)
    bytearray(b'abcde')
    >>> list(bytearray_b)
    [97, 98, 99, 100, 101]
    >>>
    >>> # 変更
    >>> bytearray_c = bytearray(b'abc')
    >>> list(bytearray_c)
    [97, 98, 99]
    >>> bytearray_c[1] = 99    # 99(c)に変更
    >>> print(bytearray_c)
    bytearray(b'acc')
    >>> list(bytearray_c)
    [97, 99, 99]
    >>>
    >>> # 削除
    >>> bytearray_d = bytearray(b'abc')
    >>> list(bytearray_d)
    [97, 98, 99]
    >>> bytearray_d.remove(98)
    >>> print(bytearray_d)
    bytearray(b'ac')
    >>> list(bytearray_d)
    [97, 99]
    >>>
    >>> # 複数存在する場合は、最初の要素を取り除く
    >>> bytearray_e = bytearray(b'abcabc')
    >>> list(bytearray_e)
    [97, 98, 99, 97, 98, 99]
    >>> bytearray_e.remove(98)
    >>> print(bytearray_e)
    bytearray(b'acabc')
    >>> list(bytearray_e)
    [97, 99, 97, 98, 99]
    >>>
    ```

- 要素の並び替え
    ```python
    $ python
    >>> # 逆順に並び替え
    >>> bytearray_a = bytearray(b'abcde')
    >>> bytearray_a.reverse()
    >>> print(bytearray_a)
    bytearray(b'edcba')
    >>> list(bytearray_a)
    [101, 100, 99, 98, 97]
    >>>
    >>> # ※戻り値はNoneなので注意
    >>> bytearray_b = bytearray(b'abcde')
    >>> bytearray_c = bytearray_b.reverse()
    >>> print(bytearray_c)
    None
    >>>
    ```

### fileobject型 : ファイル操作オブジェクト

fileobject型は、ファイル操作（読み書き、入出力）を行う型で、ファイルの内容取得や編集、新規作成などの一連のファイル操作が可能。 

- 型の特性 
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>)
  - イテラブルオブジェクト
    -  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)

- 定義例<br>
  open()でファイルを開き、処理終了時にclose()で閉じる。<br>
  open()の第\\(1\\)引数にファイルパスを指定して定義する。<br>
  第2引数のmodeは、読み書きの指定やテキスト or バイナリの指定に使用する。<br>

  - `mode`の種類
    - `r`：読込モード（書込不可）
    - `w`：書込モード（読込不可）
    - `a`：追加・書込モード（読込不可）
    - `r+`：読込・書込モード
    - `w+`：ファイルを空にした状態で、読込・書込モード
    - `a+`：読込・書込モードで開いて、追加モード（ファイルの末尾に追加）
    - `b`：バイナリモードで開いて、上記`mode`と併用する。

  - 下記サンプルでは`~/data/sample.txt`を事前に作成している前提
    ```python
    $ python
    >>> # テキストファイルをopen() で開く。
    >>> fPath = '~/data/sample.txt'
    >>> tFile = open(fPath)
    >>> # テキストであるため、io.TextIOWrapperとして定義される。
    >>> type(tFile)
    <class '_io.TextIOWrapper'>
    >>> # 開いたら必ず閉じる。
    >>> tFile.close()
    >>>
    >>> # withブロックを使してブロック終了時に自動クローズする。
    >>> with open(fPath) as tFile:
    ...     type(tFile)
    ...
    <class '_io.TextIOWrapper'>
    >>>
    ```
    また、今どこで作業しているかは`getcwd()`で取得できる。
    ```python
    $ python
    >>> # カレント（作業）ディレクトリの取得
    >>> import os
    >>> os.getcwd()
    '/home/hama'
    >>>
    ```

- `mode='r'`：読込モード（書込不可）<br>
  modeの引数なしでデフォルト **'r'** で open() するため、省略する。<br>
  以下、open(mode='r')で開いた後の読込方法。<br>
  ※ 下記サンプルでは`~/data/sample.txt`を事前に作成している前提。<br>
  ```python
  line1 work file sample
  line2 work file sample
  line3 work file sample
  line4 work file sample
  line5 work file sample
  ```

  - `read()`：全行読込
      ```python
      $ python
      >>> # read()で全文読込
      >>> fPath = '~/data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLines = tFile.read()
      ...     type(fLines)
      ...     print(fLines)
      ...
      <class 'str'>
      line1 work file sample
      line2 work file sample
      line3 work file sample
      line4 work file sample
      line5 work file sample
      >>>
      ```
  - `readlines()`：リスト型で全行読込<br>
      ```python
      $ python
      >>> # readlines()で行分割したリスト型で全行読込
      >>> fPath = '~/data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLines = tFile.readlines()
      ...     type(fLines)
      ...     print(fLines)
      ...
      <class 'list'>
      ['line1 work file sample\n', 'line2 work file sample\n', 'line3 work file sample\n', 'line4 work file sample\n', 'line5 work file sample\n']
      >>>
      >>> # ※ 改行コードを排除して取得する場合
      >>> fPath = '/root/data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLines = [line.strip() for line in tFile.readlines()]
      ...     print(fLines)
      ...
      ['line1 work file sample', 'line2 work file sample', 'line3 work file sample', 'line4 work file sample', 'line5 work file sample']
      >>>
      ```
  - `readline()`：1行ずつ読込
      ```python
      $ python
      >>> # readline()で1行ずつ読込
      >>> fPath = '/root/data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLine = tFile.readline()    # 1行目 読込
      ...     print(fLine)
      ...     fLine = tFile.readline()    # 2行目 読込
      ...     print(fLine)
      ...     fLine = tFile.readline()    # 3行目 読込
      ...     print(fLine)
      ...
      line1 work file sample
      
      line2 work file sample
      
      line3 work file sample
      
      >>>
      >>> # readline()で1行ずつ末尾まで読込
      >>> fPath = '/root/data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     while True:
      ...         fLine = tFile.readline()
      ...         print(fLine)
      ...         if not fLine:
      ...             break
      ...
      line1 work file sample
      
      line2 work file sample
      
      line3 work file sample
      
      line4 work file sample
      
      line5 work file sample
      
      >>>
      ```

- `mode='w'`：書込モード（読込不可）<br>
  以下、open(mode='w')で開いた後の書込方法。<br>
  ※ 下記サンプルでは`~/data`フォルダがあることが事前。<br>

  - `write()`：新規作成
      ```python
      $ python
      >>> # write()でファイルを新規作成
      >>> fPath = '~/data/newsample.txt'
      >>> fInput = 'line1 new work file sample'
      >>>
      >>> with open(fPath, mode='w') as tFile:
      ...     tFile.write(fInput)
      ...
      26
      >>> # read()で全行読込
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      line1 new work file sample
      >>>
      ```
  - `write()`：書込（上書き）<br>
    ※ 上記の続き（newsample.txtが作成済）
      ```python
      $ python
      >>> fPath = '~/data/newsample.txt'
      >>> # read()で全行読込
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      line1 new work file sample
      >>>
      >>> # write()で書込（上書き）
      >>> fInput = 'edit new work file sample'
      >>> with open(fPath, mode='w') as tFile:
      ...     tFile.write(fInput)
      ...
      24
      >>> # 'line1 new work file sample' が上書きされている。
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      edit new work file sample
      >>>
      ```

  - `writelines()`：リスト型で全行書込
      ```python
      $ python
      >>> fPath = '~/data/newsample.txt'
      >>> # writelines()でリスト型を全行書込
      >>> fInput = ['line1', 'line2', 'line3', 'line4', 'line5']
      >>> with open(fPath, mode='w') as tFile:
      ...     tFile.writelines(fInput)
      ...
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      line1line2line3line4line5
      >>>
      >>> # ※ 改行コードを排除して書込する場合
      >>> fPath = '~/data/newsample.txt'
      >>> fInput = ['line1', 'line2', 'line3', 'line4', 'line5']
      >>> with open(fPath, mode='w') as tFile:
      ...     tFile.write('\n'.join(fInput))
      ...
      29
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      line1
      line2
      line3
      line4
      line5
      >>>
      ```
  - `pass`で空ファイルを新規作成<br>
      ```python
      $ python
      >>> fPath = '~/data/empty.txt'
      >>> # 空ファイルを新規作成
      >>> with open(fPath, mode='w'):
      ...     pass    # 何もしない
      ...
      >>> # 空ファイルの内容を出力
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      >>>
      ```

- `mode='a'`：追加・書込モード（読込不可）<br>
  以下、open(mode='a') で開いた後の書込方法。<br>
  ※ 下記サンプルでは、`~/data/sample.txt`を事前に作成している前提。<br>
  ```python
  line1 work file sample
  line2 work file sample
  line3 work file sample
  line4 work file sample
  line5 work file sample
  ```

  - `write()`：末尾に追加
      ```python
      $ python
      >>> # write()で末尾に追加
      >>> fPath = '~/data/sample.txt'
      >>> fAdd = '\nline6 work file sample'    # 改行コードも込み
      >>> with open(fPath, mode='a') as tFile:
      ...     tFile.writelines(fAdd)
      ...
      >>> with open(fPath) as tFile:
      ...     print(tFile.read())
      ...
      line1 work file sample
      line2 work file sample
      line3 work file sample
      line4 work file sample
      line5 work file sample
      line6 work file sample
      >>>
      ```
