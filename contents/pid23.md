## タイトル
Python - AI : 交差エントロピー誤差のミニバッチ学習と実装サンプル

## 目的
この記事では、交差エントロピー誤差のミニバッチ学習について簡単な実装サンプルを記載する。

## 概念の説明と実装サンプル
### ミニバッチ学習とは
機械学習では、[Python - AI : MNISTのダウンロード方法（手書き数字画像セットを取込む）> MNISTのデータ仕様](https://sigma-se.com/detail/19/#:~:text=%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%EF%BC%8810%2C000%E5%80%8B%EF%BC%89-,MNIST%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98,-%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%81%A7%E3%81%AF) のような訓練データすべて(学習用データセット 60,000枚)を対象に損失関数を求める必要がある。

60,000枚程度であれば問題ないが、ビッグデータでは**数千万のデータ**となり、すべて求めると処理時間もサーバー負荷も膨大となり現実的でない。

また、高負荷の割には、100件程度のランダム抽出結果と大きく変わらず、機械学習では数千万データの近似値として十分有効である。
この学習方法を機械学習分野では、**ミニバッチ学習**と呼び、テレビの視聴率計測など一般的に広く使用されている。

### 交差エントロピー誤差のミニバッチ学習（定義）
下記\\(（A）\\)は、[Python - AI : 損失関数（2乗和誤差、交差エントロピー誤差）と実装サンプル）> 交差エントロピー誤差の定義](<https://sigma-se.com/detail/22/#:~:text=array(t))%0A0.0-,%E4%BA%A4%E5%B7%AE%E3%82%A8%E3%83%B3%E3%83%88%E3%83%AD%E3%83%94%E3%83%BC%E8%AA%A4%E5%B7%AE%E3%81%AE%E5%AE%9A%E7%BE%A9,-%E4%BA%A4%E5%B7%AE%E3%82%A8%E3%83%B3%E3%83%88%E3%83%AD%E3%83%94%E3%83%BC%E8%AA%A4%E5%B7%AE>) で解説した交差エントロピー誤差の定義。

<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
E = -\sum_{i=1}^{n} t_{k} \log y_{k}\hspace{5mm}･･･（A）
\]
</div>

- \\(t_{k}\\)：訓練データ
- \\(y_{k}\\)：ニューラルネットワークの出力
- \\(k\\)：データの次元数

これは、一つのデータ（数字 0 ～ 9 のいずれか）に対して、ニューラルネットワークの出力が10個の配列（正解予想）と、訓練データの出力が10個の配列（正解が1、不正解が0）となる損失関数を表している。

これをすべてのデータに対して実施し、その和を表現すると下記\\(（B）\\)の定義となる。

<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\normalsize
E = -\frac{1}{N}\sum_{i=1}^{n}\sum_{j=1}^{k} t_{nk} \log \ y_{nk}\hspace{5mm}･･･（B）
}
\]
</div>

- \\(N\\)：データの個数<br>
※ MNISTの場合、学習用データセットの60,000個。一つあたりの損失平均となるようにNで割る。
- \\(k\\)：データの次元数
※ MNISTの場合、訓練データの種類(数字 0 ～ 9 に対応する10個)<br>
- \\(t_{nk}\\)：訓練データである\\(t_{k}\\)がN個分。
※ MNISTの場合、学習用ラベルデータセットの60,000個。<br>
- \\(y_{nk}\\)：ニューラルネットワークの出力である\\(y_{k}\\)がN個分。
※ MNISTの場合、学習用ラベルデータセットの60,000個。

### 交差エントロピー誤差のミニバッチ学習（MNISTの準備）
次にMNISTを使った**ミニバッチ学習の準備**と**データの内容**について解説する。

※ MNISTのデータについては、[Python - AI : MNISTのダウンロード方法（手書き数字画像セットを取込む）> MNISTのデータ仕様](https://sigma-se.com/detail/19/#:~:text=%E3%83%87%E3%83%BC%E3%82%BF%E3%82%BB%E3%83%83%E3%83%88%EF%BC%8810%2C000%E5%80%8B%EF%BC%89-,MNIST%E3%81%AE%E3%83%87%E3%83%BC%E3%82%BF%E4%BB%95%E6%A7%98,-%E6%A9%9F%E6%A2%B0%E5%AD%A6%E7%BF%92%E3%81%A7%E3%81%AF) を参考のこと。<br>
※ リポジトリクローンについては、[Python - AI : MNISTのダウンロード方法（手書き数字画像セットを取込む）> MNISTのダウンロード](https://sigma-se.com/detail/19/#:~:text=%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E3%83%A9%E3%83%99%E3%83%AB-,MNIST%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89,-%E4%B8%8B%E8%A8%98%E3%80%81mnist) を参考のこと。

MNISTの**学習用データセット**と**検証用データセット**をダウンロードする。
```bash
$ cd gitlocalrep    # ローカルのGitリポジトリに移動
$ cd deep-learning-from-scratch/ch03    # Git (deep-learning-from-scratch) のカレントディレクトリに移動
$ python
 >>> import sys, os
 >>> sys.path.append(os.pardir)
 >>> import numpy as np
 >>> from dataset.mnist import load_mnist
 >>>
 >>> (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)
 >>>
 >>> print(x_train.shape)     # 詳細は下記（＊2）に記載
 (60000, 784)
 >>> print(t_train.shape)     # 詳細は下記（＊3）に記載
 (60000, 10)
 >>>
```

- 補足
  - （＊1）load_mnist関数の引数
    引数 normalize は、入力画像を 0.0 ～ 1.0 に正規化するかどうかをBool値で設定する。
    Falseの場合、入力画像のピクセルは 0 ～ 255 となる。

    引数 flatten は、入力画像を1次元にするかどうかをBool値で設定する。
    Falseの場合、入力画像は1 * 28 * 28 の3次元配列として格納され、Trueの場合、1次元配列(要素：784)として格納される。

    引数 one_hot_labelは、ラベルをone_hot表現で格納するかどうかをBool値で設定する。
    one_hot表現の場合は、正解となるラベルのみ1でそれ以外は0の配列となる。

    戻り値は、(訓練画像、訓練ラベル), (テスト画像, テストラベル)の形式でMNISTデータを返す。
  - （＊2）x_train.shape (形状)
    784列(= 28 × 28)の画像データが学習用データセット数の60,000枚あることを表している。
  - （＊3）t_train.shape (形状)
    10列(正解となるラベルのみ1でそれ以外は0の配列)の教師データが学習用データセット数の60,000個あることを表している。

### 交差エントロピー誤差のミニバッチ学習（Python実装サンプル）
最後に上記で準備したMNISTのデータセットを使い、**ミニバッチ学習のPython実装サンプル**について解説する。

MNISTの学習用画像データセット（60,000枚）の中から**100枚**抜出して、**交差エントロピー誤差の損失関数**を求めるサンプル。

まず、前準備として、[Python - AI : MNISTを使った推論バッチ処理の実装サンプル > 推論バッチ処理の実行準備](https://sigma-se.com/detail/21/#:~:text=%E3%81%A8%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB-,%E6%8E%A8%E8%AB%96%E3%83%90%E3%83%83%E3%83%81%E5%87%A6%E7%90%86%E3%81%AE%E5%AE%9F%E8%A1%8C%E6%BA%96%E5%82%99,-%E5%89%8D%E3%81%AE%E8%A8%98%E4%BA%8B) で解説した`ch03/neuralnet_mnist_batch.py`の`init_network()`と`predict(network, x)`を定義する。
```bash
$ cd gitlocalrep    # ローカルのGitリポジトリに移動
$ cd deep-learning-from-scratch/ch03    # Git (deep-learning-from-scratch) のカレントディレクトリに移動
$ python
 >>> import sys, os
 >>> sys.path.append(os.pardir)
 >>> import numpy as np
 >>> import pickle
 >>> from dataset.mnist import load_mnist
 >>> from common.functions import sigmoid, softmax
 >>>
 >>> def init_network():
 ...     with open("sample_weight.pkl", 'rb') as f:
 ...         network = pickle.load(f)
 ...     return network
 ...
 >>> def predict(network, x):
 ...     W1, W2, W3 = network['W1'], network['W2'], network['W3']
 ...     b1, b2, b3 = network['b1'], network['b2'], network['b3']
 ...     a1 = np.dot(x, W1) + b1
 ...     z1 = sigmoid(a1)
 ...     a2 = np.dot(z1, W2) + b2
 ...     z2 = sigmoid(a2)
 ...     a3 = np.dot(z2, W3) + b3
 ...     y = softmax(a3)
 ...     return y
 ...
 >>>
```

そして、交差エントロピー誤差のミニバッチ学習を定義。
```bash
 >>> def cross_entropy_error(y, t):
 ...     if y.ndim == 1:    # 次元が 1 の場合
 ...         t = t.reshape(1, t.size)
 ...         y = y.reshape(1, y.size)
 ...     batch_size = y.shape[0]
 ...     return -np.sum(t * np.log(y + 1e-7)) / batch_size
 ...
 >>>
```

\\(y\\) は、ニューラルネットワーク（推論バッチ処理）の出力となり、以降の解説で引数yにpredict(network, x_batch)の戻り値を設定する。

次に、MNISTの学習用データセットと検証用データセットをダウンロードする。
```bash
 >>> (x_train, t_train), (x_test, t_test) = load_mnist(normalize=True, one_hot_label=True)
 >>>
```

次にnp.random.choiceを使用しランダムで**100枚**抽出する。
```bash
 >>> train_size = x_train.shape[0]
 >>> batch_size = 100
 >>> batch_mask = np.random.choice(train_size, batch_size)
 >>> x_batch = x_train[batch_mask]
 >>> t_batch = t_train[batch_mask]
 >>>
 >>> print(batch_mask)    # np.random.choiceの結果
 [ 2759 48331 20881 29315 30035 55711 47969  1338 54067 23424 14789  9722
 38601 10138 24036 23811   284 43467 41042 39683 49572 20247 29728 23176
 50987  4855 43468  7179  2815 29033 46578 25623 41615 34833 12651 35969
 51498 34685 30303 57205 16641 39057 45010 35152 19620 34228 55637 44070
 25063 14112 45717 32403 32209 26388 27572 53492 46367 15161 38462 26947
 30193 45931 25658 24854 33528 41892 55989 32053 43699 22615 42090  3430
  1568 57173 35969 11839 26384 16123 31217 30323 46844 37015 28731 46525
 15412 19736 16773 12655 37365 52095 11550 46947 34077 31528  9691 44021
  6473 41599  7001  4999]
 >>>
```

次に100枚抜き出したニューラルネットワーク(推論バッチ処理)の出力結果をy_batchに取得する。
```bash
 >>> network = init_network()
 >>> y_batch = predict(network, x_batch)
 >>>
```

そして、最後にニューラルネットワーク(推論バッチ処理)の出力`y_batch`と`t_batch`を引数に交差エントロピー誤差を求める。
```bash
 >>> cross_entropy_error(y_batch, t_batch)
 0.20627920610480943
 >>>
```

100枚のミニバッチ学習結果は、**約0.2**という結果になった。

ちなみに上記はload_mnistで引数`one_hot_label=True`を指定したone_hot表現のミニバッチ処理だが、one_hot表現でなく**ラベルのデータセットをダウンロードした場合**は、下記の実装となる。
```bash
 >>> def cross_entropy_error(y, t):
 ...     if y.ndim == 1:
 ...         t = t.reshape(1, t.size)
 ...         y = y.reshape(1, y.size)
 ...     batch_size = y.shape[0]
 ...     return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size
 ...
 >>>
```

one_hot表現では、\\(t=0\\) のデータはすべて \\(0\\) になるが、ラベルデータとなると全てデータが対象となる。

引数 one_hot_label に関する差異
- one_hot_label=True の時
```bash
...     return -np.sum(t * np.log(y + 1e-7)) / batch_size
```
- one_hot_label=False の時
```bash
...     return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size
```

### 参考文献
- 斎藤 康毅（2018）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
