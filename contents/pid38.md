## タイトル
Python - 例外処理：try・exceptと組込み例外クラス

## 概要
Pythonの例外処理と組込み例外クラスの基本を整理する。
例外処理は、想定外の入力、ファイル操作の失敗、型の不一致などが起きたときに、プログラムを安全に制御するための仕組みとなる。
ここでは、try、except、else、finallyの役割と、代表的な組込み例外クラスの位置づけを確認する。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [例外処理と例外クラス](#例外処理と例外クラス)<br>
  例外処理と例外クラスの意味と要点を具体例から整理。
- [組込み例外クラス一覧](#組込み例外クラス一覧)<br>
  組込み例外クラス一覧の意味と要点を具体例から整理。
- [組込み例外クラスのツリー表示サンプル](#組込み例外クラスのツリー表示サンプル)<br>
  組込み例外クラスのツリー表示サンプルをコードや具体例で確認。

## 対象環境と利用上の注意
- 本文記載時の環境<br>
Python \\(3.6.4\\)。掲載した例外クラスのツリー出力は、この環境で取得したもの。
- 確認時期<br>
2026年8月にPython公式ドキュメントと照合し、例外処理の基本仕様と記載内容を見直した。
- 現在そのまま利用できない箇所<br>
掲載コード全体を現行Pythonでは再実行していない。<br>
Pythonの更新で例外階層は追加・変更されるため、掲載ツリーを現行版の完全な一覧として利用せず、利用中のバージョンの公式ドキュメントを確認する。

## 解説と実装サンプル

### 例外処理と例外クラス

文字通り、**例外**（正常系でない想定外のエラー）が発生した場合に対処する処理を**例外処理**と呼び、Pythonでは、メイン処理を**try句**に、例外処理を**except句**に書く。

また、**except句**に指定する**例外クラス**によって、どの例外をキャッチするか指定することができる。

- `ValueError`を捕捉し、`else`と`finally`を使う構文例
    ```python
    $ python
    >>> try:
    ...     value = int('123')
    ... except ValueError:
    ...     print('整数へ変換できません')
    ... else:
    ...     print(value)    # 例外が発生しなかった場合だけ実行
    ... finally:
    ...     print('処理終了')    # 例外の有無にかかわらず実行
    123
    処理終了
    ```

`BaseException`は`SystemExit`や`KeyboardInterrupt`も含む最上位の基底クラスであり、通常のアプリケーション処理で直接捕捉しない。可能な限り`ValueError`など原因に対応する具体的な例外クラスを指定する。

### 組込み例外クラス一覧

以下は、本文記載時の環境を基準にした代表的な組込み **例外クラス**とそれぞれの概要。すべて`BaseException`から派生するが、一覧は現行版の全クラスを網羅しない。<br>

<table class="table" style="width: 100%; table-layout: fixed;">
  <thead>
    <tr>
      <th scope="col">例外クラス名</th>
      <th scope="col">例外キャッチ(except)タイミング</th>
    </tr>
  </thead>
  <tbody>
    <tr><td>BaseException</td><td>任意の組込み例外が発生した場合。（全組込み例外の基底クラス）</td></tr>
    <tr><td>┣ SystemExit</td><td>システム終了した場合。（sys.exit()、exit等）</td></tr>
    <tr><td>┣ KeyboardInterrupt</td><td>ユーザーのキー割込み（Ctrl+C等）が発生した場合。</td></tr>
    <tr><td>┣ GeneratorExit</td><td>ジェネレータ 、コルーチンを閉じた場合。（generator.close() 、coroutine.close()）</td></tr>
    <tr><td>┗ Exception</td><td>システム終了以外の例外が発生した場合。（ユーザー定義の例外はここから派生させる。）</td></tr>
    <tr><td>&nbsp;┣ StopIteration</td><td>イテレータによる次の領域参照時（next()、イテレータの__next__()）、対象が存在しない場合。</td></tr>
    <tr><td>&nbsp;┣ StopAsyncIteration</td><td>非同期イテレータによる次の領域参照時（非同期イテレータの__anext__()）、対象が存在しない場合。</td></tr>
    <tr><td>&nbsp;┣ ArithmeticError</td><td>算術演算で例外が発生した場合。（OverflowError, ZeroDivisionError, FloatingPointError の基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┣ FloatingPointError</td><td>浮動小数点演算に関する例外クラス。Python公式ドキュメントでは「現在は使われていない」とされている。</td></tr>
    <tr><td>&nbsp;┃┣ OverflowError</td><td>算術演算結果が表現できない値になった場合。</td></tr>
    <tr><td>&nbsp;┃┗ ZeroDivisionError</td><td>除算や剰余演算でゼロ割り演算された場合。</td></tr>
    <tr><td>&nbsp;┣ AssertionError</td><td>assertが失敗した場合。</td></tr>
    <tr><td>&nbsp;┣ AttributeError</td><td>属性参照や代入が失敗した場合。（対象となるオブジェクトが属性参照や代入自体をサポートしていない場合は、TypeErrorとなる。）</td></tr>
    <tr><td>&nbsp;┣ BufferError</td><td>バッファ関連の操作に失敗した場合。</td></tr>
    <tr><td>&nbsp;┣ EOFError</td><td>input()がデータを読み込んでいない状態でend-of-file (EOF)に達した場合。（io.IOBase.read(), io.IOBase.readline()は、EOF に達すると空文字列を返す。）</td></tr>
    <tr><td>&nbsp;┣ ImportError</td><td>importによるロードが失敗した場合。</td></tr>
    <tr><td>&nbsp;┃┗ ModuleNotFoundError</td><td>importによるロード時、モジュールが見つからない場合 または sys.modules に None が含まれる場合。</td></tr>
    <tr><td>&nbsp;┣ LookupError</td><td>マッピング または シーケンスで使われるキーやインデクスが無効な場合（IndexError, KeyError の基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┣ IndexError</td><td>シーケンスのインデックスが範囲外の場合。（インデックスが整数でない場合は、TypeErrorとなる。）</td></tr>
    <tr><td>&nbsp;┃┗ KeyError</td><td>マッピングキー（連想配列キー）が見つからなかった場合。</td></tr>
    <tr><td>&nbsp;┣ MemoryError</td><td>メモリ不足が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ NameError</td><td>存在しないオブジェクト名が指定されている場合。（UnboundLocalError の基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┗ UnboundLocalError</td><td>値が代入されていないローカル変数を参照した場合。</td></tr>
    <tr><td>&nbsp;┣ OSError</td><td>システム関数でエラーが発生した場合。（BlockingIOError ～ TimeoutError の基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┣ BlockingIOError</td><td>ノンブロッキング処理にて処理対象のオブジェクトが事前処理等の準備が整う前に指示がされた場合。（errno EAGAIN, EALREADY, EWOULDBLOCK, EINPROGRESS）</td></tr>
    <tr><td>&nbsp;┃┣ ChildProcessError</td><td>子プロセスの操作に失敗した場合。（errorno ECHILD）</td></tr>
    <tr><td>&nbsp;┃┣ ConnectionError</td><td>コネクション関連の操作に失敗した場合。（BrokenPipeError～ ConnectionResetErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┃┣ BrokenPipeError</td><td>操作ができないコネクションのパイプ または ソケットを操作した場合。（errno EPIPE, ESHUTDOWN）</td></tr>
    <tr><td>&nbsp;┃┃┣ ConnectionAbortedError</td><td>通信先の接続が中断された場合。（errno ECONNABORTED）</td></tr>
    <tr><td>&nbsp;┃┃┣ ConnectionRefusedError</td><td>通信先の接続が拒否された場合。（errno ECONNREFUSED）</td></tr>
    <tr><td>&nbsp;┃┃┗ ConnectionResetError</td><td>通信先の接続がリセットされた場合。（errno ECONNRESET）</td></tr>
    <tr><td>&nbsp;┃┣ FileExistsError</td><td>すでに存在するファイル または ディレクトリを作成しようとした場合。（errno EEXIST）</td></tr>
    <tr><td>&nbsp;┃┣ FileNotFoundError</td><td>操作対象のファイル または ディレクトリが存在しない場合。（errno ENOENT）</td></tr>
    <tr><td>&nbsp;┃┣ InterruptedError</td><td>システムコールが中断された場合。（errno EINTR）</td></tr>
    <tr><td>&nbsp;┃┣ IsADirectoryError</td><td>ディレクトリにファイル操作（os.remove() 等）が要求された場合（errno EISDIR）</td></tr>
    <tr><td>&nbsp;┃┣ NotADirectoryError</td><td>ディレクトリ以外にディレクトリ操作（os.listdir() 等）が要求された場合。（errno ENOTDIR）</td></tr>
    <tr><td>&nbsp;┃┣ PermissionError</td><td>アクセス権がないユーザーで操作を行った場合。（errno EACCES, EPERM）</td></tr>
    <tr><td>&nbsp;┃┣ ProcessLookupError</td><td>プロセスが存在しない場合。（errno ESRCH）</td></tr>
    <tr><td>&nbsp;┃┗ TimeoutError</td><td>システム関数がシステムレベルでタイムアウトした場合。（errno ETIMEDOUT）</td></tr>
    <tr><td>&nbsp;┣ ReferenceError</td><td>弱参照プロキシ（weakref.proxy()で生成）を使って、ガーベジコレクションにより回収した後の対象オブジェクトにアクセスした場合。</td></tr>
    <tr><td>&nbsp;┣ RuntimeError</td><td>他に分類できないエラーが検出された場合。（NotImplementedError, RecursionErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┣ NotImplementedError</td><td>ユーザ定義の基底クラスにおいて、抽象メソッドが派生クラスでオーバライドされていない場合。（または クラスの一部が未実装である場合 等）</td></tr>
    <tr><td>&nbsp;┃┗ RecursionError</td><td>最大再帰回数（sys.getrecursionlimit()）を超えた場合。</td></tr>
    <tr><td>&nbsp;┣ SyntaxError</td><td>構文エラーが発生した場合。（IndentationErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┗ IndentationError</td><td>インデントに関する構文エラーが発生した場合。（TabErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃&nbsp;&nbsp;┗ TabError</td><td>インデントで使用するタブとスペースに一貫性がない場合。</td></tr>
    <tr><td>&nbsp;┣ SystemError</td><td>システムエラー（インタプリタが検知した内部エラー）が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ TypeError</td><td>型が不整合である場合。</td></tr>
    <tr><td>&nbsp;┣ ValueError</td><td>型は適切だが設定元（代入や引数等）の値が適切でない場合。（UnicodeErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃┗ UnicodeError</td><td>Unicodeのエンコード または デコードエラーが発生した場合。（UnicodeDecodeError, UnicodeEncodeError, UnicodeTranslateErrorの基底クラス。）</td></tr>
    <tr><td>&nbsp;┃&nbsp;&nbsp;┣ UnicodeDecodeError</td><td>Unicodeに関するエラーがデコード中に発生した場合。</td></tr>
    <tr><td>&nbsp;┃&nbsp;&nbsp;┣ UnicodeEncodeError</td><td>Unicodeに関するエラーがエンコード中に発生した場合。</td></tr>
    <tr><td>&nbsp;┃&nbsp;&nbsp;┗ UnicodeTranslateError</td><td>Unicodeに関するエラーが変換中に発生した場合。</td></tr>
    <tr><td>&nbsp;┣ Warning</td><td>下記サブクラスの警告が発生した場合。（DeprecationWarning ～ ResourceWarningの基底クラス。）</td></tr>
    <tr><td>&nbsp;┣ DeprecationWarning</td><td>廃止された機能に対する警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ PendingDeprecationWarning</td><td>将来廃止される予定である機能に対する警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ RuntimeWarning</td><td>曖昧なランタイム挙動に対する警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ SyntaxWarning</td><td>曖昧な構文に対する警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ UserWarning</td><td>ユーザコードによって生成される警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ FutureWarning</td><td>構文内に今後（次期バージョン等で）、意味やその構成が変わる予定があるものが含まれる場合。</td></tr>
    <tr><td>&nbsp;┣ ImportWarning</td><td>モジュールインポートの誤りが疑われる警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ UnicodeWarning</td><td>Unicode関連の警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┣ BytesWarning</td><td>bytes や bytearray に関連した警告が発生した場合。</td></tr>
    <tr><td>&nbsp;┗ ResourceWarning</td><td>リソースの使用に関連した警告が発生した場合。</td></tr>
  </tbody>
</table>

※ 各項目の詳細は[Python公式ドキュメント - 組み込み例外](https://docs.python.org/ja/3/library/exceptions.html)を参照。

### 組込み例外クラスのツリー表示サンプル

以下、前項の組込み例外クラス一覧をツリー表示した実装サンプル。<br>
`classtree`関数に`BaseException`を渡し、再帰的に`BaseException`を出力している。<br>

※ 参考元：[Pythonの組み込み例外の木構造を見てみる](https://qiita.com/amedama/items/aa840a0a98f720cfc4ca)

- ツリー表示サンプル
    ```python
    $ python
    >>> def classtree(cls, depth=0):
    ...     if depth == 0:
    ...         prefix = ''
    ...     else:
    ...         prefix = '.' * (depth * 3) + ' '
    ...     if cls.__name__.lower() == 'error':
    ...         print('{0}{1} ({2})'.format(prefix, cls.__name__, cls))
    ...     else:
    ...         print('{0}{1}'.format(prefix, cls.__name__))
    ...     for subcls in sorted(cls.__subclasses__(), key=lambda c: c.__name__):
    ...         classtree(subcls, depth+1)
    ...
    >>> if __name__ == '__main__':
    ...     print('Python Version: {0}'.format(platform.python_version()))
    ...     print()
    ...     classtree(BaseException)
    ...
    ```

- 上記の実行結果
    ```text
    Python Version: 3.6.4

    BaseException
    ... Exception
    ...... ArithmeticError
    ......... FloatingPointError
    ......... OverflowError
    ......... ZeroDivisionError
    ...... AssertionError
    ...... AttributeError
    ...... BufferError
    ...... EOFError
    ...... Error (<class 'locale.Error'>)
    ...... ImportError
    ......... ModuleNotFoundError
    ......... ZipImportError
    ...... LookupError
    ......... CodecRegistryError
    ......... IndexError
    ......... KeyError
    ...... MemoryError
    ...... NameError
    ......... UnboundLocalError
    ...... OSError
    ......... BlockingIOError
    ......... ChildProcessError
    ......... ConnectionError
    ............ BrokenPipeError
    ............ ConnectionAbortedError
    ............ ConnectionRefusedError
    ............ ConnectionResetError
    ......... FileExistsError
    ......... FileNotFoundError
    ......... InterruptedError
    ......... IsADirectoryError
    ......... ItimerError
    ......... NotADirectoryError
    ......... PermissionError
    ......... ProcessLookupError
    ......... TimeoutError
    ......... UnsupportedOperation
    ...... ReferenceError
    ...... RuntimeError
    ......... BrokenBarrierError
    ......... NotImplementedError
    ......... RecursionError
    ......... _DeadlockError
    ...... StopAsyncIteration
    ...... StopIteration
    ...... StopTokenizing
    ...... SubprocessError
    ......... CalledProcessError
    ......... TimeoutExpired
    ...... SyntaxError
    ......... IndentationError
    ............ TabError
    ...... SystemError
    ......... CodecRegistryError
    ...... TokenError
    ...... TypeError
    ...... ValueError
    ......... UnicodeError
    ............ UnicodeDecodeError
    ............ UnicodeEncodeError
    ............ UnicodeTranslateError
    ......... UnsupportedOperation
    ...... Verbose
    ...... Warning
    ......... BytesWarning
    ......... DeprecationWarning
    ......... FutureWarning
    ......... ImportWarning
    ......... PendingDeprecationWarning
    ......... ResourceWarning
    ......... RuntimeWarning
    ......... SyntaxWarning
    ......... UnicodeWarning
    ......... UserWarning
    ...... _OptionError
    ...... error (<class 'sre_constants.error'>)
    ... GeneratorExit
    ... KeyboardInterrupt
    ... SystemExit
    ```

※ エラー：`sre_constants.error`は、正規表現が曖昧な場合に発生するようだが深くは触れない。<br>
詳しくは、下記を参考。<br>
[what is sre_constants.error: nothing to repeat](https://stackoverflow.com/questions/12390238/what-is-sre-constants-error-nothing-to-repeat)

また、`help(__builtins__)`からも例外クラスを確認できる。

```python
$ python
>>> help(__builtins__)

Help on built-in module builtins:

NAME
    builtins - Built-in functions, exceptions, and other objects.

DESCRIPTION
    Noteworthy: None is the `nil' object; Ellipsis represents `...' in slices.

CLASSES
    object
        BaseException
            Exception
                ArithmeticError
                    FloatingPointError
                    OverflowError
                    ZeroDivisionError
                AssertionError
                AttributeError
                BufferError
                EOFError
                ImportError
                    ModuleNotFoundError
                LookupError
                    IndexError
                    KeyError
                MemoryError
                NameError
                    UnboundLocalError
                OSError
                    BlockingIOError
                    ChildProcessError
                    ConnectionError
                        BrokenPipeError
                        ConnectionAbortedError
                        ConnectionRefusedError
                        ConnectionResetError
                    FileExistsError
                    FileNotFoundError
                    InterruptedError
                    IsADirectoryError
                    NotADirectoryError
                    PermissionError
                    ProcessLookupError
                    TimeoutError
                ReferenceError
                RuntimeError
                    NotImplementedError
                    RecursionError
                StopAsyncIteration
                StopIteration
                SyntaxError
                    IndentationError
                        TabError
                SystemError
                TypeError
                ValueError
                    UnicodeError
                        UnicodeDecodeError
                        UnicodeEncodeError
                        UnicodeTranslateError
                Warning
                    BytesWarning
                    DeprecationWarning
                    FutureWarning
                    ImportWarning
                    PendingDeprecationWarning
                    ResourceWarning
                    RuntimeWarning
                    SyntaxWarning
                    UnicodeWarning
                    UserWarning
            GeneratorExit
            KeyboardInterrupt
            SystemExit
            …（以降省略）
```


## まとめ
- 例外処理はエラー発生時の流れを制御する仕組みで、exceptでは捕捉する例外クラスをできるだけ具体的に指定。
- BaseExceptionにはSystemExitやKeyboardInterruptも含まれるため、通常の処理で安易に捕捉しない。
- 例外を何もせず握りつぶすと原因を追えなくなるため、ログ記録や再送出を検討する。
- finallyは後片付け、elseは例外が発生しなかった場合の処理に使う。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 組み込み例外（日本語・例外クラスの公式解説）](https://docs.python.org/ja/3/library/exceptions.html)
- [Python公式チュートリアル - エラーと例外（日本語・例外処理の公式解説）](https://docs.python.org/ja/3/tutorial/errors.html)
