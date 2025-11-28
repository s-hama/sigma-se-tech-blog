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
  - イミュータブルオブジェクト : 同一アドレスで変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>) を参照

- 最大値と最小値<br>
実質、CPUに依存するので上限、下限はない。

- \\(32\\)ビットマシンの場合<br>
    最大 \\(2,147,483,647\\) :（\\(2^{31} - 1\\) \\(= 2147483647\\)）<br>
    最小 \\(-2,147,483,648\\) :（\\(- 2^{31}\\) \\(= -2147483648\\)）

- \\(62\\)ビットマシンの場合<br>
    最大 \\(9,223,372,036\\)\\(,854,775,807\\) :（\\(2^{63} - 1\\) \\(= 922337203\\)\\(6854775807\\)）<br>
    最小 \\(-9,223,372,036\\)\\(,854,775,808\\) :（\\(- 2^{63}\\) \\(= -922337203\\)\\(6854775808\\)）

- 最大は、**maxsize**で確認できる<br>
    ※ 下記、対話モード実施環境のCPUは、\\(64\\)ビット。
    ```python
    $ python
        >>> import sys
        >>>
        >>> print(sys.maxsize)
        9223372036854775807
        >>>
    ```

### float型 : 浮動小数点数型

float型は、\\(64\\)ビットの浮動小数点数表現（倍精度浮動小数点数）であり、C言語の倍精度浮動小数点数型である`double`を使用して実装されている。

他言語の多くは、\\(32\\)ビットの浮動小数点数表現（単精度浮動小数点数）をfloat\\(64\\)、ビットの浮動小数点数表現（倍精度浮動小数点数）をdoubleとして型が分かれているが、Pythonは倍精度浮動小数点数をfloatとし\\(32\\)ビットの単精度浮動小数点数の型はない。

- 定義例
    ```python
    $ python
        >>> float_a = 1.0e5    # float型の変数float_aを100000.0で定義
        >>> print(float_a)
        100000.0
        >>> type(float_a)
        <class 'float'>
        >>>
        >>> float_b = 1.2345    # 固定小数点数でfloat_bを定義
        >>> float_b
        1.2345
        >>> type(float_b)    # 固定小数点数もfloatとして扱われる
        <class 'float'>
        >>>
    ```

- 型の特性
  - イミュータブルオブジェクト : 同一アドレスで変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>) を参照

- 最大値と最小値
int型と同様にCPUに依存する。

- 64ビットマシンの場合<br>
    正の最大値 \\(1.79769313\\)\\(48623157e+308\\)<br>
    正規化数の正の最小値 \\(2.2250738\\)\\(585072014e-308\\)<br>
    負の最小値 \\(-1.797693\\)\\(1348623157e+308\\)<br>
    ※ 正規化数

- 最大・最小は、**float_info**でも確認できる。
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
        >>> -sys.float_info.max    # 負の最小値
        -1.7976931348623157e+308
        >>>
        >>> -1.8e+308    # 最小値を下回る数値は「inf」と表現される。
        -inf
        >>>
        >>> sys.float_info    # float_infoの情報すべて
        sys.float_info(max=1.7976931348623157e+308, max_exp=1024, max_10_exp=308, min=2.2250738585072014e-308, min_exp=-1021, min_10_exp=-307, dig=15, mant_dig=53, epsilon=2.220446049250313e-16, radix=2, rounds=1)
        >>>
    ```

### complex型 : 複素数型

complex型は、**実部**と**虚部**で構成され、虚部は虚数単位（\\(2\\)乗して\\(-1\\)となる）の \\(j\\) と表現する。<br>
※ 数学の虚数単位は、\\(i\\)（imaginary part）で表現されるが、工学での \\(i\\) は、他の単位で使用されているケースがあり、混乱を招くため \\(j\\) が使われている。

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

- 最大値と最小値
実部と虚部の値はそれぞれ **浮動小数点**でfloat型なのでfloat型と同様にCPUに依存する。

- 型の特性
  - イミュータブルオブジェクト : 同一アドレスで変更不可<br>
  [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>) を参照

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
