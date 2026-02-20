## タイトル
Python - 例外 : 例外処理と組込み例外クラス

## 目的
この記事では、Pythonの例外処理と組込み例外クラスそれぞれの概要について記載する。

## 解説と実装サンプル

### 例外処理と例外クラス

文字通り、**例外**（正常系でない想定外のエラー）が発生した場合に対処する処理を**例外処理**と呼び、Pythonでは、メイン処理を**try句**に、例外処理を**except句**に記載する。

また、**except句**に指定する**例外クラス**によって、どの例外をキャッチするか指定することができる。

- 例外クラス BaseException を指定した場合の構文例
    ```python
    $ python
    >>> try:
    ...     # メイン処理を記載…
    >>> except BaseException:
    ...     # BaseExceptionクラスでキャッチした場合の例外処理を記載…
    >>>
    ```

ただし、`BaseException`は、Pythonすべての組込み**例外クラス**の派生元（基底）となっており、すべての例外キャッチしてしまうため（ユーザーの妨げになる場合もあるため）、`Exception`クラス等のキャッチしたい目的に応じた**例外クラス**を指定する。

### 組込み例外クラス一覧

以下、Pythonの組込み **例外クラス**とそれぞれの概要。<br>
すべて前項で記載した `BaseException`から派生する。<br>

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
    <tr><td>&nbsp;┃┣ FloatingPointError</td><td>浮動小数点の演算で失敗した場合。※ 3.7以降のバージョンでは使われていないので注意。（＊1）</td></tr>
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

※ 各項目の詳細は下記マニュアルを参照。
https://docs.python.org/ja/3.6/library/exceptions.html
