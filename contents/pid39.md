## タイトル
Python - タスク指向型対話 : 状態遷移ベースの環境準備 > MeCab, SCXML

## 目的
この記事では、状態遷移ベースのタスク指向型対話システムを作るために使用する外部ライブラリ`MeCab`と`SCXML`の概要とインストールについて記載する。

## 概要の説明と実装サンプル

### タスク指向型対話システム (状態遷移ベース) のシステム構成について

**タスク指向型**とは、対話システムが特定のタスクを遂行することを指し、これから次の記事以降でも継続して解説する天気情報案内や特定の業務を対象とした予約システム、検索システムなど遂行業務を定めている分類のことをいう。

また、これと対極する**非タスク指向型**は、雑談システムなどの特定タスク遂行を目的とせず、遂行業務を定めていない分類のことをいう。

システム構成は、**Pythonで作成する対話システム**、**Telegramサーバー**、**Telegramをインストールしたクライアント端末**（Android、iPhone、Windows、Linux、Macなど）の単純な \\(3\\) 構成でデータベースも使わない。<br>
※ 以降、Telegramインストールした端末を**Telegramクライアント**と表現する。

大まかな処理の流れとしては、**Pythonで作成する対話システム**を起動すると、 これが**Bot**として**Telegramクライアント**に表示され、ユーザー要求の入力待ち状態となる。

そして、ユーザーが要求（入力）すると**Telegramサーバー**を介し、**対話システム**（Bot）の応答制御処理を経て、結果をユーザーに返し、対話をしていく。

上記の前提と重複するがこの記事では、外部ライブラリとなる`MeCab`と`SCXML`の概要とインストールついて解説する。
これ以外にも使用する`Telegram`、`OpenWeatherMap`については、次の記事以降で記載している。

また、次の記事以降も継続して解説していく、 タスク指向型システムでは、Telegramクライアントが Windows10、Pythonの対話システムが Linux(CentOS7) となるので、コマンドは特に自身の環境に合わせて読替えること。

### 対話の文章を解析する「MeCab」の概要とインストール

まずは、大前提となる文章解析について<br>
対話の文章解析用に形態素解析（＊1）エンジンのオープンソースである`MeCab`を用いて作成する。<br>
（＊1）文章を解析し、最小単位の単語（形態素）に分割すること。

`MeCab`について、ここではインストールと呼出し方のみ解説し、理屈や詳細については触れない。

※ MeCabについての詳細は、下記サイトを参考。<br>
[【技術解説】形態素解析とは？MeCabインストール手順からPythonでの実行例まで](https://mieruca-ai.com/ai/morphological_analysis_mecab/)

- MeCabインストール<br>
    Groongaレポジトリの追加とパッケージの最新情報を取得し、mecab本体と辞書ファイルをインストールする。<br>
    - Groongaレポジトリ追加
        ```bash
        $ sudo yum install -y https://packages.groonga.org/centos/groonga-release-latest.noarch.rpm
        ```
    - パッケージ情報の更新
        ```bash
        $ sudo yum makecache
        ```
    - MeCab本体と辞書ファイルをインストール
        ```bash
        $ sudo yum install mecab mecab-devel mecab-ipadic
        ```
    - 呼出し確認
        ```bash
        $ mecab
        昨日はいい天気でしたね
        昨日 名詞,副詞可能,*,*,*,*,昨日,キノウ,キノー
        は 助詞,係助詞,*,*,*,*,は,ハ,ワ
        いい 形容詞,自立,*,*,形容詞・イイ,基本形,いい,イイ,イイ
        天気 名詞,一般,*,*,*,*,天気,テンキ,テンキ
        でし 助動詞,*,*,*,特殊・デス,連用形,です,デシ,デシ
        た 助動詞,*,*,*,特殊・タ,基本形,た,タ,タ
        ね 助詞,終助詞,*,*,*,*,ね,ネ,ネ
        EOS
        ```
    - mecab-python3のインストール<br>
        最後に上記でインストールしたMeCabをPython3から呼び出せるように`mecab-python3`をインストールし、Pythonからの呼出しを確認する。
        ```bash
        $ pip3 install mecab-python3
        ```

- Pythonから呼出し確認<br>
    以下、呼出し確認のサンプルコード`mecab-python3_test.py`
    ```python
    import MeCab

    mecab = MeCab.Tagger()

    # python3-mecabのバグ回避のため，空文字をparse
    mecab.parse('')

    # 標準入力からテキストを受け取る
    text = input("&gt;")

    node = mecab.parseToNode(text)
    while node:
        print(node.surface, node.feature)
        node = node.next
    ```

    このまま、上記サンプルコードを実行すると、3行目の`MeCab.Tagger`でMeCabのインスタンス生成時に近代文語と言われる`unidic-lite`のインストール`pip install unidic-lite`コマンドで実施するようエラーがでる。

  - 対話モード (インタプリタ)で確認
      ```python
      $ python
      >>> import MeCab
      >>>
      >>> mecab = MeCab.Tagger() # MeCabのインスタンス生成
      Failed when trying to initialize MeCab. Some things to check:
      ...（省略）...
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
        File "/var/www/vops/lib64/python3.6/site-packages/MeCab/__init__.py", line 105, in __init__
          super(Tagger, self).__init__(args)
      RuntimeError
      >>>
      ```

      なぜ、`unidic-lite`が必要なのか、辞書ファイルである`mecab-ipadic`だけでは不足なのか？についは、調べきれず不明。

      エラーメッセージの通り`unidic-lite`をインストールする。
      ```bash
      $ pip3 install unidic-lite
      ```

  - 再度、呼出し確認<br>
    今度は、対話モード (インタプリタ)でなくプログラムファイルを実行する。
    ```bash
    $ python ~/gitlocalrep/dsbook/mecab-python3_test.py
    >昨日はいい天気でしたね
    BOS/EOS,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*
    昨日 名詞,普通名詞,副詞可能,*,*,*,キノウ,昨日,昨日,キノー,昨日,キノー,和,*,*,*,*,キノウ,キノウ,キノウ,キノウ,*,*,"2,0",C2,*
    は 助詞,係助詞,*,*,*,*,ハ,は,は,ワ,は,ワ,和,*,*,*,*,ハ,ハ,ハ,ハ,*,*,*,"動詞%F2@0,名詞%F1,形容詞%F2@-1",*
    いい 形容詞,非自立可能,*,*,形容詞,連体形-一般,ヨイ,良い,いい,イー,いい,イー,和,*,*,*,*,イイ,イイ,イイ,イイ,*,*,1,C3,*
    天気 名詞,普通名詞,一般,*,*,*,テンキ,天気,天気,テンキ,天気,テンキ,漢,*,*,*,*,テンキ,テンキ,テンキ,テンキ,*,*,1,C1,*
    でし 助動詞,*,*,*,助動詞-デス,連用形-一般,デス,です,でし,デシ,です,デス,和,*,*,*,*,デシ,デス,デシ,デス,*,*,*,"形容詞%F2@-1,動詞%F2@0,名詞%F2@1",*
    た 助動詞,*,*,*,助動詞-タ,終止形-一般,タ,た,た,タ,た,タ,和,*,*,*,*,タ,タ,タ,タ,*,*,*,"動詞%F2@1,形容詞%F4@-2",*
    ね 助詞,終助詞,*,*,*,*,ネ,ね,ね,ネ,ね,ネ,和,*,*,*,*,ネ,ネ,ネ,ネ,*,*,*,"動詞%F1,名詞%F1,形容詞%F1",*
    BOS/EOS,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*,*
    ```

    上記が**形態素解析**した結果となる。

    また、実行環境によっては 下記（＊2）の文字コードに起因するエラーになるため、下記（＊3）を参考に文字コードを**UTF8**等 に変換後、実行すること。

    - （＊2）文字コードに起因するエラー
        ```bash
        $ python ~/gitlocalrep/dsbook/mecab-python3_test.py
        >昨日はいい天気でしたね
        Traceback (most recent call last):
        File "~/gitlocalrep/dsbook/mecab-python3_test.py", line 11, in <module>
            node = mecab.parseToNode(text)
        TypeError: in method 'Tagger_parseToNode', argument 2 of type 'char const *'
        ```

    - （＊3）文字コードをUTF8に変換
        ```bash
        $ LANG=ja_JP.UTF8
        $ nkf -w8 --overwrite ~/gitlocalrep/dsbook/mecab-python3_test.py
        ```

### 状態遷移によるタスクを遂行する「SCXML」の概要とインストール

**状態遷移**とは、**状態遷移ベース**または、**ネットワーク方式**とも呼ばれ、天気情報案内を例にすると**場所**や**日付**など、天気情報を取得する（絞込む）ための条件を対話で聞き出し、次の要求状態へと遷移させ、これを繰返し業務遂行する手法のこと。

※ **状態遷移ベース**は、タスク指向型対話システムの遂行手法としては、最もシンプルだが、情報を一つ一つ聞き出すといったシステム主導型の対話になる。
一問一答でユーザーを問い詰めるような遂行ではなく、一度に複数の情報を受け付ける**フレームベース**という遂行方法もあり、この詳細については、次の記事以降で掲載予定。

また、それぞれの状態遷移や受け付ける動作、組合わせなどの情報を表現するモデルのことを**有限状態オートマトン**（有限状態機械）といい、このモデルを状態遷移させてタスクを遂行する。

**有限状態オートマトン**について、ここで深く触れないが設計から考え出すと非常に大変で現実的ではないため、この記事では、**有限状態オートマトン**を記述するためのマークアップ言語である**SCXML**（State Chart XML）を用いて状態遷移を表現する。

- SCXMLのインストール(PySide2)<br>
    PythonでGUI作成のために用いられる **Qtライブラリ**の処理系である**Qt for Python**（PySide2）の**QScxmlStateMachine**という **有限状態オートマトン**を表現するクラスを使用する。

    PySide2をインストール(ver.2-5.15.0)
    ```bash
    $ source /var/www/vops/bin/activate # 仮想環境起動
    $ pip3.6 install PySide2 # PySide2をインストール
    ```
    上記でPythonから **SCXML** を使えるようになった。

    このページでは、次に記載している **SCXML** 各要素の解説に留め、次の記事以降でPythonから呼び出した実装サンプルについて解説する。

- 天気情報案内の状態遷移図(SCXML)<br>
    以下、**SCXML** で記載した天気情報案内の状態遷移図。

    states.scxml<br>
    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <scxml xmlns="http://www.w3.org/2005/07/scxml" version="1.0" initial="ask_place">
      <state id="ask_place">
        <transition event="place" target="ask_date"/>
      </state>
      <state id="ask_date">
        <transition event="date" target="ask_type"/>
      </state>
      <state id="ask_type">
        <transition event="type" target="tell_info"/>
      </state>
      <final id="tell_info"/>
    </scxml>
    ```

`state`要素、`final`要素それぞれが一つの状態遷移を表す。

また、その子要素である`transition`の`event`は、ユーザー応答の結果が期待したワードである場合（例えば "place"（場所）でいうと、"福岡県福岡市"など地名を含んでいる場合）、このイベントが発火した状態となりこの場合、`target`に指定されている次の状態 "ask_date" に遷移する。

イベントが期待したワードでなければ、イベントは発火せず、同じ状態遷移を繰り返す。

上記の要領で`ask_place`（地名指定）→ `ask_date`（日時指定）→ `ask_type`（種別：天気 or 気温）と状態遷移が進むと、最後に`final`要素の天気情報の取得結果を返す状態に遷移し、天気情報を返して処理を終了する。

以上で`MeCab`と`SCXML`の環境準備が完了。

### 参考文献
- 東中 竜一郎、稲葉 通将、水上 雅博（\\(2020\\)）『Pythonでつくる対話システム』株式会社オーム社

### GitHubサポートページ
- https://github.com/dsbook/dsbook
