## タイトル
Python - 組込みデータ型：2/4 bool・int・float・complex

## 概要

Pythonのbool、int、float、complexの作り方と演算を整理する。

文字列の`"False"`をboolへ変換するとどうなるか、小数の足し算を`==`で比較してよいかを具体例で確かめる。入力の意味を解釈する処理と型変換を区別し、数値の性質に合わせた比較方法を選ぶ。入力変換と誤差の比較例はPython 3.12.2で確認。

## この記事の構成
- [bool型 : 真偽リテラル](#bool型--真偽リテラル)<br>
  真理値判定と文字列で渡された設定値の解釈を区別。
- [int型 : 数値（整数）](#int型--数値整数)<br>
  基数ごとの表記と整数の値域を確認。
- [float型 : 浮動小数点数型](#float型--浮動小数点数型)<br>
  表現範囲に加えて小数の誤差と比較方法を確認。
- [complex型 : 複素数型](#complex型--複素数型)<br>
  複素数リテラルのjと変数名jの違いを確認。

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

- 文字列の設定値をboolへ変換する<br>
  `bool()`は文字列の単語を解釈しない。空でない文字列は`"False"`や`"0"`でも真になる。

  ```python
  for raw in ("False", "0", ""):
      print(repr(raw), bool(raw))
  ```

  ```text
  'False' True
  '0' True
  '' False
  ```

  設定ファイルなどで`true`と`false`だけを受け付けるなら、その入力規則をコードにする。以下では前後の空白と大文字・小文字を吸収し、それ以外の値は入力ミスとして扱う。

  ```python
  def parse_enabled(raw):
      value = raw.strip().lower()
      if value == "true":
          return True
      if value == "false":
          return False
      raise ValueError("true または false を指定してください")


  for raw in (" TRUE ", "False", "flase", ""):
      try:
          print(repr(raw), parse_enabled(raw))
      except ValueError as error:
          print(repr(raw), str(error))
  ```

  ```text
  ' TRUE ' True
  'False' False
  'flase' true または false を指定してください
  '' true または false を指定してください
  ```

  この関数の引数は文字列を前提とする。単に`raw == "true"`と比較すると誤字も`False`になり、明示的な無効指定と区別できない。許可する表記と不正な入力の扱いを決めてから変換する。変換後の値を条件に組み合わせる方法は[論理演算子の記事](https://sigma-se.com/detail/35/)で扱う。

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

- 小数の計算結果は何を基準に比較するか<br>
  `0.1`や`0.2`は2進数では有限桁で正確に表せない。保存時や演算時の丸めによって、次の比較は偽になる。

  ```python
  import math
  from decimal import Decimal

  total = 0.1 + 0.2
  print(total)
  print(total == 0.3)
  print(math.isclose(total, 0.3, rel_tol=1e-9, abs_tol=0.0))
  print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))
  ```

  ```text
  0.30000000000000004
  False
  True
  True
  ```

  `math.isclose()`は指定した許容誤差の範囲で近いかを判定する。`rel_tol`は値の大きさに対する相対的な許容差、`abs_tol`は絶対的な許容差であり、例の値をすべての計算へ流用するものではない。測定精度や必要な桁数に合わせて決める。ゼロ付近を比較する場合は特に`abs_tol`の検討が必要になる。

  `Decimal`は10進小数を扱う型で、この例の足し算を正確に表せる。元の10進表記を保つため文字列から生成する。`Decimal(0.1)`では先にfloatへ丸められた値を受け取るため目的が異なる。Decimalでも除算などの精度や丸め方は設定に依存する。

  2進数で循環する理由は[基数変換の誤差](https://sigma-se.com/detail/44/#基数変換の誤差)を参照。表示だけを丸める処理と、計算結果を比較する処理も区別する。

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

- boolの真理値判定は設定文字列の解釈とは異なる。受け付ける表記を決め、不正な値を明示的なFalseと区別する。
- intは任意精度であり、sys.maxsizeはintの最大値ではない。
- floatの近似値を比較する場合は目的に合う許容誤差を決める。10進表記を保ちたい処理では文字列からのDecimal生成も検討する。
- complexの虚数リテラルは1jのように書く。変数名jとは区別する。

### 参考文献
- [Python公式ドキュメント - 数値型：int、float、complex（日本語・型と数値演算の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#numeric-types-int-float-complex)
- [Python公式ドキュメント - 真理値判定（日本語・真理値判定の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#truth-value-testing)
- [Python公式チュートリアル - 浮動小数点演算、その問題と制限（日本語・浮動小数点誤差の公式解説）](https://docs.python.org/ja/3/tutorial/floatingpoint.html)
