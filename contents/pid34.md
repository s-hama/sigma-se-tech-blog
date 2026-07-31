## タイトル
Python - 複合代入演算子：値の更新を短く書く方法

## 概要
Pythonの複合代入演算子を使い、変数の値を更新する書き方を整理する。
複合代入演算子は、`x = x + 1`のような更新処理を`x += 1`のように短く書くための記法となる。
ここでは、加算、減算、乗算、除算、剰余、べき乗の複合代入を、通常の代入との対応で確認する。

## この記事で扱うこと
- 複合代入演算子の基本形。
- 通常の代入文との対応関係。
- 数値に対する更新処理の書き方。
- mutableなオブジェクトで注意したい挙動。

## 各複合代入演算子の使い方と実装サンプル

### 複合代入演算子の種類

**代入演算子**には、一般的な右辺から左辺へ代入する**代入演算子**（＝）と右辺から左辺へ**算術演算子**を添えて代入する**複合代入演算子**（+=, -=など）がある。

- 複合代入演算子一覧
    <table class="table" style="width: 100%;">
    <thead>
        <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>+=</td><td>a += b</td><td>a = a + b と同義。<br>（ a に b を加算した結果を a に代入 ）</td></tr>
        <tr><td>-=</td><td>a -= b</td><td>a = a - b と同義。<br>（ a から b を減算した結果を a に代入 ）</td></tr>
        <tr><td>*=</td><td>a *= b</td><td>a = a * b と同義。<br>（ a に b を乗算した結果を a に代入 ）</td></tr>
        <tr><td>/=</td><td>a /= b</td><td>a = a / b と同義。<br>（ a を b で除算した結果を a に代入 ）</td></tr>
        <tr><td>//=</td><td>a //= b</td><td>a = a // b と同義。<br>（ a を b で整数除算した結果を a に代入 ）</td></tr>
        <tr><td>%=</td><td>a %= b</td><td>a = a % b と同義。<br>（ a と b で剰余した結果を a に代入 ）</td></tr>
        <tr><td>**=</td><td>a **= b</td><td>a = a ** b と同義。<br>（ a を b でべき乗した結果を a に代入 ）</td></tr>
    </tbody>
    </table>

以降、実装サンプルを対話モード（インタプリタ）で解説する。

※ 演算結果の **最大値**、**最小値** についてはPCのスペックに依存する。詳しくは下記を参考。<br>
- [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#int型--数値整数>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#float型--浮動小数点数型>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#complex型--複素数型>)

### 加算（+=）・減算（-=）
- 加算（+=）<br>
    ※ a = a + b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 2 に 3 を加算複合代入
        >>> int_a = 2
        >>> int_a += 3
        >>> print(int_a)
        5
        >>> # float型の 3.5 に 3.6 を加算複合代入
        >>> float_a = 3.5
        >>> float_a += 3.6
        >>> print(float_a)
        7.1
        >>> # complex型の 4 + 4j に 5 + 5j を加算複合代入
        >>> complex_a = 4 + 4j
        >>> complex_a += 5 + 5j
        >>> print(complex_a)
        (9+9j)
        >>>
    ```

- 減算（-=）<br>
    ※ a = a - b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 5 に 3 を減算複合代入
        >>> int_a = 5
        >>> int_a -= 3
        >>> print(int_a)
        2
        >>> # float型の 5.0 に -5.9 を減算複合代入
        >>> float_a = 5.0
        >>> float_a -= -5.9
        >>> print(float_a)
        10.9
        >>> # complex型の 5 + 5j に 10 + 10j を減算複合代入
        >>> complex_a = 5 + 5j
        >>> complex_a -= 10 - 10j
        >>> print(complex_a)
        (-5+15j)
        >>>
    ```

### 乗算（*=）・除算（/=・//=）・剰余（%=）
- 乗算（*=）<br>
    ※ a = a * b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 2 に 3 を乗算複合代入
        >>> int_a = 2
        >>> int_a *= 3
        >>> print(int_a)
        6
        >>> # float型の 2.5 に -3.0 を乗算複合代入
        >>> float_a = 2.5
        >>> float_a *= -3.0
        >>> print(float_a)
        -7.5
        >>> # complex型の 5 + 2j に 2 - 5j を乗算複合代入
        >>> complex_a = 5 + 2j
        >>> complex_a *= 2 - 5j
        >>> print(complex_a)
        (20-21j)
        >>>
    ```

- 除算（/=）<br>
    ※ a = a / b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 6 に 2 を除算複合代入
        >>> int_a = 6
        >>> int_a /= 2
        >>> print(int_a)
        3.0
        >>> # float型の 5.5 に -0.5 を除算複合代入
        >>> float_a = 5.5
        >>> float_a /= -0.5
        >>> print(float_a)
        -11.0
        >>> # complex型の 2 + 2j に 1 + 1j を除算複合代入
        >>> complex_a = 2 + 2j
        >>> complex_a /= 1 + 1j
        >>> print(complex_a)
        (2+0j)
        >>>
    ```

- 除算（//=） ※商のみ<br>
    ※ a = a // b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 11 に 3 を除算（//）複合代入
        >>> int_a = 11
        >>> int_a //= 3
        >>> print(int_a)
        3
        >>> # float型の 3.3 に 0.2 を除算（//）複合代入
        >>> float_a = 3.3
        >>> float_a //= 0.2
        >>> print(float_a)
        16.0
        >>> # complex型の除算（//）はできない
        >>> complex_a = 3 + 3j
        >>> complex_a //= 2 + 2j
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: can't take floor of complex number.
        >>>
    ```

- 剰余（%=）<br>
    ※ a = a % b と同義（簡略表記したもの）
    ```python
    $ python
        >>> # int型の 9 に 2 を剰余複合代入
        >>> int_a = 9
        >>> int_a %= 2
        >>> print(int_a)
        1
        >>> # float型の 6.5 に 2 を剰余複合代入
        >>> float_a = 6.5
        >>> float_a %= 2
        >>> print(float_a)
        0.5
        >>> # complex型に剰余はできない
        >>> complex_a = 3 + 3j
        >>> complex_a %= 2
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: can't mod complex numbers.
        >>>
    ```

### べき乗（**=）
※ a = a ** b と同義（簡略表記したもの）
```python
$ python
    >>> # int型の 2 に 4 をべき乗複合代入
    >>> int_a = 2
    >>> int_a **= 4
    >>> print(int_a)
    16
    >>> # float型の 2.5 に 2 をべき乗複合代入
    >>> float_a = 2.5
    >>> float_a **= 2
    >>> print(float_a)
    6.25
    >>> # complex型の 2 + 2j に 2 をべき乗複合代入
    >>> complex_a = 2 + 2j
    >>> complex_a **= 2
    >>> print(complex_a)
    8j
    >>>
```


## まとめ
- 複合代入演算子は演算と代入をまとめる記法で、x += 1はx = x + 1に近い意味として読める。
- listなどのmutableな型では、複合代入によって同じオブジェクトの内容が更新される場合がある。
- 短く書けても複雑な式では読みにくくなるため、通常の代入と使い分ける。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 累算代入文（日本語・複合代入の公式仕様）](https://docs.python.org/ja/3/reference/simple_stmts.html#augmented-assignment-statements)
