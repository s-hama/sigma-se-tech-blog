## タイトル
Python - 組込みデータ型：1/4 データ型の特性を表す基本用語

## 概要
Pythonの組込みデータ型を理解する前提として、immutable、mutable、iterable、sequence、mappingの意味を整理する。
これらの用語は、list、tuple、dict、setなどの挙動を説明するときに頻繁に登場する。単語だけを暗記するより、値を変更できるか、繰り返し処理できるか、インデックスで参照できるかという観点で分けると理解しやすい。
ここでは、代表的なデータ型を例に、それぞれの特性がコード上でどのように現れるかを確認する。

## この記事の構成
- [イミュータブル（immutable）: オブジェクト自体を変更不可](#イミュータブルimmutable--オブジェクト自体を変更不可)<br>
  オブジェクト自体を変更できない性質と、変数への再代入との違いを整理。
- [ミュータブル（mutable）: オブジェクト自体を変更可](#ミュータブルmutable--オブジェクト自体を変更可)<br>
  オブジェクト自体を変更できる性質を具体例から整理。
- [イテラブル（iterable）: 反復抽出可](#イテラブルiterable--反復抽出可)<br>
  イテラブル（iterable）: 反復抽出可の意味と要点を具体例から整理。
- [シーケンス（sequence）: インデックス指定可](#シーケンスsequence--インデックス指定可)<br>
  シーケンス（sequence）: インデックス指定可の意味と要点を具体例から整理。
- [マッピング（mapping）: 連想配列](#マッピングmapping--連想配列)<br>
  マッピング（mapping）: 連想配列の意味と要点を具体例から整理。

## 各データ型の特性

### イミュータブル（immutable）: オブジェクト自体を変更不可

生成後にオブジェクト自体の状態を変更できない性質を**イミュータブル**という。変数へ別のオブジェクトを再代入することはできるが、元のオブジェクトが書き換わるわけではない。`id()`は実行中のオブジェクトを識別する値であり、必ずしもメモリアドレスそのものを表すとは限らない。

- イミュータブルな型: Python公式ページのドキュメント
  - [bool 型](https://docs.python.org/ja/3/library/functions.html#bool)
  - [int 型](https://docs.python.org/ja/3/library/functions.html#int)
  - [float 型](https://docs.python.org/ja/3/library/functions.html#float)
  - [complex 型](https://docs.python.org/ja/3/library/functions.html#complex)
  - [str 型](https://docs.python.org/ja/3/library/stdtypes.html#str)
  - [tuple 型](https://docs.python.org/ja/3/library/stdtypes.html#tuple)
  - [range 型](https://docs.python.org/ja/3/library/stdtypes.html#range)
  - [bytes 型](https://docs.python.org/ja/3/library/stdtypes.html#bytes)

- int型（イミュータブル）を例に、再代入が元のオブジェクトを変更しないことを確認
    ```python
    $ python
        >>> int_a = 1
        >>> int_b = int_a
        >>> type(int_a)
        <class 'int'>
        >>> int_a += 1
        >>> int_a
        2
        >>> int_b
        1
    ```
    `int_a += 1`では整数オブジェクト1を書き換えず、計算結果の整数オブジェクト2を`int_a`へ再代入する。そのため、元の1を参照している`int_b`は変化しない。

- tuple自体はイミュータブルだが、要素にlistなどのミュータブルなオブジェクトを含めることはできる。その場合、tuple内の参照は置き換えられないが、参照先のlistの内容は変更できる。

### ミュータブル（mutable）: オブジェクト自体を変更可

生成後にオブジェクト自体の状態や内容を変更できる性質を**ミュータブル**という。同じオブジェクトを複数の変数が参照している場合、一方から内容を変更すると、もう一方から見える内容にも反映される。

- ミュータブルな型: Python公式ページのドキュメント
  - [list 型](https://docs.python.org/ja/3/library/stdtypes.html#list)
  - [dict 型](https://docs.python.org/ja/3/library/stdtypes.html#dict)
  - [set 型](https://docs.python.org/ja/3/library/stdtypes.html#set)
  - [bytearray 型](https://docs.python.org/ja/3/library/stdtypes.html#bytearray)

- list型（ミュータブル）を例に、同じオブジェクトを参照する変数への影響を確認
    ```python
    $ python
        >>> list_a = [1, 2, 3]
        >>> list_b = list_a
        >>> type(list_a)
        <class 'list'>
        >>> list_a.append(4)
        >>> list_a
        [1, 2, 3, 4]
        >>> list_b
        [1, 2, 3, 4]
    ```
    `append()`はlistオブジェクト自体を変更するため、同じlistを参照している`list_b`からも変更後の内容が見える。

### イテラブル（iterable）: 反復抽出可

要素を一つずつ抽出し、反復処理ができるオブジェクト。<br>
（特殊な加工なしで for文のループ対象として使用できるオブジェクト）

ミュータブルかどうかと、イテラブルかどうかは別の性質である。例えば、通常のファイルオブジェクトは反復できるが、イミュータブル／ミュータブルという分類だけで反復可能性は決まらない。

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

要素に順序があり、0から始まる整数インデックスで要素へアクセスできるオブジェクト。

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

- 組込みの代表的なマッピング型: Python公式ページのドキュメント
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


## まとめ
- immutableは変数を再代入できないという意味ではなく、オブジェクト自体を変更できない性質を表す。mutableなオブジェクトは内容を変更できる。
- sequenceは順序とインデックスを持ち、iterableはfor文などで要素を順に取り出せる性質を表す。
- mappingはインデックス番号ではなくキーを使って値へアクセス。型の特性を知ると、Pythonの挙動やエラーを追いやすくなる。

### 参考文献
- [Python 3 ドキュメント「データモデル」（日本語・オブジェクトと型の公式仕様）](https://docs.python.org/ja/3/reference/datamodel.html)
- [Python 3 ドキュメント「組み込み型」（日本語・各データ型の公式仕様）](https://docs.python.org/ja/3/library/stdtypes.html)
- [Python 3 ドキュメント「用語集：iterable」（日本語・用語定義）](https://docs.python.org/ja/3/glossary.html#term-iterable)
