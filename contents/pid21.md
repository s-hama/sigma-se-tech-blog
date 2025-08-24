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
