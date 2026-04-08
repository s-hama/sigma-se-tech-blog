## タイトル
Python - タスク指向型対話 : フレームベースのSVM（sklearn）モデル学習実装サンプル

## 目的
この記事では、フレームベースのタスク指向型対話システムを作るために使用するSVM（sklearn）のモデル学習実装サンプルについて記載する。

## 解説と実装サンプル
### モデル学習の実装サンプル

先行記事で作成した学習データ`da_samples.dat`（＊1）を**MeCab**（＊2）で最小単位の単語（形態素）に分割し、**SVM**（＊3）で対話行為タイプを推定（モデル学習）する実装サンプル。
- （＊1）[Python - タスク指向型対話 : フレームベースの環境準備 > SVM（sklearn）と学習データの作成 > 学習データの作成](<https://sigma-se.com/detail/42/#:~:text=%E3%82%92%E8%A7%A3%E8%AA%AC%E3%81%99%E3%82%8B%E3%80%82-,%E5%AD%A6%E7%BF%92%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E4%BD%9C%E6%88%90,-%E3%81%93%E3%81%AE%E6%A1%88%E5%86%85%E5%AF%BE%E8%A9%B1>) 
- （＊2）[Python - タスク指向型対話 : 状態遷移ベースの環境準備 > MeCab, SCXML > 対話の文章を解析する「MeCab」の概要とインストール](<https://sigma-se.com/detail/39/#:~:text=%E5%AF%BE%E8%A9%B1%E3%81%AE%E6%96%87%E7%AB%A0%E3%82%92%E8%A7%A3%E6%9E%90%E3%81%99%E3%82%8B%E3%80%8CMeCab%E3%80%8D%E3%81%AE%E6%A6%82%E8%A6%81%E3%81%A8%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB>) 
- （＊3）[Python - タスク指向型対話 : フレームベースの環境準備 > SVM（sklearn）と学習データの作成 > フレームと対話行為を推定するSVM（sklearn）の概要とインストール](<https://sigma-se.com/detail/42/#:~:text=%E3%83%95%E3%83%AC%E3%83%BC%E3%83%A0%E3%81%A8%E5%AF%BE%E8%A9%B1%E8%A1%8C%E7%82%BA%E3%82%92%E6%8E%A8%E5%AE%9A%E3%81%99%E3%82%8BSVM%EF%BC%88sklearn%EF%BC%89%E3%81%AE%E6%A6%82%E8%A6%81%E3%81%A8%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB>) 


- train_da_model.py
    ```python
    import MeCab
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    from sklearn.preprocessing import LabelEncoder
    import dill

    # MeCabの初期化
    mecab = MeCab.Tagger()
    mecab.parse('')

    sents = []
    labels = []

    # generate-samples.txt の出力である samples.dat の読み込み
    for line in open("da_samples.dat","r"):
        line = line.rstrip()
        # samples.dat は発話行為タイプ，発話文，タグとその文字位置が含まれている
        da, utt = line.split('\t')
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                # MeCabの出力から単語を抽出
                word, feature_str = line.split("\t")
                words.append(word)
        # 空白区切りの単語列をsentsに追加
        sents.append(" ".join(words))
        # 発話行為タイプをlabelsに追加
        labels.append(da)

    # TfidfVectorizerを用いて，各文をベクトルに変換
    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
    X = vectorizer.fit_transform(sents)

    # LabelEncoderを用いて，ラベルを数値に変換
    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(labels)

    # SVMでベクトルからラベルを取得するモデルを学習
    svc = SVC(gamma="scale")
    svc.fit(X,Y)

    # 学習されたモデル等一式を svc.modelに保存
    with open("svc.model","wb") as f:
        dill.dump(vectorizer, f)
        dill.dump(label_encoder, f)
        dill.dump(svc, f)
    ```

    以下、処理解説。<br>
    ※ 機械学習では、推定対象となるものを**ラベル**や**クラス**と呼ぶ。<br>
    今回のデータでは、発話行為タイプの**request-weather**がラベルとなるため、コメントや変数名の表現もラベルとなっている。

  - sentsとlabelsの作成<br>
    学習データ`da_samples.dat`を読み込み、それぞれの行に対して下記要領で発話文字列を単語分割した`sents`と発話行為タイプ`labels`をそれぞれ作成する。
    - （＊4）行の末尾の空白を削除し（rstrip）、タブで分割（split）する。
    - （＊5）1つ目分割結果（発話行為タイプ）を`da`に、2つ目分割結果（発話文字列）を`utt`に格納する。
    - （＊6）mecabで最小単位の単語（形態素）に分割し（splitlines）、最後（EOS）であればループを終了、最後（EOS）でなければタブで分割（split）し、先頭単語（word）のみを単語配列（words）に追加する。
    - （＊7）単語配列（words）を空白区切りに置換え`sents`に追加する。
    - （＊8）発話行為タイプ（da）を`labels`に追加する。

    ```python
    for line in open("da_samples.dat","r"):
        line = line.rstrip()
        # samples.dat は発話行為タイプ，発話文，タグとその文字位置が含まれている
        da, utt = line.split('\t')
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                # MeCabの出力から単語を抽出
                word, feature_str = line.split("\t")
                words.append(word)
        # 空白区切りの単語列をsentsに追加
        sents.append(" ".join(words))
        # 発話行為タイプをlabelsに追加
        labels.append(da)
    ```

- 発話情報の変換<br>
    上記で取得した発話内容`sents`と発話行為タイプ`labels`の関連付けを学習させるために発話情報を数値列に変換する必要がある。<br>
    その作成には`TfidfVectorizer`を用いて変換する。

    これを**素性ベクトル**と呼び、後続処理で**ラベル**との関連付け学習を行うために作成している。<br>
    fit_transformで発話内容`sents`を素性ベクトルに変換したものが`X`で、発話情報にある単語の登場頻度と学習データから推測できる単語の重要度をもとに素数ベクトルを自動生成している。

    ```python
    # TfidfVectorizerを用いて，各文をベクトルに変換
    vectorizer = TfidfVectorizer(tokenizer=lambda x:x.split(), ngram_range=(1,3))
    X = vectorizer.fit_transform(sents)
    ```

- 変換後の数値列を`Y`に保持<br>
    上記と同様にfit_transformで発話行為タイプ**labels**（ラベル）を数値列に変換したものを`Y`に保持する。
    ```python
    # LabelEncoderを用いて，ラベルを数値に変換
    label_encoder = LabelEncoder()
    Y = label_encoder.fit_transform(labels)
    ```

- ラベルを取得するモデルを学習させる<br>
    コメントの通り、発話内容**sents**を素性ベクトル化した`X`から、発話行為タイプ**labels**（ラベル）を数値列化した**Y**を取得するモデルを**SVM**を用いて学習させている。<br>
    ※ **モデル**とは素性ベクトルの各要素とラベルとの関連を定義した大量の通知データのこと指す。
    ```python
    # SVMでベクトルからラベルを取得するモデルを学習
    svc = SVC(gamma="scale")
    svc.fit(X,Y)
    ```

- svc.modelに保存<br>
    最後に素性ベクトル作成時に用いた`vectorizer`とラベルを数値列化する際に用いた`label_encoder`、そしてモデル学習時に用いた **svc**達を**dill**を用いて、ファイルに出力する。
    ```python
    # 学習されたモデル等一式を svc.modelに保存
    with open("svc.model","wb") as f:
        dill.dump(vectorizer, f)
        dill.dump(label_encoder, f)
        dill.dump(svc, f)
    ```

- 実行確認<br>
    上記実装サンプル（train_da_model.py）の実行確認<br>
    ※ 実行後`svc.model`が生成されていれば成功。
    ```bash
    $ python ~/gitlocalrep/dsbook/train_da_model.py
    ```

### 学習結果の確認

前項で作成した`svc.model`が正しく推定できるか以下のテストプログラムを実行して確認する。

- `da_extractor.py`（テストプログラム）
    ```python
    import MeCab
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.svm import SVC
    from sklearn.preprocessing import LabelEncoder
    import dill

    mecab = MeCab.Tagger()
    mecab.parse('')

    # SVMモデルの読み込み
    with open("svc.model","rb") as f:
        vectorizer = dill.load(f)
        label_encoder = dill.load(f)
        svc = dill.load(f)

    # 発話から発話行為タイプを推定  
    def extract_da(utt):
        words = []
        for line in mecab.parse(utt).splitlines():
            if line == "EOS":
                break
            else:
                word, feature_str = line.split("\t")
                words.append(word)
        tokens_str = " ".join(words)
        X = vectorizer.transform([tokens_str])
        Y = svc.predict(X)
        # 数値を対応するラベルに戻す
        da = label_encoder.inverse_transform(Y)[0]
        return da

    for utt in ["大阪の明日の天気","もう一度はじめから","東京じゃなくて"]:
        da = extract_da(utt)
        print(utt,da)
    ```

以下、テストプログラム（da_extractor.py）の処理解説。
