## タイトル
Python - 例外処理：try・exceptと組込み例外クラス

## 概要

Pythonのtry・except・else・finallyと組込み例外クラスを整理する。

整数への変換が成功する場合、ValueErrorを処理する場合、別の例外を呼び出し元へ伝える場合を同じ関数で比較する。実行経路を追いながら捕捉する例外とtryの範囲を決める。例外階層の一覧と過去のツリー出力は参照用に掲載する。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [例外処理と例外クラス](#例外処理と例外クラス)<br>
  成功・捕捉・伝播で通る経路とtryの範囲を比較。
- [組込み例外クラス一覧](#組込み例外クラス一覧)<br>
  発生条件から例外クラスを調べるための一覧。
- [組込み例外クラスのツリー表示サンプル](#組込み例外クラスのツリー表示サンプル)<br>
  実行環境の例外階層を調べる方法と過去の出力例。

## 対象環境と利用上の注意
- 本文記載時の環境<br>
Python \\(3.6.4\\)。掲載した例外クラスのツリー出力は、この環境で取得したもの。
- 確認時期<br>
2026年9月にPython公式ドキュメントと照合。処理経路の比較例はPython 3.12.2で実行確認。
- 現在そのまま利用できない箇所<br>
Python 3.6.4当時のツリー出力は履歴として残している。<br>
Pythonの更新で例外階層は追加・変更されるため、掲載ツリーを現行版の完全な一覧として利用せず、利用中のバージョンの公式ドキュメントを確認する。

## 解説と実装サンプル

### 例外処理と例外クラス

例外は処理の失敗などを知らせる仕組みである。`try`には例外の発生を想定する処理を書き、`except`には指定した例外への対処を書く。例外クラスを指定すると、処理できる原因を選んで捕捉できる。

- 入力を変えて実行経路を比べる<br>
  次の関数は整数への変換だけをtryに入れる。`"123"`、`"abc"`、`None`を渡して通る経路を確認する。

  ```python
  def show_integer(raw):
      try:
          value = int(raw)
      except ValueError:
          print("except: 整数へ変換できません")
      else:
          print("else:", value)
      finally:
          print("finally: 処理終了")


  for raw in ("123", "abc", None):
      print("input:", repr(raw))
      try:
          show_integer(raw)
      except TypeError:
          print("caller: TypeError")
  ```

  ```text
  input: '123'
  else: 123
  finally: 処理終了
  input: 'abc'
  except: 整数へ変換できません
  finally: 処理終了
  input: None
  finally: 処理終了
  caller: TypeError
  ```

  | 入力 | int()の結果 | 関数内の経路 | 呼び出し元への例外 |
  | --- | --- | --- | --- |
  | `"123"` | 変換成功 | try → else → finally | なし |
  | `"abc"` | ValueError | try → except → finally | 捕捉済みなのでなし |
  | `None` | TypeError | try → finally | TypeErrorが伝わる |

  `else`はtryが例外なく終了した場合に実行される。`finally`は捕捉されない例外で関数を抜ける際にも実行されるが、例外を消す役割ではない。最後のTypeErrorは呼び出し元で捕捉しているため3ケースを続けて確認できる。

  ここでは文字列の形式不正を利用者へ伝え、文字列ではない値が渡された場合は呼び出し側の問題として伝播させている。Noneも通常の入力として受け付ける仕様なら、先に未設定を判定するなど対処を変える。何を回復可能な失敗とみなすかを決めてから例外を選ぶ。

- tryの範囲を狭めて原因を取り違えない<br>
  入力の変換と変換後の処理を同じtryへ入れると、後段のValueErrorまで「入力が不正」と扱うおそれがある。次の例では変換に成功した後の処理をelseへ分ける。

  ```python
  def use_value(value):
      raise ValueError("後段の設定が不正です")


  def handle(raw):
      try:
          value = int(raw)
      except ValueError:
          print("入力を整数にしてください")
      else:
          use_value(value)


  try:
      handle("123")
  except ValueError as error:
      print("呼び出し元:", str(error))
  ```

  ```text
  呼び出し元: 後段の設定が不正です
  ```

  else内の例外は同じtryに対応するexceptでは捕捉されない。変換には成功しているため、後段の失敗を入力ミスに読み替えず呼び出し元へ伝えられる。

  ファイルを閉じる用途では通常`with open(...)`を使う。[ファイル操作の記事](https://sigma-se.com/detail/32/#file%20object型--ファイル操作オブジェクト)に読み取り位置とクローズの例を掲載している。finally内でreturnすると元の戻り値や例外を上書きし得るため、後始末と結果の返却は分ける。

  `BaseException`は`SystemExit`や`KeyboardInterrupt`も含む最上位の基底クラスである。通常のアプリケーション処理では直接捕捉せず、対処できる具体的な例外を指定する。

### 組込み例外クラス一覧
- 代表的な例外と発生条件<br>
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
- 例外階層の出力<br>
    以下、前項の組込み例外クラス一覧をツリー表示した実装サンプル。<br>
    `classtree`関数に`BaseException`を渡し、サブクラスを再帰的にたどる。組込み例外だけでなく、その時点で読み込まれているモジュールや利用者が定義した例外も含まれるため、出力はimport済みの内容でも変わる。<br>

    ※ 参考元：[Pythonの組み込み例外の木構造を見てみる](https://qiita.com/amedama/items/aa840a0a98f720cfc4ca)

    - ツリー表示サンプル
        ```python
        $ python
        >>> import platform
        >>>
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

- exceptには対処できる例外を指定する。指定と異なる例外は呼び出し元へ伝わる。
- elseはtryが例外なく終了した場合、finallyは捕捉されない例外で抜ける場合にも実行される。
- tryの範囲を狭めると入力の問題と後段の失敗を取り違えにくくなる。
- 例外階層の出力はPythonのバージョンや読み込んだモジュールで変わる。過去の出力と現在の一覧を区別する。

### 参考文献
- 金城 俊哉（\\(2018\\)）『現場ですぐに使える! Pythonプログラミング逆引き大全313の極意』株式会社昭和システム
- [Python公式ドキュメント - 組み込み例外（日本語・例外クラスの公式解説）](https://docs.python.org/ja/3/library/exceptions.html)
- [Python公式チュートリアル - エラーと例外（日本語・例外処理の公式解説）](https://docs.python.org/ja/3/tutorial/errors.html)
- [Python公式チュートリアル - エラーと例外（日本語・try、else、finallyの動作）](https://docs.python.org/ja/3/tutorial/errors.html)
