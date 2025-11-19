## タイトル
Python - 組込みデータ型まとめ : bool , int, float, complex

## 目的
この記事では、Pythonが扱う組込みデータ型（bool, int, float, complex）の基本的な操作方法について記載する。

## 各データ型の操作方法

### bool型 : 真偽リテラル

論理型とも呼ばれ、予約語である`True`または、`False`のいずれかの値を取る。

- 定義例
    ```python
    $ python
        >>> bool_a = True    # bool型の変数bool_aをTrueで定義
        >>> type(bool_a)
        <class 'bool'>
        >>>
        >>> bool_a = False    # 変数bool_aをFalseに更新
        >>> type(bool_a)
        <class 'bool'>
        >>>
    ```

- 型の特性
  - イミュータブルオブジェクト : 同一アドレスで変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>) を参照

  - bool型はint型のサブクラス
    ```python
    $ python
        >>> issubclass(bool, int)    # 第1引数が第2引数のサブクラスである場合にTrueを返す。
        True
    ```

- int型のサブクラスであることによる振る舞い
  - 数値型 \\(0\\)、\\(1\\)と同義
    ```python
    $ python
        >>> True == 1    # Trueは、1と同義
        True
        >>>
        >>> False == 0    # Falseは、0と同義
        True
        >>>
    ```

- 数値型と同義であるため、四則演算ができる
    ```python
    $ python
        >>> True + True + True   # 加算
        3
        >>> 6 - False   # 減算
        5
        >>> 100 * False   # 乗算
        0
        >>> 100 / True   # 除算
        100.0
        >>>
        >>> # 総和もとれる (Pythonでは頻繁に登場する)
        >>> bool_list_a = [True, True, False, True, True, True, False]
        >>> sum(bool_list_a)    # 和 : 1 + 1 + 0 + 1 + 1 + 1 + 0
        5
        >>>
    ```

- 判定基準<br>
    Falseと判定されるオブジェクト
    ```python
    $ python
        >>> # False : bool型のFalse
        ... bool(False)
        False
        >>>
        >>> # None : 何もないことを示すオブジェクト ( 多言語で良く見かける null は、Pythonでは None と表現する )
        ... bool(None)
        False
        >>>
        >>> # 0 : int型(整数)のゼロ
        ... bool(0)
        False
        >>>
        >>> # 0.0 :  float型(浮動小数点数)のゼロ
        ... bool(0.0)
        False
        >>>
        >>> # 0j :  complex型(複素数)のゼロ
        ... bool(0j)
        False
        >>>
        >>> # Decimal(0) :  decimal型のゼロ ※ decimal型は組込みデータ型でない
        ... from decimal import Decimal    # decimal型は組込みデータ型でない
        >>> bool(Decimal(0))
        False
        >>>
        >>> # Fraction(0, 1) :  fraction型(有理数)のゼロ
        ... from fractions import Fraction    # fraction型は組込みデータ型でない
        >>> bool(Fraction(0, 1))
        False
        >>>
        >>> # '' : str型(文字列)の空文字
        ... bool('')
        False
        >>>
        >>> # [] : list型(配列)の空配列
        ... bool([])
        False
        >>>
        >>> # {} : dict型(連想配列)の空配列
        ... bool({})
        False
        >>>
        >>> # () : tuple型(タプル)の空配列
        ... bool(())
        False
        >>>
        >>> # set() : set型(集合)の空配列
        ... bool(set())
        False
        >>>
        >>> # range(0) : range型(数値配列)の空配列
        ... bool(range(0))
        False
        >>>
        >>>
    ```
- Trueと判定されるオブジェクト<br>
  上記、Falseと判定されるオブジェクト以外のオブジェクトすべてTrueと判定される。

