## タイトル
Python - AI : MNISTを使った推論バッチ処理の実装サンプル

## 目的
この記事では、MNISTを使った推論バッチ処理についての簡単な実装サンプルを記載する。

## 概念の説明と実装サンプル
### 推論バッチ処理の実行準備
[前の記事 > Python - AI : MNISTを使ったニューラルネットワークの推論処理と実装サンプル > 推論処理の実行準備](https://sigma-se.com/detail/20/#:~:text=%E3%81%A8%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB-,%E6%8E%A8%E8%AB%96%E5%87%A6%E7%90%86%E3%81%AE%E5%AE%9F%E8%A1%8C%E6%BA%96%E5%82%99,-%E5%8F%82%E8%80%83%E6%96%87%E7%8C%AE%E3%81%AE%E3%80%8E%E3%82%BC) でダウンロードした`ch03/neuralnet_mnist_batch.py`を使ってバッチ処理を説明する。

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

上記の実行部分は、`ch03/neuralnet_mnist.py`の実行部分を**100個単位**でバッチ実行しているため、`ch03/neuralnet_mnist_batch.py`内の実行部分を実行すると`neuralnet_mnist.py`の実行時と同じ`Accuracy:0.9352`が出力される。

- 対話モードで確認
    ```bash
    $ cd gitlocalrep
    $ cd deep-learning-from-scratch/ch03
    $ source /var/www/vops/bin/activate
    $ python neuralnet_mnist_batch.py
        Accuracy:0.9352
    ```

    しかし、これでは`ch03/neuralnet_mnist_batch.py`内の実行部分で具体的にどのような型でどのような値がどのように変化しているのかイメージが難しいため、次項のサンプルで解説する。

### 推論バッチ処理の解説

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

- （＊1）どの程度のバッチ（束）で処理するかの**バッチ数**
- （＊2）0 ～ len(x) のインデックスで増加幅が100となる \\(i\\)（1周の処理対象が100要素）のループ処理<br>
    `range`は、指定した開始と終了時のインデックスで配列を作成する。<br>
    第3引数は、増加するスパンを指定できる。

    ```python
    $ python
    >>> list(range(0, 10))   # 0 ～ 10 までの配列
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    >>> list(range(5, 10))   # 5 ～ 10 までの配列
    [5, 6, 7, 8, 9]
    >>> list(range(1, 27, 3))   # 1 ～ 27 までのインデックスを3ずつ増加
    [1, 4, 7, 10, 13, 16, 19, 22, 25]
    ```

- （＊3）xの \\(i\\) ～ \\(i\\) + batch_size の配列をx_batchに取得<br>
    ループ1週目は、\\(i\\) = 0 なのでx_batchには0～99の配列が格納される。<br>
    ループ2週目は、\\(i\\) = 100 なのでx_batchには、100～199の配列が格納される。
- （＊4）`predict`の結果をy_batchに取得<br>
    `predict(network, x_batch)`のsigmoid, softmaxについては下記を参考。<br>
    - [Python - AI : ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/)<br>
    - [Python - AI : 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数）](https://sigma-se.com/detail/18/)
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
        >>> p = np.array([0.1, 0.3, 0.2, 0.9, 0.5, 0.3, 0.9, 0.1, 0.4, 0.8])
        >>> t = np.array([0.1, 0.4, 0.2, 0.9, 0.5, 0.4, 0.9, 0.2, 0.5, 0.9])
        >>> print(p==t)
        [ True False  True  True  True False  True False False False]
        >>> np.sum(p==t)
        5
        >>>
        ```

### 参考文献
- 斎藤 康毅（\\(2018\\)）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
