## タイトル
Python - 組込みデータ型：3/4 str・list・tuple・range・dict

## 概要

str、list、tuple、range、dictの生成・参照・更新を整理する。

listで複数行を初期化したときの共有と、dictをコピーしたときに残る共有を実行例で追う。元データへの影響を確かめながら、要素の置換・オブジェクトの変更・コピーの範囲を区別する。参照共有とコピーの比較例はPython 3.12.2で確認。

## この記事の構成
- [str型 : 文字列型](#str型--文字列型)<br>
  文字列の生成と引用符・エスケープの使い分けを確認。
- [list型 : 配列型](#list型--配列型)<br>
  追加・削除・並べ替えと複数行の初期化で起こる共有を確認。
- [tuple型 : イミュータブルなシーケンス型](#tuple型--イミュータブルなシーケンス型)<br>
  要素の置換と要素が指すlistの変更を区別。
- [range型 : 範囲指定](#range型--範囲指定)<br>
  開始・終了・刻み幅から生成される範囲を確認。
- [dict型 : 連想配列型（辞書型）](#dict型--連想配列型辞書型)<br>
  キーによる操作と浅いコピーが分離する範囲を確認。

## 各データ型の操作方法

### str型 : 文字列型

文字列（Unicode文字）の並びを表す型。

Unicodeは文字に符号位置を割り当てる規格であり、その文字列をバイト列へ変換する符号化方式には**UTF-8**、**UTF-16**、**UTF-32**などがある。同じ文字列でも符号化方式によってバイト列は異なるため、文字とバイト列を区別する。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)

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
    ※ エスケープ（\\）は、特別な意味を持つ文字を無効化。

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

- 文字列にダブルクォーテーションを含める場合、外側をシングルクォーテーションで囲むとエスケープ不要<br>
    `"This is a "string""`のように、外側と内側をどちらもダブルクォーテーションにすると、文字列の終端を判別できず`SyntaxError`となる。
    ```python
    $ python
        >>> str_b = 'This is a "string"'
        >>> print(str_b)
        This is a "string"
        >>>
    ```

- 文字列にシングルクォーテーションを含める場合、外側をダブルクォーテーションで囲むとエスケープ不要<br>
    `'Let's'`のように、外側と内側をどちらもシングルクォーテーションにすると、同様に`SyntaxError`となる。
    ```python
    $ python
        >>> str_a = "Let's"
        >>> print(str_a)
        Let's
        >>>
    ```

### list型 : 配列型

論理型や数値型、文字列型など任意の型を配列として定義する。

- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: オブジェクト自体を変更可](<https://sigma-se.com/detail/29/#ミュータブルmutable--オブジェクト自体を変更可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)

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

- 複数行の初期化で同じlistを共有しないようにする<br>
  `[0] * 3`は数値の初期化に使えるが、`[[0, 0]] * 3`では内側のlistが複製されない。3日分の記録を用意し、1日目の最初の値だけを更新して比べる。

  ```python
  shared_rows = [[0, 0]] * 3
  shared_rows[0][0] = 8
  print(shared_rows)
  print(shared_rows[0] is shared_rows[1])

  separate_rows = [[0, 0] for _ in range(3)]
  separate_rows[0][0] = 8
  print(separate_rows)
  print(separate_rows[0] is separate_rows[1])
  ```

  ```text
  [[8, 0], [8, 0], [8, 0]]
  True
  [[8, 0], [0, 0], [0, 0]]
  False
  ```

  最初の例は一つの内側listへの参照を3回並べている。`is`は同じオブジェクトかを調べる演算子なので、最初の2行の比較が`True`になる。内包表記では繰り返すたびに`[0, 0]`を生成するため各行を独立して更新できる。

  `[0] * 3`の各要素も同じ整数を参照し得るが、整数自体は変更できない。`values[0] = 8`はその位置の参照を置き換える操作なので他の位置には伝わらない。

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
        >>> # インデックス5（現在の末尾の後ろ）に要素を挿入
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
        >>> # 直前に昇順へ並べたlistを反転して降順にする
        >>> list_a.reverse()
        >>>
        >>> print(list_a)
        [50, 40, 30, 20, 10]
        >>>
    ```

### tuple型 : イミュータブルなシーケンス型

tuple型は、要素の並びを保持するイミュータブルなシーケンス型である。生成後に要素の**追加**、**削除**、**置換**はできないが、tupleの要素がlistなどのミュータブルオブジェクトであれば、そのオブジェクトの内容は変更できる。<br>
「定数」と同じ意味ではなく、tupleが保証するのは要素を指す参照の並びを変更できないことである。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)

- 定義例<br>
tupleを作る構文上の要点は小カッコではなくカンマである。小カッコは式を見やすくまとめるために使われ、要素が一つのtupleでは末尾のカンマが必要となる。
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
list型と同じく、インデックスやスライスの指定には大カッコ`[]`を使う。小カッコ`()`は要素取得の記号ではない。
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
        >>> # 内包表記の結果をtupleへ変換
        >>> tuple_b = (1, 2, 3, 4, 5)
        >>> tuple([tuple_b_row for tuple_b_row in tuple_b if tuple_b_row > 2])
        (3, 4, 5)
        >>>
    ```

- tuple型要素の追加、変更、削除<br>
tuple型は、**イミュータブルオブジェクト**であるため要素個別の変更ができない。<br>
  - tupleオブジェクト自体の要素は置換・削除できない
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

  - 変数を別のtupleへ再代入することはできる。`+=` やtuple同士の `+` も元のtupleを変更せず、新しいtupleを作って変数へ代入する
    ```python
    $ python
        >>> tuple_a = (10, 20, 30)
        >>> id(tuple_a)    # idを確認
        139970050305480
        >>>
        >>> tuple_a = (15, 25, 35)    # 新しいtupleを変数tuple_aへ再代入
        >>> print(tuple_a)
        (15, 25, 35)
        >>> id(tuple_a)    # 上記のidと違う
        139970050305840
        >>>
        >>> tuple_a += (45, 55)    # 連結した新しいtupleを変数tuple_aへ再代入
        >>> print(tuple_a)
        (15, 25, 35, 45, 55)
        >>> id(tuple_a)    # 上記のidと違う
        139970050257232
        >>>
        >>> tuple_a = tuple_a + (45, 55, 65)    # 連結した新しいtupleを変数tuple_aへ再代入
        >>> print(tuple_a)
        (15, 25, 35, 45, 55, 45, 55, 65)
        >>> id(tuple_a)    # 上記のidと違う
        139970072464168
        >>>
    ```

- tupleの要素がlistの場合<br>
  tupleが固定するのは要素を指す参照の並びであり、参照先のlistまで変更不可になるわけではない。

  ```python
  record = ("day1", [10, 20])
  record[1].append(30)
  print(record)
  try:
      record[1] = [99]
  except TypeError as error:
      print(type(error).__name__)
  ```

  ```text
  ('day1', [10, 20, 30])
  TypeError
  ```

  `append()`は既存のlistの内容を変更する。後半の代入はtupleの2番目を別のlistへ置き換えようとするため失敗する。変更されない記録が必要なら、内側のデータも含めて型を選ぶ。

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

### range型 : 範囲指定

range型は、for文のループ対象など**範囲指定**を目的としたオブジェクトを作成する。

- 型の特性
  - イミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イミュータブル（immutable）: オブジェクト自体を変更不可](<https://sigma-se.com/detail/29/#イミュータブルimmutable--オブジェクト自体を変更不可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - シーケンスオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > シーケンス（sequence）: インデックス指定可](<https://sigma-se.com/detail/29/#シーケンスsequence--インデックス指定可>)


- 定義例<br>
**開始位置**（デフォルト 0）、**終了位置**、**増加幅**（デフォルト\\(1\\)）を指定し定義。<br>
※ range型のオブジェクト要素を可視化するため、list型に変換した出力をしている。
    ```python
    $ python
        >>> # 開始位置、増加幅を省略（デフォルト適用）し、終了位置のみ指定した定義
        >>> range_a = range(5)
        >>> print(range_a)
        range(0, 5)
        >>> type(range_a)
        <class 'range'>
        >>> list(range_a)
        [0, 1, 2, 3, 4]
        >>>
        >>> # 開始位置、増加幅を省略（デフォルト適用）し、終了位置をマイナスで定義
        >>> range_b = range(-5)
        >>> print(range_b)
        range(0, -5)
        >>> type(range_b)
        <class 'range'>
        >>> list(range_b)    # 開始位置（デフォルト 0）～終了位置 -5 となるため、区間なしと見なされる
        []
        >>>
        >>> # 増加幅を省略（デフォルト適用）し、開始位置 5、終了位置 10 を指定した定義
        >>> range_c = range(5, 10)
        >>> print(range_c)
        range(5, 10)
        >>> type(range_c)
        <class 'range'>
        >>> list(range_c)
        [5, 6, 7, 8, 9]
        >>>
        >>> # 増加幅を省略（デフォルト適用）し、開始位置 -5、終了位置 -10 を指定した定義
        >>> range_d = range(-5, -10)
        >>> print(range_d)
        range(-5, -10)
        >>> list(range_d)    # 開始位置 -5～終了位置 -10 となるため、区間なしと見なされる
        []
        >>>
        >>> # 増加幅を省略（デフォルト適用）し、開始位置 -5、終了位置 0 を指定した定義
        >>> range_e = range(-5, 0)
        >>> print(range_e)
        range(-5, 0)
        >>> list(range_e)
        [-5, -4, -3, -2, -1]
        >>>
        >>> # 開始位置 1、終了位置 10、増加幅 2 を指定した定義
        >>> range_f = range(1, 10, 2)
        >>> print(range_f)
        range(1, 10, 2)
        >>> type(range_f)
        <class 'range'>
        >>> list(range_f)
        [1, 3, 5, 7, 9]
        >>>
        >>> # 開始位置 1、終了位置 10、増加幅 -2 を指定した定義
        >>> range_g = range(1, 10, -2)
        >>> print(range_g)
        range(1, 10, -2)
        >>> type(range_g)
        <class 'range'>
        >>> list(range_g)    # 開始位置 1～終了位置 10 と増加しているが、増加幅 -2 なので区間なしと見なされる
        []
        >>>
        >>> # 開始位置 10、終了位置 1、増加幅 -2 を指定した定義
        >>> range_h = range(10, 1, -2)
        >>> print(range_h)
        range(10, 1, -2)
        >>> type(range_h)
        <class 'range'>
        >>> list(range_h)
        [10, 8, 6, 4, 2]
        >>>
    ```

- float型を指定した定義<br>
range型の生成時、float型は指定できないためリスト内包表記で表現する。
    ```python
    $ python
        >>> # 開始位置 5、終了位置 50、増加幅 5 を指定し、リスト内包表記で10で割る
        >>> [i / 10 for i in range(5, 50, 5)]
        [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 3.5, 4.0, 4.5]
        >>>
    ```

### dict型 : 連想配列型（辞書型）

dict型（辞書型）は、キーと値の対応関係を保持するミュータブルなマッピング型である。他の言語では、同種のデータ構造を**連想配列**や**ハッシュマップ**と呼ぶ場合がある。
- 型の特性
  - ミュータブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > ミュータブル（mutable）: オブジェクト自体を変更可](<https://sigma-se.com/detail/29/#ミュータブルmutable--オブジェクト自体を変更可>)
  - イテラブルオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > イテラブル（iterable）: 反復抽出可](<https://sigma-se.com/detail/29/#イテラブルiterable--反復抽出可>)
  - マッピングオブジェクト
    - [Python - 組込みデータ型の特性 : immutable, mutable, iterable, sequence, mapping > マッピング（mapping）: 連想配列](<https://sigma-se.com/detail/29/#マッピングmapping--連想配列>)

- 定義例
    ```python
    $ python
        >>> # キーと値のセットで定義
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key3': 300}
        >>> type(dict_a)
        <class 'dict'>
        >>>
        >>> # 同じキーを定義した場合、後勝ちで上書かれる
        >>> # ※エラーにならないので注意。
        >>> dict_b = {'key1': 100, 'key2': 200, 'key3': 300, 'key1': 400}
        >>> print(dict_b)
        {'key1': 400, 'key2': 200, 'key3': 300}
        >>> type(dict_b)
        <class 'dict'>
        >>>
        >>> # コンストラクタを使用した定義
        >>> dict_c = dict(key1=100, key2=200, key3=300)
        >>> print(dict_c)
        {'key1': 100, 'key2': 200, 'key3': 300}
        >>> type(dict_c)
        <class 'dict'>
        >>>
        >>> # コンストラクタを使用した変換
        >>> # ※ list型、tuple型が指定できる
        >>> dict_d = dict([('key1', 100), ('key2', 200), ('key3', 300)])
        >>> dict_d
        {'key1': 100, 'key2': 200, 'key3': 300}
        >>> type(dict_d)
        <class 'dict'>
        >>>
    ```

- dict要素の取得
    ```python
    $ python
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>>
        >>> # すべてのキーを取得
        >>> dict_a.keys()
        dict_keys(['key1', 'key2', 'key3'])
        >>>
        >>> # すべての値を取得
        >>> dict_a.values()
        dict_values([100, 200, 300])
        >>>
        >>> # すべてのキーと値を取得
        >>> dict_a.items()
        dict_items([('key1', 100), ('key2', 200), ('key3', 300)])
        >>>
        >>> # キーを指定して値を取得
        >>> print(dict_a['key1'])
        100
        >>>
    ```

- dict要素の追加、変更、削除
    ```python
    $ python
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>>
        >>> # キーを指定して追加
        >>> dict_a['key4'] = 400
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key3': 300, 'key4': 400}
        >>>
        >>> # キーを指定して追加（すでにキーがあれば変更なし）
        >>> dict_a.setdefault('key5', 500)
        500
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key3': 300, 'key4': 400, 'key5': 500}
        >>>
        >>> # キーを指定して変更
        >>> dict_a['key4'] = 444
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key3': 300, 'key4': 444, 'key5': 500}
        >>>
        >>> # キーを指定して削除（pop）
        >>> dict_a.pop('key4')
        444
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key3': 300, 'key5': 500}
        >>>
        >>> # キーを指定して削除（del）
        >>> del dict_a['key3']
        >>> print(dict_a)
        {'key1': 100, 'key2': 200, 'key5': 500}
        >>>
    ```

- 変更時の注意<br>
単純な代入ではdictを複製せず、二つの変数が同じオブジェクトを参照する。外側のdictを別のオブジェクトにしたい場合は`copy()`で浅いコピーを作る。値の中にlistやdictがあり、それらも再帰的に複製したい場合は`copy.deepcopy()`を検討する。
    ```python
    $ python
        >>> # copyを使用しない場合
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>>
        >>> dict_a_temp = dict_a
        >>> dict_a_temp['key2'] = 999    # 代入先のdict型を変更する
        >>>
        >>> print(dict_a_temp)
        {'key1': 100, 'key2': 999, 'key3': 300}
        >>> print(dict_a)
        {'key1': 100, 'key2': 999, 'key3': 300}    # 代入元のdict型も変更されている
        >>>
        >>> # copyを使用した場合
        >>> dict_b = {'key1': 100, 'key2': 200, 'key3': 300}
        >>>
        >>> dict_b_temp = dict_b.copy()
        >>> dict_b_temp['key2'] = 999    # 代入先のdict型を変更する
        >>>
        >>> print(dict_b_temp)
        {'key1': 100, 'key2': 999, 'key3': 300}
        >>> print(dict_b)
        {'key1': 100, 'key2': 200, 'key3': 300}    # 代入元のdict型は変更されていない
        >>>
    ```

- 浅いコピーでは入れ子のlistが共有される<br>
  直前の例はdictの値が整数だったため、コピー先の値を置き換えても元のdictへ影響しなかった。値にlistが入っている場合は外側と内側を分けて確認する。

  ```python
  from copy import deepcopy

  original = {"name": "A", "scores": [70, 80]}
  shallow = original.copy()
  independent = deepcopy(original)

  shallow["name"] = "B"
  shallow["scores"].append(90)
  print(original)
  print(shallow)
  print(independent)
  print(shallow is original)
  print(shallow["scores"] is original["scores"])
  ```

  ```text
  {'name': 'A', 'scores': [70, 80, 90]}
  {'name': 'B', 'scores': [70, 80, 90]}
  {'name': 'A', 'scores': [70, 80]}
  False
  True
  ```

  `copy()`で外側のdictは分かれるので`name`の置換は伝わらない。一方で`scores`に対応するlistは共有され、`append()`による変更が両方から見える。ここでの`deepcopy()`は内側のlistも複製するため元の記録を保てる。

  コピーの方法は「どこを変更するか」で選ぶ。外側のキーと値の対応だけを編集するなら浅いコピーで足りる。入れ子の内容まで独立して編集するなら必要な部分の複製やdeepcopyを検討する。

- dict型の結合<br>
str型、list型、tuple型のように**+演算子**で結合ができない。
    ```python
    $ python
        >>> # updateで dict_a に dict_b を追加する（重複キーは後者で上書き）
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>> dict_b = {'key4': 400, 'key1': 999, 'key2': 999}
        >>> dict_a.update(dict_b)
        >>> print(dict_a)
        {'key1': 999, 'key2': 999, 'key3': 300, 'key4': 400}
        >>>
        >>> # updateを使用しない場合
        >>> dict_a = {'key1': 100, 'key2': 200, 'key3': 300}
        >>> dict_b = {'key4': 400, 'key5': 500, 'key6': 600}
        >>> dict_c = {**dict_a, **dict_b}
        >>> print(dict_c)
        {'key1': 100, 'key2': 200, 'key3': 300, 'key4': 400, 'key5': 500, 'key6': 600}
        >>>
    ```


## まとめ

- listの繰り返しは内側のオブジェクトを複製しない。各行を独立して更新する配列は内包表記などで行ごとに生成する。
- tupleでは要素を置き換えられないが、要素が指すlistの内容は変更できる。
- dict.copy()は外側のdictを複製する。入れ子のlistなども独立して編集する場合はコピーの範囲を確認する。
- str・list・tuple・rangeは位置で、dictはキーで参照する。更新方法は各型の変更可能性に合わせて選ぶ。

### 参考文献
- [Python公式ドキュメント - テキストシーケンス型：str（日本語・文字列型の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#text-sequence-type-str)
- [Python公式ドキュメント - シーケンス型：list、tuple、range（日本語・シーケンス型の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#sequence-types-list-tuple-range)
- [Python公式ドキュメント - マッピング型：dict（日本語・辞書型の公式解説）](https://docs.python.org/ja/3/library/stdtypes.html#mapping-types-dict)
