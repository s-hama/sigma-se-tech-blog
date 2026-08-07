## タイトル
Python - 組込みデータ型：2/4 bool・int・float・complex

## 概要
Pythonの数値系データ型であるbool、int、float、complexの基本操作を整理する。
数値型は計算の基本だが、真偽値が整数として扱えること、floatには丸め誤差があること、complexは実部と虚部を持つことなど、型ごとの性質を理解しておく必要がある。
ここでは、それぞれの型の作り方、確認方法、代表的な演算を対話モードで確認する。

## この記事の構成
- [bool型 : 真偽リテラル](#bool型--真偽リテラル)<br>
  bool型 : 真偽リテラルの意味と要点を具体例から整理。
- [int型 : 数値（整数）](#int型--数値整数)<br>
  int型 : 数値（整数）の意味と要点を具体例から整理。
- [float型 : 浮動小数点数型](#float型--浮動小数点数型)<br>
  float型 : 浮動小数点数型の意味と要点を具体例から整理。
- [complex型 : 複素数型](#complex型--複素数型)<br>
  complex型 : 複素数型の意味と要点を具体例から整理。

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
  - イミュータブルオブジェクト : オブジェクト自体を変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>) を参照

  - bool型はint型のサブクラス
    ```python
    $ python
        >>> issubclass(bool, int)    # 第1引数が第2引数のサブクラスである場合にTrueを返す。
        True
    ```

- int型のサブクラスであることによる振る舞い
  - 数値演算では `True` を \\(1\\)、`False` を \\(0\\) として扱える
    ```python
    $ python
        >>> True == 1    # 数値として比較すると等しい
        True
        >>>
        >>> False == 0    # 数値として比較すると等しい
        True
        >>>
    ```

- int型のサブクラスであるため、数値演算にも利用できる
    ```python
    $ python
        >>> True + True + True   # 加算
        3
        >>> 6 - False   # 減算
        6
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
        >>> bool(False)
        False
        >>>
        >>> # None : 何もないことを示すオブジェクト ( 多言語で良く見かける null は、Pythonでは None と表現する )
        >>> bool(None)
        False
        >>>
        >>> # 0 : int型(整数)のゼロ
        >>> bool(0)
        False
        >>>
        >>> # 0.0 :  float型(浮動小数点数)のゼロ
        >>> bool(0.0)
        False
        >>>
        >>> # 0j :  complex型(複素数)のゼロ
        >>> bool(0j)
        False
        >>>
        >>> # Decimal(0) :  decimal型のゼロ ※ decimal型は組込みデータ型でない
        >>> from decimal import Decimal    # decimal型は組込みデータ型でない
        >>> bool(Decimal(0))
        False
        >>>
        >>> # Fraction(0, 1) :  fraction型(有理数)のゼロ
        >>> from fractions import Fraction    # fraction型は組込みデータ型でない
        >>> bool(Fraction(0, 1))
        False
        >>>
        >>> # '' : str型(文字列)の空文字
        >>> bool('')
        False
        >>>
        >>> # [] : list型(配列)の空配列
        >>> bool([])
        False
        >>>
        >>> # {} : dict型(連想配列)の空配列
        >>> bool({})
        False
        >>>
        >>> # () : tuple型(タプル)の空配列
        >>> bool(())
        False
        >>>
        >>> # set() : set型(集合)の空配列
        >>> bool(set())
        False
        >>>
        >>> # range(0) : range型(数値配列)の空配列
        >>> bool(range(0))
        False
        >>>
        >>>
    ```
- Trueと判定されるオブジェクト<br>
  ここに挙げた代表的な偽と判定される値以外も、各型の `__bool__()` または `__len__()` などの真偽値規則に従って判定される。

### int型 : 数値（整数）

整数型で \\(10\\)進数以外に \\(2\\)進数、\\(8\\)進数、\\(16\\)進数を表現できる。

※ Python\\(2\\) までは、末尾に \\(l\\) や \\(L\\) を付けることでlong型（長整数型）となりint型とlong型は、区別されていたが、Python\\(3\\) から統合され、長整数もint型として扱われるようになった。

- 定義例
    ```python
    $ python
        >>> # 10進数 : そのまま整数を格納
        ... int_a = 12345
        >>> type(int_a)
        <class 'int'>
        >>> print(int_a)    # 値を10進数で出力
        12345
        >>>
        >>> # 2進数 : 頭に「0b」または「0B」を付加して格納
        ... int_a2 = 0b100
        >>> type(int_a2)
        <class 'int'>
        >>> print(int_a2)    # 値を10進数で出力
        4
        >>>
        >>> # 8進数 : 頭に「0o」または「0O」を付加して格納
        ... int_a8 = 0o100
        >>> type(int_a8)
        <class 'int'>
        >>> print(int_a8)    # 値を10進数で出力
        64
        >>>
        >>> # 16進数 : 頭に「0x」または「0X」を付加して格納
        ... int_a16 = 0x100
        >>> type(int_a16)
        <class 'int'>
        >>> print(int_a16)    # 値を10進数で出力
        256
        >>>
    ```

- 型の特性
  - イミュータブルオブジェクト : オブジェクト自体を変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>) を参照

- 値の範囲<br>
Pythonのint型は任意精度であり、固定された最大値・最小値を持たない。扱える大きさは利用可能なメモリなどの実行環境の資源に制約される。<br>
`sys.maxsize`はint型の最大値ではなく、リストや文字列などの要素数・インデックスに使える実装上の上限を示す値である。
    ```python
    $ python
        >>> import sys
        >>>
        >>> print(sys.maxsize)    # int型の最大値ではない
        9223372036854775807
        >>>
    ```

### float型 : 浮動小数点数型

Pythonのfloat型は、通常はC言語の`double`と同じ倍精度浮動小数点数として実装される。CPythonの一般的な環境ではIEEE 754のbinary64に相当するが、正確な精度や範囲は`sys.float_info`で確認する。Pythonの組込み型には、単精度専用のfloat型はない。

- 定義例
    ```python
    $ python
        >>> float_a = 1.0e5    # float型の変数float_aを100000.0で定義
        >>> print(float_a)
        100000.0
        >>> type(float_a)
        <class 'float'>
        >>>
        >>> float_b = 1.2345    # 小数点を含む通常表記でfloat_bを定義
        >>> float_b
        1.2345
        >>> type(float_b)    # 通常の小数表記もfloatとして扱われる
        <class 'float'>
        >>>
    ```

- 型の特性
  - イミュータブルオブジェクト : オブジェクト自体を変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>) を参照

- 値の範囲<br>
一般的なCPython環境では、正の有限最大値は約 \\(1.7976931348623157 \\times 10^{308}\\) となる。`sys.float_info.min`は正の**正規化数**の最小値であり、表現できる正の値全体の最小値ではない。\\(0\\)に最も近い正の非正規化数は`math.ulp(0.0)`で確認できる。

- 実行環境の値を**float_info**で確認
    ```python
    $ python
        >>> import sys
        >>>
        >>> print(sys.float_info.max)    # 最大値
        1.7976931348623157e+308
        >>>
        >>> 1.8e+308    # 最大値を超える数値は「inf」と表現される。
        inf
        >>>
        >>> print(sys.float_info.min)    # 正規化数の正の最小値
        2.2250738585072014e-308
        >>>
        >>> import math
        >>> math.ulp(0.0)    # 0に最も近い正の非正規化数
        5e-324
        >>>
        >>> -sys.float_info.max    # 負の最小値
        -1.7976931348623157e+308
        >>>
        >>> -1.8e+308    # 負の有限値の範囲を下回ると「-inf」と表現される。
        -inf
        >>>
        >>> sys.float_info    # float_infoの情報すべて
        sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)
        >>>
    ```

### complex型 : 複素数型

complex型は、**実部**と**虚部**で構成され、虚数単位（\\(2\\)乗して\\(-1\\)となる）を \\(j\\) で表現する。数学では \\(i\\) が一般的だが、電気工学では \\(i\\) を電流に使うため、虚数単位に \\(j\\) を使う慣習がある。Pythonの複素数リテラルもこの \\(j\\) を採用している。

- 定義例
    ```python
    $ python
        >>> complex_a = 5 + 5j    # complex型の変数 complex_a を5 + 5jで定義
        >>> type(complex_a)
        <class 'complex'>
        >>>
        >>> complex_b = 5 + 5J    # jは大文字でも可
        >>> type(complex_b)
        <class 'complex'>
        >>>
        >>> complex_c = 5j    # 実部は省略可能
        >>> type(complex_c)
        <class 'complex'>
        >>>
        >>> complex_d = 5.5e5+5j    # 実部をfloat型で定義
        >>> type(complex_d)
        <class 'complex'>
        >>>
        >>> print(complex_d)
        (550000+5j)
        >>>
    ```

- 値の範囲<br>
実部と虚部はそれぞれfloat型で保持されるため、有限値の範囲や丸めの性質はfloat型と同様となる。

- 型の特性
  - イミュータブルオブジェクト : オブジェクト自体を変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>) を参照

- 実部、虚部を別々に取得
    ```python
    $ python
        >>> complex_a = 5 + 50j
        >>> print(complex_a.real)    # 実部の値を取得
        5.0
        >>> print(complex_a.imag)    # 虚部の値を取得
        50.0
        >>>
    ```

- 虚数の性質確認
    ```python
    $ python
        >>> complex_a = 123j   # complex型の変数 complex_a を123jで定義
        >>> type(complex_a)
        <class 'complex'>
        >>> complex_b = complex_a * complex_a    # 123jを二乗する
        >>> print(complex_b)    # -15129の実部のみとなる
        (-15129+0j)
        >>> type(complex_b)
        <class 'complex'>
        >>>
    ```

- 使用上の注意
  - 虚数部が \\(1\\) の場合、数学と違い省略できない。
  ```python
  $ python
      >>> complex_a = 5 + j    # 虚数部を数学と同じように省略するとNameErrorとなる。
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      NameError: name 'j' is not defined
      >>>
      >>> complex_b = 5 + 1j    # 虚数部を1jと明示すること。
      >>> type(complex_b)
      <class 'complex'>
      >>>
  ```
- \\(j\\) は、予約語でないため、単独で宣言できてしまうので注意<br>
    complex型に関係なく、全く別の変数として定義できるため、誤用にも注意。
    ```python
    $ python
        >>> j = 12345    # int型で12345を定義
        >>>
        >>> complex_a = 5 + j     # 上記1jと記載しない場合、NameErrorが発生しない。
        >>> print(complex_a)    # 12345 + 5 の演算結果となっている。
        12350
        >>>
        >>> complex_b = 5 + 1j    # 1jと記載した場合、int型 ( j ) と区別される。
        >>> print(complex_b)
        (5+1j)
        >>>
    ```


## まとめ
- bool、int、float、complexはPythonの基本的な数値型で、演算によって結果の型が変わることがある。
- boolはintの派生型なのでTrueを1、Falseを0として扱えるが、意味としては真偽値として読む。
- floatは2進数で正確に表せない値があるため、丸め誤差が発生する場合がある。
- complexでは虚数単位をjで表す。

### 参考文献
- [Python公式ドキュメント - 数値型：int、float、complex（日本語・型と数値演算の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#numeric-types-int-float-complex)
- [Python公式ドキュメント - 真理値判定（日本語・真理値判定の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#truth-value-testing)
- [Python公式チュートリアル - 浮動小数点演算、その問題と制限（日本語・浮動小数点誤差の公式解説）](https://docs.python.org/ja/3/tutorial/floatingpoint.html)
