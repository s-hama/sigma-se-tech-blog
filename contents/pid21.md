## タイトル
Python - ニューラルネットワーク：7/14 MNIST推論のバッチ処理

## 概要
MNISTの推論処理を1件ずつではなく、複数件まとめて処理するバッチ処理として整理する。
バッチ処理を使うと、行列計算をまとめて実行できるため、処理効率を上げやすくなる。
ここでは、バッチサイズ、配列のshape、予測結果の集計を確認しながら、推論処理をまとめて実行する。

## この記事の構成
- [推論バッチ処理の実行準備](#推論バッチ処理の実行準備)<br>
  推論バッチ処理の実行準備の手順と確認ポイントを整理。
- [推論バッチ処理の実行](#推論バッチ処理の実行)<br>
  推論バッチ処理の実行の意味と要点を具体例から整理。
- [推論バッチ処理の解説](#推論バッチ処理の解説)<br>
  複数の入力をまとめて推論する処理を、配列の形状とともに確認。

## 概念の説明と実装サンプル
### 推論バッチ処理の実行準備
- バッチ推論用コードの準備<br>
    [前の記事 > Python - ニューラルネットワーク： MNISTを使ったニューラルネットワークの推論処理と実装サンプル > 推論処理の実行準備](https://sigma-se.com/detail/20/#推論処理の実行準備) でダウンロードした`ch03/neuralnet_mnist_batch.py`を使ってバッチ処理を説明する。

    ※ `ch03/neuralnet_mnist_batch.py`は、`ch03/neuralnet_mnist.py`の実行部分をバッチ処理に書き換えたもの（下記Pythonコードのコメントの「# 追記」「# 書き換え」の部分）で、3つの関数については全く同じ。

    ```python
    import sys, os
    sys.path.append(os.pardir)    # 親ディレクトリのファイルをインポートするための設定
    import numpy as np
    import pickle
    from dataset.mnist import load_mnist
    from common.functions import sigmoid, softmax

    def get_data():
        (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, flatten=True, one_hot_label=False)
        return x_test, t_test

    def init_network():
        with open("sample_weight.pkl", 'rb') as f:
            network = pickle.load(f)
        return network

    def predict(network, x):
        W1, W2, W3 = network['W1'], network['W2'], network['W3']
        b1, b2, b3 = network['b1'], network['b2'], network['b3']
        a1 = np.dot(x, W1) + b1
        z1 = sigmoid(a1)
        a2 = np.dot(z1, W2) + b2
        z2 = sigmoid(a2)
        a3 = np.dot(z2, W3) + b3
        y = softmax(a3)
        return y

    x, t = get_data()
    network = init_network()

    batch_size = 100    # 追記
    accuracy_cnt = 0

    for i in range(0, len(x), batch_size):    # 書き換え
        x_batch = x[i:i+batch_size]           # 書き換え
        y_batch = predict(network, x_batch)   # 書き換え
        p = np.argmax(y_batch, axis=1)        # 書き換え
        accuracy_cnt += np.sum(p == t[i:i+batch_size])    # 書き換え

    print("Accuracy:" + str(float(accuracy_cnt) / len(x)))
    ```

### 推論バッチ処理の実行
- バッチ推論の実行結果<br>
    上記の実行部分は、`ch03/neuralnet_mnist.py`の実行部分を**100個単位**でバッチ実行しているため、`ch03/neuralnet_mnist_batch.py`内の実行部分を実行すると`neuralnet_mnist.py`の実行時と同じ`Accuracy:0.9352`が出力される。

    - 対話モードで確認
        ```bash
        $ cd gitlocalrep
        $ cd deep-learning-from-scratch/ch03
        $ source /var/www/vops/bin/activate
        $ python neuralnet_mnist_batch.py
            Accuracy:0.9352
        ```

        しかし、これでは`ch03/neuralnet_mnist_batch.py`内の実行部分で具体的にどのような型でどのような値がどのように変化しているのかイメージが難しいため、次項のサンプルで解説。

### 推論バッチ処理の解説
- コードの処理手順<br>
    実行部分（Pythonコードのコメントの「# 追記」「# 書き換え」の部分）を（＊1）〜（＊6）と置く。

    ```python
    x, t = get_data()
    network = init_network()

    batch_size = 100    # （＊1）
    accuracy_cnt = 0

    for i in range(0, len(x), batch_size):    # （＊2）
        x_batch = x[i:i+batch_size]           # （＊3）
        y_batch = predict(network, x_batch)   # （＊4）
        p = np.argmax(y_batch, axis=1)        # （＊5）
        accuracy_cnt += np.sum(p == t[i:i+batch_size])    # （＊6）

    print("Accuracy:" + str(float(accuracy_cnt) / len(x)))
    ```

    - （＊1）一度に何件処理するかを表す**バッチサイズ**
    - （＊2）0 ～ len(x) のインデックスで増加幅が100となる \\(i\\)（1周の処理対象が100要素）のループ処理<br>
        `range`は、開始値以上・終了値未満の整数列を表す`range`オブジェクトを作成。<br>
        第3引数は、増加するスパンを指定できる。

        ```python
        $ python
        >>> list(range(0, 10))   # 0以上10未満の整数
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
        >>> list(range(5, 10))   # 5以上10未満の整数
        [5, 6, 7, 8, 9]
        >>> list(range(1, 27, 3))   # 1以上27未満で3ずつ増加
        [1, 4, 7, 10, 13, 16, 19, 22, 25]
        ```

    - （＊3）xの \\(i\\) 以上 \\(i\\) + batch_size 未満の行をx_batchに取得<br>
        ループ1周目は、\\(i\\) = 0 なのでx_batchには0～99行目の画像が格納される。<br>
        ループ2周目は、\\(i\\) = 100 なのでx_batchには100～199行目の画像が格納される。バッチサイズが100なら、x_batchのshapeは`(100, 784)`、予測結果y_batchのshapeは`(100, 10)`となる。
    - （＊4）`predict`の結果をy_batchに取得<br>
        `predict(network, x_batch)`のsigmoid, softmaxについては下記を参考。<br>
        - [Python - ニューラルネットワーク： ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/)<br>
        - [Python - ニューラルネットワーク： 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数）](https://sigma-se.com/detail/18/)
    - （＊5）`np.argmax`で**y_batchの最大値となるインデックス**を取得
        - `axis=1`は、それぞれの行を対象に最大値を取るインデックスを抽出するオプション
            ```python
            $ python
            >>> import numpy as np
            >>> x = np.array([[0.1, 0.3, 0.2, 0.9, 0.5], [0.3, 0.9, 0.1, 0.4, 0.8], [0.9, 0.2, 0.1, 0.6, 0.5]])
            >>> y = np.argmax(x, axis=1)
            >>> print(y)
            [3 1 0]
            >>>
            ```
        - 同様に`axis=0`は、それぞれの列を対象に最大値を取るインデックスを抽出するオプション
            ```python
            $ python
            >>> import numpy as np
            >>> x = np.array([[0.1, 0.3, 0.2, 0.9, 0.5], [0.3, 0.9, 0.1, 0.4, 0.8], [0.9, 0.2, 0.1, 0.6, 0.5]])
            >>> y = np.argmax(x, axis=0)
            >>> print(y)
            [2 1 0 0 1]
            >>>
            ```
    - （＊6）バッチ単位で抽出した結果pと正解tを比較し、**一致している個数（合計値）**を取得
        - sum（bool値）の例
            ```python
            $ python
            >>> import numpy as np
            >>> p = np.array([0, 3, 2, 9, 5, 3, 9, 1, 4, 8])
            >>> t = np.array([0, 4, 2, 9, 5, 4, 9, 2, 5, 9])
            >>> print(p==t)
            [ True False  True  True  True False  True False False False]
            >>> np.sum(p==t)
            5
            >>>
            ```

## まとめ
- バッチ処理は複数の入力をまとめて推論する方法で、batch_sizeは一度に処理する件数を表し、データ全体の件数ではない。
- 入力のshapeが変わるため行列計算の次元を確認し、argmaxでは予測クラスを取り出すaxisを正しく指定。
- バッチを大きくすると効率化できる一方、メモリ使用量も増えるため、実行環境に合わせて調整する。

### 参考文献
- 斎藤 康毅（\\(2016\\)）[『ゼロから作るDeep Learning ―Pythonで学ぶディープラーニングの理論と実装』（日本語・本記事シリーズの基礎文献）](https://www.oreilly.co.jp/books/9784873117584/) 株式会社オライリー・ジャパン
- [O'Reilly Japan「deep-learning-from-scratch」neuralnet_mnist_batch.py（Python・公式サンプルコード）](https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/ch03/neuralnet_mnist_batch.py)
- [NumPy Reference, numpy.argmax（英語・最大値インデックス取得の公式仕様）](https://numpy.org/doc/stable/reference/generated/numpy.argmax.html)
