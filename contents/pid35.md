## タイトル
Python - 論理演算子：or・and・notと真偽値判定

## 概要

Pythonの論理演算子or、and、notを真理値判定と実行順序から整理する。

再試行回数の0を残す初期値設定と、ゼロ除算を避ける条件式を比較する。何が偽になるかに加えて、どの値が返り、どこまで式が実行されるかを確認する。設定値と短絡評価の比較例はPython 3.12.2で確認。

## この記事の構成
- [論理演算子の種類](#論理演算子の種類)<br>
  論理演算子の種類と各項目の特徴を整理。
- [True/Falseの判定基準](#truefalseの判定基準)<br>
  数値の0・空のコンテナ・Noneなどの真理値判定を確認。
- [論理和（or）](#論理和or)<br>
  返される値を確認し、有効な0を残す初期値設定と比較。
- [論理積（and）](#論理積and)<br>
  評価順序を追い、ゼロ除算を防ぐ条件の並べ方を確認。
- [論理否定（not）](#論理否定not)<br>
  真理値を反転し、boolとして返す動作を確認。

## 各論理演算子の使い方と実装サンプル

### 論理演算子の種類

Pythonではbool型以外のオブジェクトも条件式に使える。組込み型では数値のゼロ、空の文字列やコンテナ、`None`などが`False`となり、それ以外は原則として`True`となる。独自クラスでは`__bool__()`または`__len__()`で判定方法を定義できる。

- 各データ型の参考
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > bool型 : 真偽リテラル](<https://sigma-se.com/detail/30/#bool型--真偽リテラル>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#int型--数値整数>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#float型--浮動小数点数型>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#complex型--複素数型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > str型 : 文字列型](<https://sigma-se.com/detail/31/#str型--文字列型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > list型 : 配列型](<https://sigma-se.com/detail/31/#list型--配列型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > tuple型 : イミュータブルなシーケンス型](<https://sigma-se.com/detail/31/#tuple型--イミュータブルなシーケンス型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > range型 : 範囲指定](<https://sigma-se.com/detail/31/#range型--範囲指定>)

- 論理演算子一覧（or, and, not の三つのみ）
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>or</td><td>a or b</td><td>a、b の論理和</td></tr>
        <tr><td>and</td><td>a and b</td><td>a、b の論理積</td></tr>
        <tr><td>not</td><td>not a</td><td>a の否定</td></tr>
    </tbody>
    </table>

### True/Falseの判定基準

論理演算で最も重要となるTrue/Falseの判定基準として、**空文字**や**空リスト**等も`False`と判定される。<br>
下記は偽と判定される代表例である。独自クラスなどでは型が定めた真理値判定に従い、判定自体が例外になる場合もある。

- False判定一覧
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">False判定となる要素</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>False</td><td>bool型のFalse</td></tr>
        <tr><td>None</td><td>何もないことを示すオブジェクト（≒多言語のNull）</td></tr>
        <tr><td>0</td><td>int型（整数）のゼロ</td></tr>
        <tr><td>0.0</td><td>float型（浮動小数点数）のゼロ</td></tr>
        <tr><td>0j</td><td>complex型（複素数）のゼロ</td></tr>
        <tr><td>Decimal(0)</td><td>decimal型のゼロ</td></tr>
        <tr><td>Fraction(0, 1)</td><td>fraction型（有理数）のゼロ</td></tr>
        <tr><td>''</td><td>str型（文字列）の空文字</td></tr>
        <tr><td>[]</td><td>list型（配列）の空配列</td></tr>
        <tr><td>{}</td><td>dict型（連想配列）の空配列</td></tr>
        <tr><td>()</td><td>tuple型（タプル）の空配列</td></tr>
        <tr><td>set()</td><td>set型（集合）の空配列</td></tr>
        <tr><td>range(0)</td><td>range型（数値配列）の空配列</td></tr>
    </tbody>
    </table>
<br>

※ 各実装サンプルは、下記ページを参考。
- [Python - 組込みデータ型まとめ : bool , int, float, complex > bool型 : 真偽リテラル](<https://sigma-se.com/detail/30/#bool型--真偽リテラル>)

以降、論理演算子に関する実装サンプルを対話モード（インタプリタ）で解説する。

### 論理和（or）
`a or b`は、前方から評価して最初に`True`となるオペランドを返す。そこで評価を終える動作を**ショートサーキット**という。<br>
a、b共にFalseである場合は、末尾の要素`b`を返す。

- 論理和パターン
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">a の評価</th>
        <th scope="col">b の評価</th>
        <th scope="col">a or b の戻り値</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>True</td><td>False</td><td>a の値</td></tr>
        <tr><td>False</td><td>True</td><td>b の値</td></tr>
        <tr><td>True</td><td>True</td><td>a の値</td></tr>
        <tr><td>False</td><td>False</td><td>b の値</td></tr>
    </tbody>
    </table>

- 論理和 実装サンプル（論理和パターン）
    ```python
    $ python
        >>> # True or False (int型 or int型)
        >>> bool_a = 1 or 0
        >>> print(bool_a)
        1
        >>> # False or True (float型 or float型)
        >>> bool_b = 0.0 or 1.0
        >>> print(bool_b)
        1.0
        >>> # True or True (complex型 or complex型)
        >>> bool_c = 1j or 2j
        >>> print(bool_c)
        1j
        >>> # False or False (list型 or dict型)
        >>> bool_d = [] or {}
        >>> print(bool_d)
        {}
        >>>
    ```

- ショートサーキットの例<br>
    複数の候補は左から評価され、最初に真となった値が返る。順番を変えると返る値や実行される処理も変わるため、候補の優先順位に合わせて並べる。
    ```python
    $ python
        >>> # 先頭の 2 (True) のみで評価が返される。
        >>> # 以降の 0 (False)、1 (True) は評価しない。
        >>> bool_a = 2 or 0 or 1
        >>> print(bool_a)
        2
        >>> # 2項目の 4 (True) で評価が返される。
        >>> # 以降の 3 (True)、2 (True)、1 (True) は評価しない。
        >>> bool_b = 0 or 4 or 3 or 2 or 1
        >>> print(bool_b)
        4
        >>>
    ```

- 有効な0を初期値で置き換えない<br>
  再試行回数は`0`なら再試行なし、`None`なら未設定として扱う。未設定のときだけ3回へ補うつもりで`or`を使うと、0回の指定も置き換わる。

  ```python
  for retries in (None, 0, 5):
      by_or = retries or 3
      by_none = 3 if retries is None else retries
      print(retries, by_or, by_none)
  ```

  ```text
  None 3 3
  0 3 0
  5 5 5
  ```

  各行は「元の指定・orの結果・Noneだけを補う結果」の順である。`or`は未設定かを調べる演算子ではなく、左辺が偽なら右辺を返す演算子なので0も対象になる。

  空文字列や0をすべて既定値へ置き換えたい仕様なら`or`を使える。値として有効な0を残したい場合は`is None`で未設定を判定する。入力の型や範囲の検査は別途必要であり、この例は非負整数またはNoneを前提とする。

### 論理積（and）
`a and b`は、前方から評価していき`False`となる要素が見つかった時点（ショートサーキット）でその要素を返す。
a、b共にTrueである場合は、末尾の要素`b`を返す。

- 論理積パターン
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">a の評価</th>
        <th scope="col">b の評価</th>
        <th scope="col">a and b の戻り値</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>True</td><td>False</td><td>b の値</td></tr>
        <tr><td>False</td><td>True</td><td>a の値</td></tr>
        <tr><td>True</td><td>True</td><td>b の値</td></tr>
        <tr><td>False</td><td>False</td><td>a の値</td></tr>
    </tbody>
    </table>

- 論理積 実装サンプル（論理積パターン）
    ```python
    $ python
        >>> # True and False (int型 and int型)
        >>> bool_a = 1 and 0
        >>> print(bool_a)
        0
        >>> # False and True (float型 and float型)
        >>> bool_b = 0.0 and 1.0
        >>> print(bool_b)
        0.0
        >>> # True and True (complex型 and complex型)
        >>> bool_c = 1j and 2j
        >>> print(bool_c)
        2j
        >>> # False and False (list型 and dict型)
        >>> bool_d = [] and {}
        >>> print(bool_d)
        []
        >>>
    ```

- ショートサーキットの例
    左から評価して最初に偽となった値を返し、残りの式は実行しない。後ろの式を実行できる条件を先に確認すると、前提を満たさない計算を避けられる。
    ```python
    $ python
        >>> # 先頭の 0 (False) のみで評価が返される。
        >>> # 以降の 1 (True)、2 (True) は評価しない。
        >>> bool_a = 0 and 1 and 2
        >>> print(bool_a)
        0
        >>> # 3項目の 0 (False) で評価が返される。
        >>> # 以降の 4 (True)、5 (True) は評価しない。
        >>> bool_b = 1 and 2 and 0 and 4 and 5
        >>> print(bool_b)
        0
        >>>
    ```

- ゼロ除算を避ける条件は左側で確認する<br>
  「分母が0でなく、割った結果が2を超える」という条件を考える。関数内で表示させ、割り算が実行されたかも確認する。

  ```python
  def exceeds_two(numerator, denominator):
      print("divide", numerator, denominator)
      return numerator / denominator > 2


  for denominator in (0, 2):
      result = denominator != 0 and exceeds_two(6, denominator)
      print("result", denominator, result)
  ```

  ```text
  result 0 False
  divide 6 2
  result 2 True
  ```

  分母が0のときは左辺が偽なので関数自体が呼ばれない。次のように逆順にすると先に割り算が実行され、右側の判定では防げない。

  ```python
  denominator = 0
  try:
      print(6 / denominator > 2 and denominator != 0)
  except ZeroDivisionError as error:
      print(type(error).__name__)
  ```

  ```text
  ZeroDivisionError
  ```

  真になりやすさや偽になりやすさだけで順番を変えず、後続の式が安全に評価できる前提と副作用を確認する。長い条件は名前の付いた変数やif文へ分けると、その依存関係を追いやすい。

### 論理否定（not）
`not x`は、対象`x`を否定した結果をbool型で返す。<br>
`False`なら`True`を返し、`True`なら`False`を返す。

- 論理否定 実装サンプル
    ```python
    $ python
        >>> # int型 0 の否定
        >>> bool_a = not 0
        >>> print(bool_a)
        True
        >>> # int型 1 の否定
        >>> bool_b = not 1
        >>> print(bool_b)
        False
        >>> # float型 0.0 の否定
        >>> bool_c = not 0.0
        >>> print(bool_c)
        True
        >>> # float型 2.5 の否定
        >>> bool_d = not 2.5
        >>> print(bool_d)
        False
        >>> # complex型 0j の否定
        >>> bool_e = not 0j
        >>> print(bool_e)
        True
        >>> # complex型 1j の否定
        >>> bool_f = not 1j
        >>> print(bool_f)
        False
        >>> # int型 1 and int型 2 and int型 0 の否定
        >>> bool_g = not (1 and 2 and 0)
        >>> print(bool_g)
        True
        >>>
    ```


## まとめ

- orとandはTrue/Falseへ変換した値ではなく、選ばれたオペランドの値を返す。notはboolを返す。
- 0もNoneも真理値判定では偽になる。有効な0を残して未設定だけを補う場合はis Noneを使う。
- 短絡評価では後ろの式が実行されないことがある。後続の計算に必要な前提を左側で確認する。
- 条件の並べ替えは返る値や副作用にも影響する。処理の意味を保てるか確認してから変更する。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 真理値判定（日本語・真偽値評価の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#truth-value-testing)
- [Python公式ドキュメント - ブール演算（日本語・論理演算子の公式仕様）](https://docs.python.org/ja/3/reference/expressions.html#boolean-operations)
