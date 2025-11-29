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
