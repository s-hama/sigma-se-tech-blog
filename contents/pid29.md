## タイトル
Python - 組込みデータ型：1/4 データ型の特性を表す基本用語

## 概要
Pythonの組込みデータ型を理解する前提として、immutable、mutable、iterable、sequence、mappingの意味を整理する。
これらの用語は、list、tuple、dict、setなどの挙動を説明するときに頻繁に登場する。単語だけを暗記するより、値を変更できるか、繰り返し処理できるか、インデックスで参照できるかという観点で分けると理解しやすい。
ここでは、代表的なデータ型を例に、それぞれの特性がコード上でどのように現れるかを確認する。

## この記事で扱うこと
- immutableとmutableの違い。
- iterable、sequence、mappingの関係。
- データ型の特性がfor文、添字アクセス、代入操作にどう影響するか。
- エラーが出たときに、型の性質から原因を考える方法。

## 作業前に確認すること
| 確認項目 | 内容 |
| --- | --- |
| Python環境 | 対話モードで型やidを確認できる状態にしておく。 |
| 前提知識 | str、list、tuple、dict、setなどの名前を見たことがある状態で読む。 |
| 確認観点 | 値そのものを変更しているのか、新しい値を作っているのかを意識する。 |


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

### シーケンス（sequence）: インデックス指定可

インデックスを指定して直接要素にアクセスできるオブジェクト。

また、ミュータブルと同様にシーケンスオブジェクトはすべてイテラブルなオブジェクトとなる。

- シーケンスな型: Python公式ページのドキュメント
  - [str 型](https://docs.python.org/ja/3/library/stdtypes.html#str)
  - [list 型](https://docs.python.org/ja/3/library/stdtypes.html#list)
  - [tuple 型](https://docs.python.org/ja/3/library/stdtypes.html#tuple)
  - [range 型](https://docs.python.org/ja/3/library/stdtypes.html#range)
  - [bytes 型](https://docs.python.org/ja/3/library/stdtypes.html#bytes)
  - [bytearray 型](https://docs.python.org/ja/3/library/stdtypes.html#bytearray)

- シーケンスオブジェクトからインデックスを指定した抽出例
    ```python
    $ python
        # list_a を list型で定義
        >>> list_a = [1, 2, 3]
        >>> print(list_a[0])    # インデックス 0 を指定
        1
        >>> print(list_a[1])    # インデックス 1 を指定
        2
        >>> print(list_a[2])    # インデックス 2 を指定
        3
        # str_a を str型で定義
        >>> str_a = "abcdefg"
        >>> print(str_a[1])    # インデックス 1 を指定
        'b'
        >>> print(str_a[3])    # インデックス 3 を指定
        'd'
        >>> print(str_a[5])    # インデックス 5 を指定
        'f'
    ```

### マッピング（mapping）: 連想配列

任意に決めたキーで要素を抽出することができるオブジェクト。

シーケンスオブジェクトがインデックスを指定して抽出するのに対し、マッピングオブジェクトは、オブジェクト生成時に自作したキーを指定して抽出する。<br>
※ 一般的に連想配列と言われる配列のこと。

- マッピング型は、dict型のみ: Python公式ページのドキュメント
  - [dict 型](https://docs.python.org/ja/3/library/stdtypes.html#dict)

- dict型（マッピング）からキーを指定した抽出例
    ```python
    $ python
        >>> dict_a = {"s1":123, "s2":456, "s3":789}
        >>> type(dict_a)
        <class 'dict'>
        >>> print(dict_a["s1"])
        123
        >>> print(dict_a["s2"])
        456
        >>> print(dict_a["s3"])
        789
    ```


## 違いを整理する
| 比較する項目 | 整理するポイント |
| --- | --- |
| immutableは変数が変わらないという意味ではない | 変数には別のオブジェクトを再代入できる。変えられないのはオブジェクト自体。 |
| iterableとsequenceの混同 | sequenceは順序とインデックスを持つ。iterableはforで取り出せる性質。 |
| mappingの理解 | インデックス番号ではなく、キーを使って値にアクセスする。 |

## 実務とのつながり
- バグ調査<br>
    listを関数に渡したあと中身が変わる、tupleで代入できない、といった挙動はmutable/immutableの理解で整理できる。
- API設計<br>
    戻り値を変更してよいデータとして渡すか、変更されにくい形で渡すかを判断しやすくなる。

## まとめ
- immutableは変更不可、mutableは変更可能なオブジェクトを指す。
- iterable、sequence、mappingは、値の取り出し方やアクセス方法を表す。
- 型の特性を知ると、Pythonのエラーや挙動を追いやすくなる。
