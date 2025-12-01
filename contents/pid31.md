## タイトル
Python - 組込みデータ型まとめ : str, list, tuple, range, dict

## 目的
この記事では、Pythonが扱う組込みデータ型（str、list、tuple、range、dict）の基本的な操作方法について記載する。

## 各データ型の操作方法

### str型 : 文字列型

文字列（Unicode文字）の並びを表す型。

Unicodeは**文字集合**であり、Unicodeの符号化方式（文字コード）である**UTF-8**や**UTF-16**と混同しないように注意。<br>
例えば、別の文字集合である**JISX0208**なら**符号化方式**は、**ISO-2022-JP**（通称JISコード）か**Shift-JIS**となるように、文字集合に対応する符号化方式（文字コード）は決まっている。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%B7%E3%83%BC%E3%82%B1%E3%83%B3%E3%82%B9%EF%BC%88sequence%EF%BC%89%3A%20%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E6%8C%87%E5%AE%9A%E5%8F%AF>)

- 定義例
    ```python
    $ python
        >>> # 変数 str_a をシングルクォーテーションで囲んで定義
        >>> str_a = 'abc'
        >>> type(str_a)
        <class 'str'>
        >>>
        >>> # 変数 str_b をダブルクォーテーションで囲んで定義
        >>> str_b = "abc"
        >>> type(str_b)
        <class 'str'>
        >>>
        >>> # 変数 str_c をトリプルクォート（シングルクォーテーション）で囲んで定義
        >>> str_c = '''hij
        ... klmn'''
        >>> print(str_c)    # 定義文字として改行（\n）を認識する
        hij
        klmn
        >>>
        >>> type(str_c)
        <class 'str'>
        >>>
        >>> # 変数 str_d をトリプルクォート（ダブルクォーテーション）で囲んで定義
        >>> str_d = """abc
        ... defg"""
        >>> print(str_d)    # 定義文字として改行（\n）を認識する
        abc
    defg
        >>>
        >>> type(str_d)
        <class 'str'>
        >>>
    ```

- エスケープの使用例
  - よく使用されるエスケープシーケンス<br>
    <table class="table" style="width: 100%;">
      <thead>
        <tr>
          <th scope="col">エスケープシーケンス</th>
          <th scope="col">説明</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>\\</td><td>バックスラッシュ（\\）</td></tr>
        <tr><td>\\'</td><td>シングルクォーテーション（'）</td></tr>
        <tr><td>\\"</td><td>ダブルクォーテーション（"）</td></tr>
        <tr><td>\n</td><td>ASCII 行送り（LF）</td></tr>
        <tr><td>\r</td><td>ASCII 復帰（CR）</td></tr>
        <tr><td>\t</td><td>ASCII 水平タブ（TAB）</td></tr>
      </tbody>
    </table>
    ※ エスケープ（\\）は、特別な意味を持つ文字を無効化する。

- 主な使用例
    ```python
    $ python
        >>> # 行送りLF（改行）
        >>> str_a = "abcdefg\nhijklmn"
        >>> print(str_a)
        abcdefg
        hijklmn
        >>>
        >>> # 水平タブ（TAB）
        >>> str_b = "abcdefg\thijklmn"
        >>> print(str_b)
        abcdefg	hijklmn
        >>>
        >>> # シングルクォーテーション（'）
        >>> str_c = "abc'def'ghi"
        >>> print(str_c)
        abc'def'ghi
        >>>
        >>> # ダブルクォーテーション（"）
        >>> str_d = 'abc"def"ghi'
        >>> print(str_d)
        abc"def"ghi
        >>>
    ```

- ダブルクォーテーションで囲む場合、シングルクォーテーションのエスケープ（\\）は省略可能
    ```python
    $ python
        >>> str_a = "This is a "string""    # エスケープがないとエラーとなる
        File "<stdin>", line 1
            str_a = "This is a "string""
        SyntaxError: invalid syntax
        >>> str_b = 'This is a "string"'    # シングルクォーテーションで囲った場合はエスケープは不要
        >>> print(str_b)
        This is a "string"
        >>>
    ```

- シングルクォーテーションで囲む場合、ダブルクォーテーションのエスケープ（\\）は省略可能
    ```python
    $ python
        >>> str_a = 'Let\'s'    # エスケープがないとエラーとなる
        File "<stdin>", line 1
            str_a = 'Let's'
                        ^
        SyntaxError: invalid syntax
        >>> str_a = "Let's"    # ダブルクォーテーションで囲った場合はエスケープは不要
        >>> print(str_a)
        Let's
        >>>
    ```

### list型 : 配列型

論理型や数値型、文字列型など任意の型を配列として定義する。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: 同一アドレスで変更可](<https://sigma-se.com/detail/29/#:~:text=%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88mutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%B7%E3%83%BC%E3%82%B1%E3%83%B3%E3%82%B9%EF%BC%88sequence%EF%BC%89%3A%20%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E6%8C%87%E5%AE%9A%E5%8F%AF>)

- 定義例
    ```python
    $ python
        >>> # 変数 list_a を空配列で定義
        >>> list_a = []
        >>> type(list_a)
        <class 'list'>
        >>>
        >>> # 変数 list_b をコンストラクタを用いて空配列で定義
        >>> list_b = list()
        >>> type(list_b)
        <class 'list'>
        >>>
        >>> # 要素数と初期値を指定して定義する
        >>> list_c = [0]*10
        >>> print(list_c)
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        >>>
        >>> # 変数 list_d を int型の1次元配列で定義
        >>> list_d = [1, 2, 3, 4, 5]
        >>> print(list_d)
        [1, 2, 3, 4, 5]
        >>> type(list_d)
        <class 'list'>
        >>>
        >>> # 変数 list_f を string型の1次元配列で定義
        >>> list_f = ['a', 'b', 'c', 'd', 'e']
        >>> type(list_f)
        <class 'list'>
        >>>
        >>> # 変数 list_g を string型とint型の2次元配列で定義
        >>> list_g = [['typeA',1000], ['typeB', 2000], ['typeC', 3000]]
        >>> type(list_g)
        <class 'list'>
        >>>
    ```

- list要素の取得
    ```python
    $ python
        >>> # 変数 list_a を string型の1次元配列で定義
        >>> list_a = ['a', 'b', 'c', 'd', 'e']
        >>>
        >>> # 出現回数の取得
        >>> print(list_a.count('c'))
        1
        >>>
        >>> # 1番目を取得
        >>> print(list_a[0])
        a
        >>>
        >>> # 4番目（末尾が起点）を取得
        >>> print(list_a[-2])
        d
        >>>
        >>> # 1番目から3番目まで取得
        >>> print(list_a[0:3])
        ['a', 'b', 'c']
        >>>
        >>> # 先頭（1番目）から最後（5番目）まで取得
        >>> print(list_a[:])
        ['a', 'b', 'c', 'd', 'e']
        >>>
        >>> # 3番目から最後（5番目）まで取得
        >>> print(list_a[2:])
        ['c', 'd', 'e']
        >>>
        >>> # 4番目（末尾が起点）から最後（5番目）まで取得
        >>> print(list_a[-2:])
        ['d', 'e']
        >>>
        >>> # 先頭（1番目）から最後（5番目）まで一つ飛ばしで取得
        >>> print(list_a[::2])
        ['a', 'c', 'e']
        >>>
        >>> # list内包表記でfor文の結果を取得
        >>> list_b = [1, 2, 3, 4, 5]
        >>> [list_b_row for list_b_row in list_b if list_b_row > 2]
        [3, 4, 5]
        >>>
    ```

- list要素の追加、変更、削除
    ```python
    $ python
        >>> # 末尾に要素を追加
        >>> list_a = [10, 20, 30, 40, 50]
        >>>
        >>> list_a.append(60)
        >>>
        >>> print(list_a)
        [10, 20, 30, 40, 50, 60]
        >>>
        >>> # 5番目と6番目の間に要素を挿入
        >>> list_b = [10, 20, 30, 40, 50]
        >>>
        >>> list_b.insert(5, 55)
        >>>
        >>> print(list_b)
        [10, 20, 30, 40, 50, 55]
        >>>
        >>> # 要素を結合
        >>> list_a = ['a', 'b', 'c', 'd', 'e']
        >>> list_b = [1, 2, 3, 4, 5]
        >>>
        >>> # list_aとlist_b の結合結果を表示（list_a、list_bは書き変わらない）
        >>> print(list_a + list_b)
        ['a', 'b', 'c', 'd', 'e', 1, 2, 3, 4, 5]
        >>>
        >>> # list_a の末尾に list_b を結合
        >>> list_a.extend(list_b)
        >>>
        >>> print(list_a)
        ['a', 'b', 'c', 'd', 'e', 1, 2, 3, 4, 5]
        >>>
        >>> # 5番目の要素を変更
        >>> list_c = [10, 20, 30, 40, 50]
        >>> list_c[4] = 55
        >>> print(list_c)
        [10, 20, 30, 40, 55]
        >>>
        >>> # 3番目の要素を削除
        >>> list_d = [10, 20, 30, 40, 50]
        >>>
        >>> list_d.pop(2)
        30
        >>> print(list_d)
        [10, 20, 40, 50]
        >>>
        >>> # 末尾の要素を削除
        >>> list_e = [10, 20, 30, 40, 50]
        >>>
        >>> list_e.pop()
        50
        >>> print(list_e)
        [10, 20, 30, 40]
        >>>
        >>> # 値 x を持つ最初の要素を削除
        >>> list_f = [10, 20, 30, 40, 50, 60]
        >>>
        >>> list_f.remove(40)
        >>>
        >>> print(list_f)
        [10, 20, 30, 50, 60]
        >>>
    ```

- list要素の並び替え
    ```python
    $ python
        >>> list_a = [10, 40, 30, 20, 50]
        >>>
        >>> # 昇順に並び替え
        >>> list_a.sort()
        >>>
        >>> print(list_a)
        [10, 20, 30, 40, 50]
        >>>
        >>> # 降順に並び替え
        >>> list_a.reverse()
        >>>
        >>> print(list_a)
        [50, 40, 30, 20, 10]
        >>>
    ```

### tuple型 : 定数の配列型

tuple型は、list型と表記が似ているが、処理速度に重点を置いているため、list型に比べ使用メモリが小さくなっている。<br>
その分、同一アドレスでの要素の**追加**、**削除**、**変更**ができないイミュータブルオブジェクトであるため、**定数配列**とも呼ばれる。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: 同一アドレスで変更不可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%9F%E3%83%A5%E3%83%BC%E3%82%BF%E3%83%96%E3%83%AB%EF%BC%88immutable%EF%BC%89%3A%20%E5%90%8C%E4%B8%80%E3%82%A2%E3%83%89%E3%83%AC%E3%82%B9%E3%81%A7%E5%A4%89%E6%9B%B4%E4%B8%8D%E5%8F%AF>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%A4%E3%83%86%E3%83%A9%E3%83%96%E3%83%AB%EF%BC%88iterable%EF%BC%89%3A%20%E5%8F%8D%E5%BE%A9%E6%8A%BD%E5%87%BA%E5%8F%AF>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#:~:text=%E3%82%B7%E3%83%BC%E3%82%B1%E3%83%B3%E3%82%B9%EF%BC%88sequence%EF%BC%89%3A%20%E3%82%A4%E3%83%B3%E3%83%87%E3%83%83%E3%82%AF%E3%82%B9%E6%8C%87%E5%AE%9A%E5%8F%AF>)

- 定義例<br>
要素数が一つの場合を除き、list型とtuple型の定義例の違いは、大カッコ**[]**であるか小カッコ**()**であるかの違いのみ。
    ```python
    $ python
        >>> # 変数 tuple_a を空配列で定義
        >>> tuple_a = ()
        >>> type(tuple_a)
        <class 'tuple'>
        >>>
        >>> # 変数 tuple_b をコンストラクタを用いて空配列で定義
        >>> tuple_b = tuple()
        >>> type(tuple_b)
        <class 'tuple'>
        >>>
        >>> # 変数 tuple_c を int型の1次元配列で定義
        >>> tuple_c = (1, 2, 3, 4, 5)
        >>> print(tuple_c)
        (1, 2, 3, 4, 5)
        >>> type(tuple_c)
        <class 'tuple'>
        >>>
        >>> # 変数 tuple_d を string型の1次元配列で定義
        >>> tuple_d = ('a', 'b', 'c', 'd', 'e')
        >>> type(tuple_d)
        <class 'tuple'>
        >>>
        >>> # 数値と文字列のtuple型 変数 tuple_e を定義
        >>> tuple_e = (1, 2, 3, 4, 'five')
        >>> type(tuple_e)
        <class 'tuple'>
        >>>
        >>> # 変数 tuple_f を string型とint型の2次元配列で定義
        >>> tuple_f = ((1, 'one'), (2, 'two'))
        >>> type(tuple_f)
        <class 'tuple'>
        >>> print(tuple_f)
        ((1, 'one'), (2, 'two'))
        >>>
        >>> # （注意）要素数が一つのtuple型の定義は、カンマが必要
        >>> tuple_g = (0)    # 数値要素が一つでカンマがないとint型の 0として定義される
        >>> type(tuple_g)
        <class 'int'>
        >>>
        >>> tuple_h = (0,)    # 末尾にカンマを付けるとtuple型として定義される
        >>> type(tuple_h)
        <class 'tuple'>
        >>>
        >>> tuple_i = ('zero')    # 文字列要素が一つでカンマがないとstr型の zeroとして定義される
        >>> type(tuple_i)
        <class 'str'>
        >>>
        >>> tuple_j = ('zero',)    # 末尾にカンマを付けるとtuple型として定義される
        >>> type(tuple_j)
        <class 'tuple'>
        >>>
        >>> tuple_k = 0,    # カッコがない状態で末尾にカンマを付けてもtuple型として定義される
        >>> type(tuple_k)
        <class 'tuple'>
        >>>
        >>> tuple_l = 'zero',
        >>> type(tuple_l)
        <class 'tuple'>
        >>>
        >>> # 初期値の5を10回繰り返して定義する
        >>> tuple_m = (5,)*10
        >>> type(tuple_m)
        <class 'tuple'>
        >>> print(tuple_m)
        (5, 5, 5, 5, 5, 5, 5, 5, 5, 5)
        >>>
        >>> tuple_n = (1, 2, 3) * 5    # 要素が2つ以上ある場合も同様の定義となる
        >>> print(tuple_n)
        (1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3, 1, 2, 3)
        >>>
    ```

- tuple要素の取得<br>
要素の取得も、list型とtuple型の違いは、大カッコ**[]**であるか小カッコ**()**であるかの違いのみ。
    ```python
    $ python
        >>> # 変数 tuple_a を string型の1次元配列で定義
        >>> tuple_a = ('a', 'b', 'c', 'd', 'e')
        >>>
        >>> # 出現回数の取得
        >>> tuple_a.count('c')
        1
        >>>
        >>> # 1番目を取得
        >>> print(tuple_a[0])
        a
        >>>
        >>> # 4番目（末尾が起点）を取得
        >>> print(tuple_a[-2])
        d
        >>>
        >>> # 1番目から3番目まで取得
        >>> print(tuple_a[0:3])
        ('a', 'b', 'c')
        >>>
        >>> # 先頭（1番目）から最後（5番目）まで取得
        >>> print(tuple_a[:])
        ('a', 'b', 'c', 'd', 'e')
        >>>
        >>> # 3番目から最後（5番目）まで取得
        >>> print(tuple_a[2:])
        ('c', 'd', 'e')
        >>>
        >>> # 4番目（末尾が起点）から最後（5番目）まで取得
        >>> print(tuple_a[-2:])
        ('d', 'e')
        >>>
        >>> # 先頭（1番目）から最後（5番目）まで一つ飛ばしで取得
        >>> print(tuple_a[::2])
        ('a', 'c', 'e')
        >>>
        >>> # tuple内包表記でfor文の結果を取得
        >>> tuple_b = (1, 2, 3, 4, 5)
        >>> tuple([tuple_b_row for tuple_b_row in tuple_b if tuple_b_row > 2])
        (3, 4, 5)
        >>>
    ```

- tuple型要素の追加、変更、削除<br>
tuple型は、**イミュータブルオブジェクト**であるため要素個別の変更ができない。<br>
  - 同一アドレス（変数の再定義なし）である場合、追加・変更・削除はすべてエラーになる
    ```python
    $ python
        >>> tuple_a = (10, 20, 30)
        >>> id(tuple_a)    # idを確認
        139970050305480
        >>>
        >>> tuple_a[0] = 11    # id=139970050305480のオブジェクトの1番目を変更
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: 'tuple' object does not support item assignment
        >>>
        >>> del tuple_a[2]    # id=139970050305480のオブジェクトの3番目を削除
        Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        TypeError: 'tuple' object doesn't support item deletion
        >>>
    ```

  - 同一アドレスでない場合（変数の再定義する）の追加・変更・削除は、**別アドレスで定義される**ためエラーにならない
    ```python
    $ python
        >>> tuple_a = (10, 20, 30)
        >>> id(tuple_a)    # idを確認
        139970050305480
        >>>
        >>> tuple_a = (15, 25, 35)    # (15, 25, 35)で別アドレスとして再定義（元のオブジェクトは抹消される）
        >>> print(tuple_a)
        (15, 25, 35)
        >>> id(tuple_a)    # 上記のidと違う
        139970050305840
        >>>
        >>> tuple_a += (45, 55)    # (15, 25, 35, 45, 55)で別アドレスとして再定義（元のオブジェクトは抹消される）
        >>> print(tuple_a)
        (15, 25, 35, 45, 55)
        >>> id(tuple_a)    # 上記のidと違う
        139970050257232
        >>>
        >>> tuple_a = tuple_a + (45, 55, 65)    # (15, 25, 35) + (45, 55, 65) で別アドレスとして再定義（元のオブジェクトは抹消される）
        >>> print(tuple_a)
        (15, 25, 35, 45, 55, 65)
        >>> id(tuple_a)    # 上記のidと違う
        139970072464168
        >>>
    ```

- その他補足<br>
list型は**ミュータブルオブジェクト**であるため、appendやinsertやremoveなど、様々なメソッドが準備されているが、tuple型は**イミュータブルオブジェクト**なので、countとindexの\\(2\\)つだけ。
    ```python
    $ python
        >>> list_a = [1, 2]
        >>> type(list_a)
        <class 'list'>
        >>> dir(list_a)
        [..., 'append', ..., 'count', ..., 'index', ..., 'remove', ...]
        >>>
        >>> tuple_a = (1, 2)
        >>> type(tuple_a)
        <class 'tuple'>
        >>> dir(tuple_a)
        [..., 'count', 'index', ...]
        >>>
    ```
