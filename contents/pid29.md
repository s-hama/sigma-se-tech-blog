## タイトル
Python - 組込みデータ型まとめ : immutable, mutable, iterable, sequence, mapping

## 目的
この記事では、Pythonを扱う上で頻繁に登場する組込みデータ型の特性を表す用語について記載する。

## 各データ型の特性

### イミュータブル（immutable）: 同一アドレスで変更不可

同一オブジェクト（アドレスが同一）での値の変更ができないオブジェクト。<br>
そのため、値を変更すると別オブジェクト（別のアドレス）として再生成される。

- イミュータブルな型: Python公式ページのドキュメント
  - [bool 型](https://docs.python.org/ja/3/library/functions.html#bool)
  - [int 型](https://docs.python.org/ja/3/library/functions.html#int)
  - [float 型](https://docs.python.org/ja/3/library/functions.html#float)
  - [complex 型](https://docs.python.org/ja/3/library/functions.html#complex)
  - [str 型](https://docs.python.org/ja/3/library/stdtypes.html#str)
  - [tuple 型](https://docs.python.org/ja/3/library/stdtypes.html#tuple)
  - [range 型](https://docs.python.org/ja/3/library/stdtypes.html#range)
  - [bytes 型](https://docs.python.org/ja/3/library/stdtypes.html#bytes)
  - [file object 型](https://docs.python.org/ja/3/glossary.html#term-file-object)

- int型（イミュータブル）を例に変更前の値と変更後の値のアドレスを比較
    ```python
    $ python
        # int_a を int型 の 1で定義
        >>> int_a = 1
        >>> type(int_a)
        <class 'int'>
        # int_a のアドレスを確認
        >>> id(int_a)
        139837241521312
        # int_a を 2 に変更
        >>> int_a = 2
        # int_a のアドレスを確認 ⇒ 変更前と別アドレスとなる。
        >>> id(int_a)
        139837241521344
    ```

- bool型（イミュータブル）を例に変更前の値と変更後の値のアドレスを比較
    ```python
    $ python
        # bool_a を bool型の False で定義
        >>> bool_a = False
        >>> type(bool_a)
        <class 'bool'>
        # bool_a のアドレスを確認
        >>> id(bool_a)
        139837241113440
        # bool_a を True に変更
        >>> bool_a = True
        # bool_a のアドレスを確認 ⇒ 変更前と別アドレスとなる。
        >>> id(bool_a)
        139837241113408
    ```

### ミュータブル（mutable）: 同一アドレスで変更可

同一オブジェクト（アドレスが同一）で値を変更できるオブジェクト。<br>
（値を変更してもアドレスが変わらない。）

また、オブジェクトの一部を変更できるデータ型は、オブジェクトの中身を頻繁に編集することを前提としているため、アドレスが変わらない（わざわざ変える必要がない）ミュータブルとなっている。

- ミュータブルな型: Python公式ページのドキュメント
  - [list 型](https://docs.python.org/ja/3/library/stdtypes.html#list)
  - [dict 型](https://docs.python.org/ja/3/library/stdtypes.html#dict)
  - [set 型](https://docs.python.org/ja/3/library/stdtypes.html#set)
  - [bytearray 型](https://docs.python.org/ja/3/library/stdtypes.html#bytearray)

- list型（ミュータブル）を例に変更前の値と変更後の値のアドレスを比較
    ```python
    $ python
        # list_a を list型で定義
        >>> list_a = [1, 2, 3, 4, 5]
        >>> type(list_a)
        <class 'list'>
        # list_a のアドレスを確認
        >>> id(list_a)
        139837220876360
        # list_a に 7 を追加
        >>> list_a.append(7)
        >>> print(list_a)
        [1, 2, 3, 4, 5, 7]
        # list_a のアドレスを確認 ⇒ 変更前と同一アドレスとなっている。
        >>> id(list_a)
        139837220876360
    ```

### イテラブル（iterable）: 反復抽出可

要素を一つずつ抽出し、反復処理ができるオブジェクト。<br>
（特殊な加工なしで for文のループ対象として使用できるオブジェクト）

また、ミュータブルオブジェクトはすべてイテラブルなオブジェクトとなる。

- イテラブルな型: Python公式ページのドキュメント
  - [str 型](https://docs.python.org/ja/3/library/stdtypes.html#str)
  - [list 型](https://docs.python.org/ja/3/library/stdtypes.html#list)
  - [tuple 型](https://docs.python.org/ja/3/library/stdtypes.html#tuple)
  - [range 型](https://docs.python.org/ja/3/library/stdtypes.html#range)
  - [dict 型](https://docs.python.org/ja/3/library/stdtypes.html#dict)
  - [set 型](https://docs.python.org/ja/3/library/stdtypes.html#set)
  - [bytes 型](https://docs.python.org/ja/3/library/stdtypes.html#bytes)
  - [bytearray 型](https://docs.python.org/ja/3/library/stdtypes.html#bytearray)
  - [file object 型](https://docs.python.org/ja/3/glossary.html#term-file-object)

- イテラブルの反復処理使用例
    ```python
    $ python
        # list_a を list型で定義
        >>> list_a = [1, 2, 3]
        >>> type(list_a)
        <class 'list'>
        # 要素を出力する 反復処理
        >>> for element in list_a:
        ...     print(element)
        ...
        1
        2
        3
        # str_a を str型で定義
        >>> str_a = "abc"
        # 要素を出力する 反復処理
        >>> for element in str_a:
        ...     print(element)
        ...
        a
        b
        c
    ```
