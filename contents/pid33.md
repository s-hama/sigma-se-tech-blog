## タイトル
Python - 算術演算子：基本計算と除算・べき乗の使い方

## 概要
Pythonの算術演算子を使い、数値計算の基本を整理する。
加算、減算、乗算だけでなく、通常の除算、切り捨て除算、剰余、べき乗は、用途によって結果が大きく変わる。
ここでは、各演算子の意味と戻り値の違いを、対話モードの実行例で確認する。

## この記事の構成
- [算術演算子の種類](#算術演算子の種類)<br>
  算術演算子の種類と各項目の特徴を整理。
- [単項プラス・マイナス演算子（+／-）](#単項プラスマイナス演算子-)<br>
  単項プラス・マイナス演算子（+／-）をコードや具体例とともに整理。
- [加算（+）・減算（-）](#加算減算-)<br>
  加算（+）・減算（-）の意味と要点を具体例から整理。
- [乗算（*）・除算（/・//）・剰余（%）](#乗算除算剰余)<br>
  乗算（*）・除算（/・//）・剰余（%）の意味と要点を具体例から整理。
- [べき乗（**）](#べき乗)<br>
  べき乗（**）の意味と要点を具体例から整理。

## 各算術演算子の使い方と実装サンプル

### 算術演算子の種類
**算術演算子**は、一般的な**四則演算**とプログラム特有の表現である**単項プラス演算**と**単項マイナス演算**を合わせた演算子を指す。

- 算術演算子一覧
  <table class="table" style="width: 100%;">
    <thead>
      <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>+</td><td>+a</td><td>単項プラス：数値に単項正演算を適用する。</td></tr>
      <tr><td>-</td><td>-a</td><td>符号反転：a の符号を反転する。</td></tr>
      <tr><td>+</td><td>a + b</td><td>加算：a に b を足す。</td></tr>
      <tr><td>-</td><td>a - b</td><td>減算：a から b を引く。</td></tr>
      <tr><td>*</td><td>a * b</td><td>乗算：a に b を掛ける。</td></tr>
      <tr><td>/</td><td>a / b</td><td>除算：a を b で割る。</td></tr>
      <tr><td>//</td><td>a // b</td><td>切り下げ除算：a を b で割った商を負の無限大方向へ丸める。</td></tr>
      <tr><td>%</td><td>a % b</td><td>剰余：a を b で割った余り。</td></tr>
      <tr><td>**</td><td>a ** b</td><td>べき乗：a の b 乗。</td></tr>
    </tbody>
  </table>

以降、実装サンプルを対話モード（インタプリタ）で解説する。

※ int型は任意精度であり、float型とcomplex型の有限値の範囲は実装環境の浮動小数点形式に依存する。詳しくは下記を参考。<br>
- [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#int型--数値整数>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#float型--浮動小数点数型>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#complex型--複素数型>)

### 単項プラス・マイナス演算子（+／-）

- 単項プラス演算子（+）<br>
    単項プラス演算子は、少し特殊で対象値に付加しても符号（もちろん値）の変化はない。
    ```python
    $ python
        >>>
        >>> # 5 に単項プラス演算子を付加して出力
        >>> int_a = 5
        >>> print(+int_a)
        5
        >>>
    ```
    上記の通り、通常のint型に単項プラス演算子を適用しても値は変わらない。bool型はint型のサブクラスであるため、単項プラスの結果はint型の`0`または`1`となるが、型変換を意図する場合は`int(value)`と明示する方が読みやすい。
    ```python
    $ python
        >>>
        >>> # boolean を定義し、単項プラス演算子でintに変換
        >>> bool_a = False
        >>> print(bool_a)
        False
        >>> print(+bool_a)
        0
        >>> bool_b = True
        >>> print(bool_b)
        True
        >>> print(+bool_b)
        1
        >>>
    ```

- 単項マイナス演算子（-）<br>
    単項マイナス演算子は、対象値の符号を反転する。<br>
    ※ **-1** を掛けた結果が欲しいような場合に使用。
    ```python
    $ python
        >>>
        >>> # int型の 5 に単項マイナス演算子を付加して出力
        >>> int_a = 5
        >>> print(-int_a)
        -5
        >>>
        >>> # 単項マイナス演算子を 2 回付加して出力
        >>> print(-(-int_a))
        5
        >>>
        >>> # complex型の 1 - 2j に単項マイナス演算子を付加して出力
        >>> complex_a = - (1 - 2j)
        >>> print(complex_a)
        (-1+2j)
        >>>
    ```

### 加算（+）・減算（-）
- 加算（+）<br>
    ※ 四則演算の**加算**と同じ結果。
    ```python
    $ python
        >>>
        >>> # int型の 1 に 2 を加算
        >>> int_a = 1 + 2
        >>> print(int_a)
        3
        >>>
        >>> # float型の 1.5 に 2.5 を加算
        >>> float_a = 1.5 + 2.5
        >>> print(float_a)
        4.0
        >>>
        >>> # complex型の 5+5j に 5+5j を加算
        >>> complex_a = 5 + 5j + 5 + 5j
        >>> print(complex_a)
        (10+10j)
        >>>
    ```

- 減算（-）<br>
    ※ 四則演算の**減算**と同じ結果。
    ```python
    $ python
        >>>
        >>> # int型の 3 から 2 を減算
        >>> int_a = 3 - 2
        >>> print(int_a)
        1
        >>>
        >>> # float型の 1.5 から 2.5 を減算
        >>> float_a = 1.5 - 2.5
        >>> print(float_a)
        -1.0
        >>>
        >>> # complex型の 5 + 5j から 7 + 3j を減算
        >>> complex_a = 5 + 5j - (7 + 3j)
        >>> print(complex_a)
        (-2+2j)
        >>>
    ```

### 乗算（*）・除算（/・//）・剰余（%）
  - 乗算（*）<br>
    ※ 四則演算の**乗算**と同じ結果。
    ```python
    $ python
        >>>
        >>> # int型の 2に 2 を乗算
        >>> int_a = 2 * 2
        >>> print(int_a)
        4
        >>> # float型の -2.0に 2.5 を乗算
        >>> float_a = -2.0 * 2.5
        >>> print(float_a)
        -5.0
        >>> # complex型の 2 + 2j に -2.0 を乗算
        >>> complex_a = -2.0 * (2 + 2j)
        >>> print(complex_a)
        (-4-4j)
        >>>
    ```

- 除算（/）<br>
    ※ 四則演算の**除算**と同じ結果。
    ```python
    $ python
        >>>
        >>> # int型の 6 を 2 で除算
        >>> int_a = 6 / 2
        >>> print(int_a)
        3.0
        >>> # float型の -6.5 を 0.5 で除算
        >>> float_a = -6.5 / 0.5
        >>> print(float_a)
        -13.0
        >>> # complex型の 2 + 2j を 2 で除算
        >>> complex_a = (2 + 2j) / 2
        >>> print(complex_a)
        (1+1j)
        >>>
    ```

- 切り下げ除算（//）<br>
    `//`は、除算結果を負の無限大方向へ丸めた商を返す。単なる小数部の切捨てではないため、負数では`-5.5 // 0.2`が`-28.0`となる。int同士なら結果はint、少なくとも一方がfloatなら結果はfloatとなる。
    ```python
    $ python
        >>>
        >>> # int型の 6 を 2 で除算 (//)
        >>> int_a = 5 // 2
        >>> print(int_a)
        2
        >>> # float型の -6.5 を 0.5 で除算 (//)
        >>> float_a = -5.5 // 0.2
        >>> print(float_a)
        -28.0
        >>> # complex型の除算 (//)はできない
        >>> complex_a = 3j // 2
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: unsupported operand type(s) for //: 'complex' and 'int'
        >>>
    ```

- 剰余（%）<br>
    除算の演算結果の**余り**を返す。
    ```python
    $ python
        >>>
        >>> # int型の 5 に 2 の剰余
        >>> int_a = 5 % 2
        >>> print(int_a)
        1
        >>>
        >>> # float型の 5.5 に 2.5 の剰余
        >>> float_a = 5.5 % 2.5
        >>> print(float_a)
        0.5
        >>>
        >>> # complex型に剰余はできない
        >>> complex_a = 5j % 2
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: unsupported operand type(s) for %: 'complex' and 'int'
        >>>
    ```
    ※ 例外メッセージの文言はPythonのバージョンで変わる場合があるが、複素数に `//` や `%` を適用すると `TypeError` になる点が重要。
### べき乗（**）
- **底**と**指数**の演算結果（底のべき乗）<br>
    ```python
    $ python
        >>>
        >>> # int型の 2 の 3 乗
        >>> int_a = 2 ** 3
        >>> print(int_a)
        8
        >>> # int型の 10 の -10 乗
        >>> int_b = 10 ** -10
        >>> print(int_b)
        1e-10
        >>>
        >>> # float型の 2.0 の 2.5 乗
        >>> float_a = 2.0 ** 2.5
        >>> print(float_a)
        5.656854249492381
        >>>
        >>> # complex型の 2 + 2j の 3 を乗算
        >>> complex_a = (2 + 2j) ** 3
        >>> print(complex_a)
        (-16+16j)
        >>>
    ```


## まとめ
- 通常の除算には /、負の無限大方向へ丸める切り下げ除算には //、剰余には % を使い、目的に応じて区別。
- 負数を含む剰余は直感と異なる場合があるため、必要に応じて実行結果を確認。
- べき乗演算子 ** は他の算術演算子より優先されるため、複雑な式では括弧を使って計算順序を明確にする。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 二項算術演算（日本語・算術演算子の公式仕様）](https://docs.python.org/ja/3/reference/expressions.html#binary-arithmetic-operations)
