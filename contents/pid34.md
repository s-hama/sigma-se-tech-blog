## タイトル
Python - 複合代入演算子：値の更新を短く書く方法

## 概要

Pythonの複合代入演算子を使った値の更新を整理する。

数値の加算・減算などを通常の代入と対応させた後、listの`+=`と`+`を比較する。更新後の値が同じでも別の変数への影響が異なる理由を追い、共有しているデータを変更するかどうかで書き方を選ぶ。listの比較例はPython 3.12.2で確認。

## この記事の構成
- [複合代入演算子の種類](#複合代入演算子の種類)<br>
  複合代入演算子の種類と各項目の特徴を整理。
- [加算（+=）・減算（-=）](#加算減算-)<br>
  数値の更新とlistの参照共有への影響を比較。
- [乗算（*=）・除算（/=・//=）・剰余（%=）](#乗算除算剰余)<br>
  乗算（*=）・除算（/=・//=）・剰余（%=）の意味と要点を具体例から整理。
- [べき乗（**=）](#べき乗)<br>
  べき乗（**=）の意味と要点を具体例から整理。

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
        <tr><td>+=</td><td>a += b</td><td>a に b を加算し、結果を a に代入。</td></tr>
        <tr><td>-=</td><td>a -= b</td><td>a から b を減算し、結果を a に代入。</td></tr>
        <tr><td>*=</td><td>a *= b</td><td>a に b を乗算し、結果を a に代入。</td></tr>
        <tr><td>/=</td><td>a /= b</td><td>a を b で除算し、結果を a に代入。</td></tr>
        <tr><td>//=</td><td>a //= b</td><td>a を b で切り下げ除算し、結果を a に代入。</td></tr>
        <tr><td>%=</td><td>a %= b</td><td>a を b で割った剰余を a に代入。</td></tr>
        <tr><td>**=</td><td>a **= b</td><td>a の b 乗を a に代入。</td></tr>
    </tbody>
    </table>

`a += b`は`a = a + b`に近い計算だが、完全に同一ではない。複合代入は左辺を一度だけ評価し、型が対応していれば同じオブジェクトをその場で変更する。この違いはlistなどのミュータブルな型や、添字・属性を左辺にした場合に現れる。

以降、実装サンプルを対話モード（インタプリタ）で解説する。

※ int型は任意精度であり、float型とcomplex型の有限値の範囲は実装環境の浮動小数点形式に依存する。詳しくは下記を参考。<br>
- [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#int型--数値整数>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#float型--浮動小数点数型>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#complex型--複素数型>)

### 加算（+=）・減算（-=）
- 加算（+=）<br>
    ※ 数値型では`a = a + b`に近い結果となるが、複合代入は左辺を一度だけ評価する。
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

- listの`+=`と`+`を別の変数から比べる<br>
  どちらも`items`へ30を追加するが、同じlistを参照している`observed`から見た結果は異なる。

  ```python
  items = [10, 20]
  observed = items
  items += [30]
  print(items, observed, items is observed)

  items = [10, 20]
  observed = items
  items = items + [30]
  print(items, observed, items is observed)
  ```

  ```text
  [10, 20, 30] [10, 20, 30] True
  [10, 20, 30] [10, 20] False
  ```

  listの`+=`は元のlistを変更するため、同じオブジェクトを参照する`observed`にも追加後の内容が見える。`+`は連結した新しいlistを作り、その参照を`items`へ代入する。`observed`は元のlistを参照し続ける。

  共有中のlistを更新したい場合は`+=`や`extend()`を使える。連結前のlistを残したい場合は`+`で新しいlistを作る。ただし新しい外側のlistを作っても入れ子の要素までは複製されない。コピーの範囲は[list・dictの記事](https://sigma-se.com/detail/31/)を参照。

  整数の`+=`は元の整数オブジェクトを書き換えない。複合代入がその場で変更するかどうかは型に依存するため、短く書き換える際も対象の型と共有の有無を確かめる。

- 減算（-=）<br>
    以下の組込み数値型と単純な変数の例では、`a = a - b`と同じ計算結果になる。
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
        >>> # complex型の 5 + 5j に 10 - 10j を減算複合代入
        >>> complex_a = 5 + 5j
        >>> complex_a -= 10 - 10j
        >>> print(complex_a)
        (-5+15j)
        >>>
    ```

### 乗算（*=）・除算（/=・//=）・剰余（%=）
- 乗算（*=）<br>
    以下の組込み数値型と単純な変数の例では、`a = a * b`と同じ計算結果になる。
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
    以下の組込み数値型と単純な変数の例では、`a = a / b`と同じ計算結果になる。
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

- 切り下げ除算（//=）<br>
    以下の組込み数値型と単純な変数の例では、`a = a // b`と同じ計算結果になる。
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
        TypeError: unsupported operand type(s) for //: 'complex' and 'complex'
        >>>
    ```

- 剰余（%=）<br>
    以下の組込み数値型と単純な変数の例では、`a = a % b`と同じ計算結果になる。
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
        TypeError: unsupported operand type(s) for %: 'complex' and 'int'
        >>>
    ```
    ※ 例外メッセージの文言はPythonのバージョンで変わる場合があるが、複素数に `//` や `%` を適用すると `TypeError` になる点が重要。

### べき乗（**=）
以下の組込み数値型と単純な変数の例では、`a = a ** b`と同じ計算結果になる。
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

- 複合代入は演算と代入をまとめ、左辺を一度だけ評価する。
- listの+=は元のlistを変更する。+で連結して再代入すると外側のlistは別オブジェクトになり、元のlistを参照する変数へ連結結果は伝わらない。
- その場で変更するかどうかは型に依存する。通常の代入を短く書き換える前に型と参照共有を確認する。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 累算代入文（日本語・複合代入の公式仕様）](https://docs.python.org/ja/3/reference/simple_stmts.html#augmented-assignment-statements)
