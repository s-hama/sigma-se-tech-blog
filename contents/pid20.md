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
