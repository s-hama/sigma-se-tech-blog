## タイトル
Python - AI : MNISTを使ったニューラルネットワークの推論処理と実装サンプル

## 目的
この記事では、MNISTを使ったニューラルネットワークの推論処理についての簡単な実装サンプルを記載する。

## 概念の説明と実装サンプル
### 推論処理の実行準備
参考文献の『ゼロから作るDeep Learning』から提供されている推論処理のサンプルコード（`ch03/neuralnet_mnist.py`）をダウンロードする。

Git(deep-learning-from-scratch)：
<a href="https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/dataset/mnist.py">https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/dataset/mnist.py</a>

MNISTのダウンロードについては、[前の記事 > Python - AI : MNISTのダウンロード方法（手書き数字画像セットを取込む）> MNISTのダウンロード](https://sigma-se.com/detail/19/#:~:text=%E3%83%87%E3%83%BC%E3%82%BF%E3%81%AE%E3%83%A9%E3%83%99%E3%83%AB-,MNIST%E3%81%AE%E3%83%80%E3%82%A6%E3%83%B3%E3%83%AD%E3%83%BC%E3%83%89,-%E4%B8%8B%E8%A8%98%E3%80%81mnist)を参照


### 推論処理のニューロン構成と関数定義
- ニューロン構成について<br>
入力層：784個（画像データ28 x 28 = 784（px））<br>
隠れ層1：50（任意の値）<br>
隠れ層2：100（任意の値）<br>
出力層：10（数字0～9の10クラス）

- 実装サンプル（関数定義）<br>
以下、ch03/neuralnet_mnist.py内の3つの関数定義。<br>
  ```python
  import sys, os
  sys.path.append(os.pardir) # 親ディレクトリのファイルをインポートするための設定
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
  ```

  `init_network()`では、pickleファイルとなる`sample_weight.pkl`を読み込んでいる。

  ※ pickleファイルには、重みとバイアスのパラメータがdictionary型で保存されている。<br>
  ※ predict(network, x)のsigmoid, softmaxについては、下記を参考。<br>
  ・[Python - AI : ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/)<br>
  ・[Python - AI : 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数）](https://sigma-se.com/detail/18/)

### 推論処理の実行
- ch03/neuralnet_mnist.py内の実行処理
  ```python
  x, t = get_data()    # … 1.
  network = init_network()    # … 2.

  accuracy_cnt = 0
  for i in range(len(x)):    # … 3.
      y = predict(network, x[i])    # … 4.
      p= np.argmax(y)    # … 5.
      if p == t[i]:    # … 6.
          accuracy_cnt += 1    # … 7.

  print("Accuracy:" + str(float(accuracy_cnt) / len(x)))    # … 8.
  ```

- 実行処理の解説<br>
  1. `get_data()`でMNISTデータセットを取得。<br>
  2. `init_network()`でpickleファイルを読み込む。<br>
  3. \\(x\\)の画像データ60000枚をfor文でループ。<br>
  4. 1枚の画像データに対して`predict(network, x[i])`を実行し、下記のNumPy配列のように数字0～9それぞれの確立を出力。<br>
    ※ 0である確率：20%、1である確率：10%、2である確率：4%、… 9である確率：5%
      ```python
      [ 0.2, 0.1, 0.04 , … , 0.05  ]    # 0 ～ 9 それぞれの確率 (20%, 10%, 4%,  … , 5%)
      ```
  5. 「4.」の結果であるNumPy配列\\(y\\)に対して、最も確率が高い要素のインデックスを取得。<br>
  6. 推論処理出した「5.」の予測結果が正解ラベル\\(t\\)と一致しているかチェック。<br>
  7. 一致していれば、認識制度を加算。<br> 
  8. 最後に正解率を出力。<br>

- 実行結果<br>
実際に上記を対話モードで実行すると`Accuracy:0.9352`が出力される。
  ```python
  $ cd gitlocalrep
  $ cd deep-learning-from-scratch/ch03
  $ source /var/www/vops/bin/activate
  $ python neuralnet_mnist.py
  Accuracy:0.9352
  ```
  上記実装サンプルでは、93％程度の精度だったが、実際のニューラルネットワークでは、さらにニューラルネットワークの構造や「4.」の関数`predict`内の処理にあたる学習方法を工夫し、99％以上の精度を出していく。

### 参考文献
- 斎藤 康毅（2018）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
