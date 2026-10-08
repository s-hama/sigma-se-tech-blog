## タイトル
Python - 算術演算子：基本計算と除算・べき乗の使い方

## 概要

Pythonの算術演算子の意味と結果の型を整理する。

秒数を分と残りの秒へ分ける例から`//`と`%`の役割を確認し、負数でも商と余りから元の整数へ戻せることを検算する。べき乗では括弧の位置による結果の違いも扱う。商・余り・優先順位の比較例はPython 3.12.2で確認。

## この記事の構成
- [算術演算子の種類](#算術演算子の種類)<br>
  算術演算子の種類と各項目の特徴を整理。
- [単項プラス・マイナス演算子（+／-）](#単項プラスマイナス演算子-)<br>
  単項プラス・マイナス演算子（+／-）をコードや具体例とともに整理。
- [加算（+）・減算（-）](#加算減算-)<br>
  加算（+）・減算（-）の意味と要点を具体例から整理。
- [乗算（*）・除算（/・//）・剰余（%）](#乗算除算剰余)<br>
  秒数の分解と負数の検算で除算・商・余りを区別。
- [べき乗（**）](#べき乗)<br>
  基本計算と負号・括弧による優先順位の違いを確認。

## 各算術演算子の使い方と実装サンプル

### 算術演算子の種類
**算術演算子**は数値の加減乗除、剰余、べき乗や符号の操作に使う。以下では各演算の結果と型を確認する。

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
        >>> # int型の 5 を 2 で切り下げ除算 (//)
        >>> int_a = 5 // 2
        >>> print(int_a)
        2
        >>> # float型の -5.5 を 0.2 で切り下げ除算 (//)
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
- 商と余りを組み合わせて秒数を分解する<br>
  125秒を分と残りの秒で表すには、60で割った商と余りを使う。`divmod()`なら両方をまとめて得られる。

  ```python
  seconds = 125
  minutes, remainder = divmod(seconds, 60)
  print(minutes, remainder)
  print(minutes * 60 + remainder == seconds)
  ```

  ```text
  2 5
  True
  ```

  `125 // 60`が2分、`125 % 60`が残り5秒に対応する。整数`a`とゼロでない整数`b`では`a == (a // b) * b + a % b`が成り立つので、商と余りを元に戻して確認できる。

- 負数では小数部の切り捨てと商が異なる<br>
  `-5 / 2`は`-2.5`である。`int()`はゼロへ近づく向き、`//`は負の無限大方向へ丸めるため結果が異なる。

  ```python
  print(int(-5 / 2), -5 // 2)
  for a, b in ((5, 2), (-5, 2), (5, -2), (-5, -2)):
      quotient, remainder = divmod(a, b)
      print(a, b, quotient, remainder, quotient * b + remainder)
  ```

  ```text
  -2 -3
  5 2 2 1 5
  -5 2 -3 1 -5
  5 -2 -3 -1 5
  -5 -2 2 -1 -5
  ```

  各行は「割られる数・割る数・商・余り・復元した値」の順である。`-5 = (-3) * 2 + 1`となるように、切り下げた商と余りが組になる。整数の余りはゼロか除数と同じ符号で、絶対値は除数の絶対値より小さい。負数の処理でも商だけで判断せず、この関係を確認する。

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
        >>> # complex型の 2 + 2j を3乗
        >>> complex_a = (2 + 2j) ** 3
        >>> print(complex_a)
        (-16+16j)
        >>>
    ```


- 負号を含めて2乗するには括弧を使う<br>
  ```python
  print(-3 ** 2)
  print((-3) ** 2)
  print(2 ** -3)
  ```

  ```text
  -9
  9
  0.125
  ```

  `-3 ** 2`は`-(3 ** 2)`として評価される。負数全体を底にするなら`(-3) ** 2`と書く。一方で右側の`-3`は負の指数として扱われるため、`2 ** -3`は8分の1になる。

## まとめ

- /は通常の除算、//は商の切り下げ、%は余りを求める。整数の商と余りを同時に使う場合はdivmod()で取り出せる。
- ゼロでない整数bに対してa == (a // b) * b + a % bが成り立つ。負数ではint(a / b)とa // bが異なる場合がある。
- 負数を底としてべき乗する場合は括弧を付ける。-3 ** 2と(-3) ** 2は異なる結果になる。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 二項算術演算（日本語・算術演算子の公式仕様）](https://docs.python.org/ja/3/reference/expressions.html#binary-arithmetic-operations)
