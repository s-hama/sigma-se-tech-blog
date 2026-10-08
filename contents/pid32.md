## タイトル
Python - 組込みデータ型：4/4 set・bytes・bytearray・file object

## 概要

set、bytes、bytearray、ファイルオブジェクトの基本操作を整理する。

集合演算では予定者と参加者の差分を調べる。文字列とバイト列では日本語の長さと切り出し結果を比べ、ファイル操作では同じ入力を読み進めたときの位置を確認する。比較例はPython 3.12.2で確認。

## この記事の構成
- [set型 : 集合](#set型--集合)<br>
  予定者と参加者の集合から共通・不足・予定外を取り出す。
- [bytes型 : バイト](#bytes型--バイト)<br>
  文字数とバイト数、文字の途中で切る場合の違いを確認。
- [bytearray型 : バイト配列](#bytearray型--バイト配列)<br>
  バイト列を直接変更する操作と戻り値を確認。
- [file object型 : ファイル操作オブジェクト](#file%20object型--ファイル操作オブジェクト)<br>
  読み書きの基本と読み取り位置・文字コードの扱いを確認。

## 各データ型の操作方法

### set型 : 集合

set型は、**重複した要素**がなく、要素に**順番を**持たない配列のような集合。

記述は、dict型と同じ中カッコ`{}`で囲み、**キーが無い状態**（値のみ）で定義する。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: オブジェクト自体を変更可](<https://sigma-se.com/detail/29/#ミュータブルmutable--オブジェクト自体を変更可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)

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
    >>> # ハッシュ可能なオブジェクトなら異なる型でも要素にできる
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
※ `pop()`は位置を指定できず、任意の要素を一つ削除して返す。無作為抽出を保証する操作ではない。
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
    >>> # 任意の要素を一つ削除
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

  - 対称差集合（^ 演算子 or symmetric_difference）<br>
  二つの集合のどちらか一方だけに含まれる要素を取得する。集合の包含判定をビットで考えると、排他的論理和（XOR）に対応する。
    ```python
    $ python
    >>> # ^ 演算子を用いた対称差集合
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5, 6, 7}
    >>> set_c = set_a ^ set_b
    >>> print(set_c)
    {1, 2, 3, 6, 7}
    >>>
    >>> # symmetric_differenceを用いた対称差集合
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
  ※ 以下、サンプルコードでは、集合`set_a`が集合`set_b`の上位集合であるかを判定している。
    ```python
    $ python
    >>> # >= を用いた判定
    >>> set_a = {1, 2, 3, 4, 5}
    >>> set_b = {4, 5}
    >>> set_c = set_a >= set_b
    >>> print(set_c)
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

- 予定者と参加者を集合で照合する<br>
  次のIDは説明用のデータである。予定者に対して誰が参加し、誰が未参加で、誰が予定外だったかを同じ2集合から取り出す。

  ```python
  planned = {"A", "B", "C"}
  attended = {"B", "C", "D"}
  print("参加済み:", sorted(planned & attended))
  print("未参加:", sorted(planned - attended))
  print("予定外:", sorted(attended - planned))
  print("双方を合わせたID:", sorted(planned | attended))
  ```

  ```text
  参加済み: ['B', 'C']
  未参加: ['A']
  予定外: ['D']
  双方を合わせたID: ['A', 'B', 'C', 'D']
  ```

  差集合は引く向きで意味が変わる。`planned - attended`は予定者から参加済みを除く操作になる。`sorted()`は表示順を固定するために使っており、set自体が順序を保持するわけではない。同じIDの参加回数もsetでは残らないため、回数が必要な処理では元のlistなどを保持する。

  演算と条件の対応は[集合の具体例](https://sigma-se.com/detail/44/#集合)も参照。

### bytes型 : バイト

bytes型は、各要素が \\(0\\) から \\(255\\) の整数となるイミュータブルなバイト列である。

文字列を指定した符号化方式で`str.encode()`するとbytes型になり、bytes型を同じ符号化方式で`bytes.decode()`するとstr型に戻る。bytesリテラルは先頭に**b**を付ける。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)

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
    >>> # bytesオブジェクトを変換元にした場合、encoding引数は指定できない。
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
    abcde
    >>> type(str_b)
    <class 'str'>
    >>>
    ```

- 日本語の文字数とUTF-8のバイト数を区別する<br>
  ASCII文字だけの例では長さが一致するため、文字列`"Aあ"`で確認する。

  ```python
  text = "Aあ"
  encoded = text.encode("utf-8")
  print(len(text), len(encoded))
  print(list(encoded))
  print(text[:2])
  try:
      print(encoded[:2].decode("utf-8"))
  except UnicodeDecodeError as error:
      print(type(error).__name__)
  print(encoded.decode("utf-8") == text)
  ```

  ```text
  2 4
  [65, 227, 129, 130]
  Aあ
  UnicodeDecodeError
  True
  ```

  この例の`A`は1バイト、`あ`は3バイトで表される。`encoded[:2]`は`あ`の途中までしか含まないのでUTF-8として復元できない。文字として切り出したい場合はデコード後のstrを扱い、通信などのバイト数制限とは分けて考える。

  strの`len()`が数えるのはUnicodeの符号位置であり、結合文字や一部の絵文字では画面上の見た目の文字数とも一致しない。エラーを無視してデコードすると失われるデータがあるため、まず文字コードと切り出した境界を確認する。

### bytearray型 : バイト配列

bytearray型は、bytes型に対応するミュータブルなバイト列であり、各要素を同じオブジェクト上で変更できる。文字列から生成する場合は、`bytearray('abc', 'utf-8')`のように符号化方式の指定が必要であり、文字コードのデフォルト値はない。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: オブジェクト自体を変更可](<https://sigma-se.com/detail/29/#ミュータブルmutable--オブジェクト自体を変更可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)

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

### file object型 : ファイル操作オブジェクト

`open()`は、モードに応じて`io.TextIOWrapper`や`io.BufferedReader`などのファイルオブジェクトを返す。単一の「file object型」があるのではなく、共通のファイル操作インターフェースを持つ複数のクラスがある。

- 型の特性
  - テキストファイルは行単位で反復できるイテラブルオブジェクト
    -  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - 使用後はクローズが必要なため、通常は`with open(...) as f:`で扱う

- 定義例<br>
  open()でファイルを開き、処理終了時にclose()で閉じる。<br>
  open()の第\\(1\\)引数にファイルパスを指定して定義。<br>
  第2引数のmodeは、読み書きの指定やテキスト or バイナリの指定に使用。<br>

  - `mode`の種類
    - `r`：読込モード（書込不可）
    - `w`：書込モード（読込不可）
    - `a`：追加・書込モード（読込不可）
    - `r+`：読込・書込モード
    - `w+`：ファイルを空にした状態で、読込・書込モード
    - `a+`：読込・書込モードで開いて、追加モード（ファイルの末尾に追加）
    - `b`：バイナリモードで開いて、上記`mode`と併用する。

  - 下記サンプルでは、カレントディレクトリの`data/sample.txt`を事前に作成している前提
    ```python
    $ python
    >>> # テキストファイルをopen() で開く。
    >>> fPath = 'data/sample.txt'
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
  ※ 下記サンプルでは`data/sample.txt`を事前に作成し、最終行の後にも改行を入れる。`open()`は`~`をホームディレクトリへ自動展開しない。<br>
  ```text
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
      >>> fPath = 'data/sample.txt'
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
      >>> fPath = 'data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLines = tFile.readlines()
      ...     type(fLines)
      ...     print(fLines)
      ...
      <class 'list'>
      ['line1 work file sample\n', 'line2 work file sample\n', 'line3 work file sample\n', 'line4 work file sample\n', 'line5 work file sample\n']
      >>>
      >>> # ※ 改行コードを排除して取得する場合
      >>> fPath = 'data/sample.txt'
      >>> with open(fPath) as tFile:
      ...     fLines = [line.rstrip("\n") for line in tFile]
      ...     print(fLines)
      ...
      ['line1 work file sample', 'line2 work file sample', 'line3 work file sample', 'line4 work file sample', 'line5 work file sample']
      >>>
      ```
  - `readline()`：1行ずつ読込
      ```python
      $ python
      >>> # readline()で1行ずつ読込
      >>> fPath = 'data/sample.txt'
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
      >>> fPath = 'data/sample.txt'
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
  ※ 下記サンプルでは`data`フォルダがあることが前提。<br>

  - `write()`：新規作成
      ```python
      $ python
      >>> # write()でファイルを新規作成
      >>> fPath = 'data/newsample.txt'
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
      >>> fPath = 'data/newsample.txt'
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
      >>> fPath = 'data/newsample.txt'
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
      >>> # ※ 各行の間に改行を入れて書き込む場合
      >>> fPath = 'data/newsample.txt'
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
      >>> fPath = 'data/empty.txt'
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
  ※ 下記サンプルでは`data/sample.txt`を事前に作成し、最終行の後にも改行を入れる。<br>
  ```text
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
      >>> fPath = 'data/sample.txt'
      >>> fAdd = 'line6 work file sample\n'    # 行末に改行を付けて追加
      >>> with open(fPath, mode='a') as tFile:
      ...     tFile.write(fAdd)
      ...
      23
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


- 同じファイルを2回readすると空になる理由<br>
  説明用ファイルを一時ディレクトリに作り、先頭から読み終えた後の位置を確認する。一時ディレクトリはwithブロックを抜けると削除される。

  ```python
  from pathlib import Path
  from tempfile import TemporaryDirectory

  with TemporaryDirectory() as directory:
      path = Path(directory) / "sample.txt"
      path.write_text("Aあ\nBい\n", encoding="utf-8")
      with path.open(encoding="utf-8") as stream:
          print(repr(stream.read()))
          print(repr(stream.read()))
          stream.seek(0)
          print([line.rstrip("\n") for line in stream])
      print(stream.closed)
  ```

  ```text
  'Aあ\nBい\n'
  ''
  ['Aあ', 'Bい']
  True
  ```

  最初の`read()`で位置が末尾へ進むため2回目は空文字列になる。ファイルの内容が消えたわけではなく、`seek(0)`で先頭へ戻すと再び読める。書き込みと読み込みの両方で文字コードを指定し、`with`でクローズする範囲を明確にする。

  行末の改行だけを除く例では`rstrip("\n")`を使う。引数なしの`strip()`は行頭・行末の空白やタブも除くため、空白をデータとして残す必要がある場合は結果が異なる。

## まとめ

- setの差集合は向きによって結果が変わる。予定者と参加者の照合では不足と予定外を別々に取り出せる。
- setは重複回数や順序を保持する用途には向かない。表示順が必要ならsorted()などで明示する。
- strの長さと符号化後のバイト数は異なる。bytesを文字の途中で切るとデコードできない場合がある。
- bytesは変更不可、bytearrayは変更可能なバイト列として使い分ける。
- ファイルは読み進めた位置を持つ。文字コードを明示し、withによるクローズと必要に応じた位置の移動を行う。

### 参考文献
- [Python公式ドキュメント - 集合型：set、frozenset（日本語・集合型の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#set-types-set-frozenset)
- [Python公式ドキュメント - バイナリシーケンス型：bytes、bytearray、memoryview（日本語・バイト列の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#binary-sequence-types-bytes-bytearray-memoryview)
- [Python公式ドキュメント - io：ストリームを扱うコアツール（日本語・ファイル入出力の公式解説）](https://docs.python.org/ja/3/library/io.html)
