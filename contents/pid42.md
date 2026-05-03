## タイトル
Python - タスク指向型対話 : 4/5 フレームベースの環境準備 > SVM（sklearn）と学習データの作成

## 目的
この記事では、フレームベースのタスク指向型対話システムを作るために使用するSVM（sklearn）の概要及びインストールと学習データの作成について記載する。

## 実装内容
### タスク指向型対話システム（フレームベース）のシステム構成について

システム構成は、状態遷移ベースと同様に**Pythonで作成する対話システム**、**Telegramサーバー**、**Telegramをインストールしたクライアント端末**（Android、iPhone、Windows、Linux、Macなど）の単純な**3構成**でデータベースも使わない。<br>
※ 以降、Telegramインストールした端末を**Telegramクライアント**と表現する。

大まかな処理の流れとしては、Pythonで作成する対話システムを起動すると、これがBotとしてTelegramクライアントに表示され、ユーザー要求の入力待ち状態となる。

その後、ユーザーが要求（入力）するとTelegramサーバーを介し、対話システム（Bot）の応答制御処理を経て、結果をユーザーに返し対話していく。

上記の前提と重複するがこの記事では、SVM（sklearn）の概要とインストールと学習データ作成について解説する。

また、次の記事以降も継続して解説していく、タスク指向型システムのフレームベースについての動作環境は、状態遷移ベースと同じでTelegramクライアントがWindows、Pythonの対話システムがLinux（CentOS7）となるので、コマンドは特に自身の環境に合わせて読み替えること。

### フレームと対話行為を推定するSVM（sklearn）の概要とインストール

まず、**フレーム**とは、一度に複数の情報を受付けられるように**スロット**と呼ばれる**属性**と**値**からなる入力情報を複数持つデータ構造のことで、遂行手法としてフレームベースとも呼ばれる。

フレームベースの基本処理構成は、**発話処理部**、**対話管理部**（状態更新、行動決定）、**発話生成部**から成っていて、**パイプラインアーキテクチャ**または**Vモデル**とも呼ばれる。<br>
※ この記事では、フレームベースに関する解説は概要レベルに留め、次の記事以降でSVMやCRFを絡めた実装を例に掘り下げて解説する。

始めのユーザーの発話直後に処理される**発話処理部**では、発話内容から**発話の意図となる対話行為**を推定する。

**対話行為**は、対話の大分類（意図）を表す**対話行為タイプ**とその詳細情報である**コンセプト**で構成される。

例えば、ユーザーの入力値が「福岡の明日の天気は？」の場合
発話行為タイプを「天気情報の要求」に分類し、コンセプトの場所（都道府県）を「福岡」、日付を「明日」、情報種別を「天気」という具合に分類（推定）する。

対話行為タイプとコンセプトは、開発環境（＊1）、（＊2）によって呼び方が違うので注意。<br>
- （＊1）「Google Home」は、対話行為タイプをインテント、コンセプトをエンティティと呼ぶ。
- （＊2）「Amazon Alexa」は、対話行為タイプをインテント、コンセプトをスロットと呼ぶ。<br>
（上記フレームのスロット（属性／値）と（＊2）のスロットは表現は同じ「スロット」という表現だが意味が違うので混同注意。）

この**対話行為タイプ**を推定するためにパターン識別用の機械学習方法の一つである**SVM**（support vector machine）を使用する。<br>
※ パターン識別の理屈については、ここで触れないがデータを2つのグループに分類する問題に優れており、2分類化することにおいては、最も優秀な識別能力を持つとされる。

SVMによる学習は、Pythonの機械学習ライブラリである**sklearn**（scikit-learn）を用いて実装する。

- sklearn, dillのインストール
    ```bash
    $ pip3 install sklearn
    ```

    また、学習結果を保存するため シリアライズモジュールである**dill**もインストールする。
    ```bash
    $ pip3 install dill
    ```

以上がSVMの環境準備。

また、対話行為の分類基準を確立するため、学習データ（事例）が必要になってくるため、次項で作成方法を解説する。

### 学習データの作成

この案内対話で使用する発話行為タイプとコンセプトを以下のように定義する。

- 発話行為タイプ
    <table class="table" style="width: 100%;">
    <thead>
        <tr>
        <th scope="col">発話行為名</th>
        <th scope="col">発話行為キー</th>
        <th scope="col">備考</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>天気情報の要求</td><td>request-weather</td><td>ユーザーが天気情報を要求している。</td></tr>
        <tr><td>伝達情報の初期化</td><td>initialize</td><td>ユーザーが案内の初期化を要求している。</td></tr>
        <tr><td>伝達情報の訂正</td><td>correct-info</td><td>ユーザーが発話行為の推定を訂正要求している。</td></tr>
    </tbody>
    </table>

- コンセプト
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">属性名</th>
        <th scope="col">属性キー</th>
        <th scope="col">値</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>場所（都道府県）</td><td>place</td><td>都道府県のいずれか</td></tr>
        <tr><td>日付</td><td>date</td><td>今日、明日等の日付</td></tr>
        <tr><td>情報種別</td><td>type</td><td>天気 or 気温</td></tr>
    </tbody>
    </table>

例えば、上記発話行為タイプの学習データを作成する場合<br>
前方を「発話行為キー」、後方を「ユーザーの入力値」とし、そのまま愚直に書くと

    ```
    request-weather 福岡の天気は？
    request-weather 明日の福岡の気温教えて
    correct-info 大阪じゃなくて福岡です
    correct-info 天気じゃなく気温
    initialize もう一度はじめから
    initialize リセットして！
    …
    ```
という具合に発話行為タイプ別の都道府県別でさらにニュアンスを変えた学習データを一つ一つ手動で書かなければならず、現実的でないため、タグ付けした学習データを作り、これを量産するプログラムを準備する。

まず、学習データにコンセプトの属性キーでタグを付けた代表データ（examples.txt）なるものを準備する。<br>
※ da=XXXX でどの発話行為タイプのデータか定義している。

- examples.txt
    ```xml
    da=request-weather
    大阪
    大阪です
    明日
    明日です
    天気
    天気です
    大阪の明日
    大阪の明日です
    大阪の天気
    大阪の天気です
    大阪の天気を教えてください
    明日の天気
    明日の天気です
    明日の天気を教えてください
    明日の大阪の天気
    明日の大阪の天気です
    明日の大阪の天気を教えてください
    大阪の明日の天気
    大阪の明日の天気です
    大阪の明日の天気を教えてください

    da=initialize
    もう一度はじめから
    はじめから
    はじめからお願いします
    最初から
    最初からお願いします
    初期化してください
    キャンセル
    すべてキャンセル

    da=correct-info
    大阪じゃない
    大阪じゃなくて
    大阪じゃないです
    大阪ではありません
    明日じゃない
    明日じゃなくて
    明日じゃないです
    明日ではありません
    天気じゃない
    天気じゃなくて
    天気じゃないです
    天気ではありません
    ```

次に上記代表データを読込んで対象のタグに応じた辞書（都道府県名、日付、情報種別）からランダムで一つ抽出し、学習データを作成するプログラム（generate_da_samples.py）を準備する。<br>
※ 下記のプログラムでは、代表データ一行あたり\\(1000\\)個の学習データを作成している。

- generate_da_samples.py
    ```python
    import re
    import random
    import json
    import xml.etree.ElementTree

    # 都道府県名のリスト
    prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
            '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
            '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
            '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
            '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # 日付のリスト
    dates = ["今日","明日"]

    # 情報種別のリスト
    types = ["天気","気温"]

    # サンプル文に含まれる単語を置き換えることで学習用事例を作成
    def random_generate(root):
        buf = ""
        # タグがない文章の場合は置き換えしないでそのまま返す
        if len(root) == 0:
            return root.text
        # タグで囲まれた箇所を同じ種類の単語で置き換える
        for elem in root:
            if elem.tag == "place":
                pref = random.choice(prefs)
                buf += pref
            elif elem.tag == "date":
                date = random.choice(dates)
                buf += date
            elif elem.tag == "type":
                _type =  random.choice(types)
                buf += _type
            if elem.tail is not None:
                buf += elem.tail
        return buf

    # 学習用ファイルの書き出し先
    fp = open("da_samples.dat","w")

    da = ''
    # examples.txt ファイルの読み込み
    for line in open("examples.txt","r"):
        line = line.rstrip()
        # da= から始まる行から対話行為タイプを取得
        if re.search(r'^da=',line):
            da = line.replace('da=','')
        # 空行は無視
        elif line == "":
            pass
        else:
            # タグの部分を取得するため，周囲にダミーのタグをつけて解析
            root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
            # 各サンプル文を1000倍に増やす
            for i in range(1000):
                sample = random_generate(root)
                # 対話行為タイプ，発話文，タグとその文字位置を学習用ファイルに書き出す
                fp.write(da + "\t" + sample + "\n")

    fp.close()
    ```

以下、上記`generate_da_samples.py`処理の実行順解説。

- 都道府県名、日付、情報種別の辞書を定義
    ```python
    … (省略) …
    # 都道府県名のリスト
    prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
            '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
            '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
            '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
            '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

    # 日付のリスト
    dates = ["今日","明日"]

    # 情報種別のリスト
    types = ["天気","気温"]
    … (省略) …
    ```

- da_samples.datを書き込みモードで定義<br>
    作成する学習用データファイル`da_samples.dat`を新規作成し、書き込みモードで開いた`fp`を定義する。<br>
    ※ openは、指定したファイルが存在しなければ新規作成した状態で開き、存在していれば上書き状態で開く。<br>
    但し、指定したファイルがおかれているディレクトリが存在しない場合は、エラーとなるので注意。
    ```python
    … (省略) …
    # 学習用ファイルの書き出し先
    fp = open("da_samples.dat","w")
    … (省略) …
    ```

- examples.txtファイルの読み込み<br>
上記で準備した代表データ（examples.txt）を読み込みモードで開き、読込んだ行数分ループし（＊3）or（＊4）or（＊5）を実行する。<br>
  - （＊3）正規表現モジュール`re`で`da=`から始まるかどうかチェックし、始まるのであれば、右辺の発話行為タイプを`da`に保持する。
  - （＊4）空白行とみなしスキップし、何もしない。
  - （＊5）XMLとして解析するため（最上位のタグは1つでなければならない）、対象行を`dummy`タグで囲い、`fromstring`で文字列から`xml.etree.ElementTree.Element`にパースしたものを`root`に保持する。
    この`root`を引数に\\(1000\\)回`random_generate`メソッド（処理詳細は下記（＊6）を参照）を呼出し、対話行為タイプと`random_generate`の戻り値`sample`を`fp`に書き込む。
    ```python
    da = ''
    for line in open("examples.txt","r"):
        line = line.rstrip()
        if re.search(r'^da=',line):
            da = line.replace('da=','')
        elif line == "":
            pass
        else:
            root = xml.etree.ElementTree.fromstring("<dummy>"+line+"</dummy>")
            for i in range(1000):
                sample = random_generate(root)
                fp.write(da + "\t" + sample + "\n")
    ```
  - （＊6）random_generate メソッドの処理
      引数の`root`内にタグが存在しない場合（`len(root) == 0`）、root直下のテキストをそのまま返す。<br>
      以降は、`root`内のタグに応じて、都道府県名 or 日付 or 情報種別の辞書からそれぞれからランダム抽出した結果と対象タグ末尾の発話文（`tail`）を`buf`に加算して返す。
      ```python
      def random_generate(root):
          buf = ""
          if len(root) == 0:
              return root.text
          for elem in root:
              if elem.tag == "place":
                  pref = random.choice(prefs)
                  buf += pref
              elif elem.tag == "date":
                  date = random.choice(dates)
                  buf += date
              elif elem.tag == "type":
                  _type =  random.choice(types)
                  buf += _type
              if elem.tail is not None:
                  buf += elem.tail
          return buf
      ```

- 最後に`fp`を閉じて処理終了
    ```python
    … (省略) …
    fp.close()
    … (省略) …
    ```

最後に実行確認

- generate_da_samples.pyの実行確認<br>
上記の代表データ（examples.txt）がgenerate_da_samples.pyと同じフォルダ内にある状態で実行する。<br>
（もちろんgenerate_da_samples.pyまでのファイルパスは各自環境と読替えること。）
    ```bash
    $ python ~/gitlocalrep/dsbook/generate_da_samples.py
    ```

- da_samples.datの確認<br>
    代表データ（examples.txt）の学習データが40個でそれぞれ\\(1000\\)個の学習データを出力しているため、da_samples.datは、\\(10000\\)個のデータとなっている。
    ```bash
    $ cat ~/gitlocalrep/dsbook/da_samples.dat
    request-weather 高知
    request-weather 大分
    request-weather 京都
    … (省略) …
    equest-weather 青森です
    request-weather 神奈川です
    request-weather 神奈川です
    … (省略) …
    request-weather 今日
    request-weather 明日
    request-weather 今日
    … (省略) …
    initialize もう一度はじめから
    initialize はじめから
    initialize はじめからお願いします
    … (省略) …
    correct-info 福岡じゃない
    correct-info 神奈川じゃない
    correct-info 広島じゃない
    … (省略) …
    ```

以上で学習データの準備が完了。

### 参考文献
- 東中 竜一郎、稲葉 通将、水上 雅博（\\(2020\\)）『Pythonでつくる対話システム』株式会社オーム社

### GitHubサポートページ
- https://github.com/dsbook/dsbook
