## タイトル
Python - 論理演算子：or・and・notと真偽値判定

## 概要
Pythonの論理演算子であるor、and、notの基本的な使い方を整理する。
論理演算子は、条件分岐や入力チェックで複数の条件を組み合わせるために使う。PythonではTrue/Falseだけでなく、空文字、空リスト、0なども真偽値として評価される。
ここでは、真偽値判定の基準と、or、and、notの実行結果を対話モードで確認する。

## この記事で扱うこと
- or、and、notの基本動作。
- PythonでFalseとして扱われる値。
- 短絡評価の考え方。
- 条件式を読みやすく書くための注意点。

## 各論理演算子の使い方と実装サンプル

### 論理演算子の種類

**論理演算子**には、bool型に加え、数値型である int型、float型、complex型や文字列である str型、リスト型であるlist型、tuple型、dict型の指定ができる。

- 各データ型の参考
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > bool型 : 真偽リテラル](<https://sigma-se.com/detail/30/#bool型--真偽リテラル>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#int型--数値整数>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#float型--浮動小数点数型>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#complex型--複素数型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > str型 : 文字列型](<https://sigma-se.com/detail/31/#str型--文字列型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > list型 : 配列型](<https://sigma-se.com/detail/31/#list型--配列型>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > tuple型 : 定数の配列型](<https://sigma-se.com/detail/31/#tuple型--定数の配列型>)
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
下記一覧で示す要素以外は、すべて`True`として判定される。

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
`a and b`は、前方から評価していき`True`となる要素が見つかった時点で（**ショートサーキット**と呼ぶ）その要素を返す。<br>
a、b共にFalseである場合は、末尾の要素`b`を返す。

- 論理和パターン
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">a の評価</th>
        <th scope="col">b の評価</th>
        <th scope="col">a or b の評価</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>True</td><td>False</td><td>a の評価</td></tr>
        <tr><td>False</td><td>True</td><td>b の評価</td></tr>
        <tr><td>True</td><td>True</td><td>a の評価</td></tr>
        <tr><td>False</td><td>False</td><td>b の評価</td></tr>
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
    一度に複数の論理和を行う場合、ショートサーキットの性質を利用し、Trueになる可能性が高い評価対象を前方に置くことで、不要な演算を省くことができる。
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

### 論理積（and）
`a and b`は、前方から評価していき`False`となる要素が見つかった時点（ショートサーキット）でその要素を返す。
a、b共にTrueである場合は、末尾の要素`b`を返す。

- 論理積パターン
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">a の評価</th>
        <th scope="col">b の評価</th>
        <th scope="col">a and b の評価</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>True</td><td>False</td><td>b の評価</td></tr>
        <tr><td>False</td><td>True</td><td>a の評価</td></tr>
        <tr><td>True</td><td>True</td><td>b の評価</td></tr>
        <tr><td>False</td><td>False</td><td>a の評価</td></tr>
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
    上記の論理和と同様に、一度に複数の論理積を行う場合、ショートサーキットの性質を利用し、Falseになる可能性が高い評価対象を前方に置くことで、不要な演算を省くことができる。
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
- or、and、notは条件を組み合わせる論理演算子。
- Pythonでは空文字、空リスト、0、NoneなどもFalseとして評価される。
- orやandは短絡評価を行うため、条件によって後ろの式が実行されない場合がある。
- 長い条件式へ処理を詰め込みすぎず、意味のある変数へ分けると読みやすくなる。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 真理値判定（日本語・真偽値評価の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#truth-value-testing)
- [Python公式ドキュメント - ブール演算（日本語・論理演算子の公式仕様）](https://docs.python.org/ja/3/reference/expressions.html#boolean-operations)
