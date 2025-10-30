## タイトル
Python - AI : MNISTのダウンロード方法（手書き数字画像セットを取込む）

## 目的
この記事では、MNISTのダウンロード方法についての簡単な実装サンプルについて記載する。

## 概念の説明と実装サンプル
### MNISTとは
**MNIST**（Mixed National Institute of Standards and Technology database）とは、数字画像（1～9）から構成され、手書き数字の訓練画像が60,000枚、テスト画像が10,000枚が用意された画像データセットのことで、機械学習の分野で最も利用されている。

また、手書き数字の訓練画像が60,000枚、テスト画像が10,000枚の「1枚」に対して**画像データ**と**その画像の正解となるラベルデータ**がペアとなっており、下記の4つのファイルで構成されている。
- train-images-idx3-ubyte : 学習用 画像データセット（60,000枚）
- train-labels-idx1-ubyte : 学習用 ラベルデータセット（60,000個）
- t10k-images-idx3-ubyte : 検証用 画像データセット（10,000枚）
- t10k-labels-idx1-ubyte : 検証用 ラベルデータセット（10,000個）

### MNISTのデータ仕様
機械学習では画像を数値として扱う必要があるため、**バイナリデータ**となっており、画像とラベルデータが紐付いている。

※ 下記、画像、ラベルのデータフォーマットについては、下記サイトを参考に記載。<br>
参考URL（WEB ARCH LABO）：https://weblabo.oscasierra.net/python/ai-mnist-data-detail.html

以下、画像とラベルのフォーマット仕様。
- 画像データのフォーマット（train-images-idx3-ubyte、t10k-images-idx3-ubyte）
  <table class="table" style="width: 100%; margin-bottom: 2em; table-layout: fixed;">
    <thead>
      <tr>
        <th scope="col">offset</th>
        <th scope="col">type</th>
        <th scope="col">value</th>
        <th scope="col">description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>0000</td><td>32 bit integer</td><td>0x00000803(2051)</td><td>識別子（定数）</td></tr>
      <tr><td>0004</td><td>32 bit integer</td><td>60000</td><td>画像データの数</td></tr>
      <tr><td>0008</td><td>32 bit integer</td><td>28</td><td>1画像あたりのデータ行数</td></tr>
      <tr><td>0012</td><td>32 bit integer</td><td>28</td><td>1画像あたりのデータ列数</td></tr>
      <tr><td>0016</td><td>unsigned byte</td><td>0 ～ 255</td><td>1つめの画像の1ピクセル目の値</td></tr>
      <tr><td>0017</td><td>unsigned byte</td><td>0 ～ 255</td><td>1つめの画像の2ピクセル目の値</td></tr>
      <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
      <tr><td>xxxx</td><td>unsigned byte</td><td>0 ～ 255</td><td>最後の画像の784ピクセル目の値</td></tr>
    </tbody>
  </table>

- ラベルデータのフォーマット（train-labels-idx1-ubyte、t10k-labels-idx1-ubyte）
  <table class="table" style="width: 100%; margin-bottom: 2em; table-layout: fixed;">
    <thead>
      <tr>
        <th scope="col">offset</th>
        <th scope="col">type</th>
        <th scope="col">value</th>
        <th scope="col">description</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>0000</td><td>32 bit integer</td><td>0x00000803(2049)</td><td>識別子（定数）</td></tr>
      <tr><td>0004</td><td>32 bit integer</td><td>60000 or 10000</td><td>ラベルデータの数</td></tr>
      <tr><td>0008</td><td>unsigned byte</td><td>0 ～ 9</td><td>1つ目のデータのラベル</td></tr>
      <tr><td>0009</td><td>unsigned byte</td><td>0 ～ 9</td><td>2つ目のデータのラベル</td></tr>
      <tr><td>...</td><td>...</td><td>...</td><td>...</td></tr>
      <tr><td>xxxx</td><td>unsigned byte</td><td>0 ～ 9</td><td>最後のデータのラベル</td></tr>
    </tbody>
  </table>

### MNISTのダウンロード
下記、`mnist.py`を使用し、MNISTをダウンロードする。

Git（deep-learning-from-scratch）：https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/dataset/mnist.py

- リポジトリをクローン
  ```bash
  $ cd gitlocalrep
  $ git clone https://github.com/oreilly-japan/deep-learning-from-scratch.git
  Cloning into 'deep-learning-from-scratch'...
  remote: Enumerating objects: 381, done.
  remote: Total 381 (delta 0), reused 0 (delta 0), pack-reused 381
  Receiving objects: 100% (381/381), 4.93 MiB | 4.16 MiB/s, done.
  Resolving deltas: 100% (197/197), done.
  ```

- カレントディレクトに移動<br>
  `mnist.py`の利用時は、カレントディレクトを ch01、ch02、ch03 … ch08 のいずれかで実施する必要がある。<br>
  ここでは、ch03から実施する。
  ```bash
  $ cd deep-learning-from-scratch/ch03
  ```

- ダウンロード<br>
下記、load_mnistによってMNISTデータセットのダウンロードを行っているが、初回のみオンラインである必要があり数分かかる。<br />
初回で読み込み時に`pickle`というローカルファイルが作成され、ダウンロード結果を保持しているので、2回目以降は、オフラインかつ、すぐに処理が終わる。<br />
※ Pythonの`pickle`は、プログラム実行中のオブジェクト情報をファイルとして保存できる機能。
  ```bash
  $ python
   >>> import sys, os
   >>> sys.path.append(os.pardir)    # 親ディレクトリのファイルをインポートするための設定
   >>> from dataset.mnist import load_mnist
   >>>
   >>> (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)    # MNISTデータセットのダウンロード
   Downloading train-images-idx3-ubyte.gz ...
   Done
   Downloading train-labels-idx1-ubyte.gz ...
   Done
   Downloading t10k-images-idx3-ubyte.gz ...
   Done
   Downloading t10k-labels-idx1-ubyte.gz ...
   Done
   Converting train-images-idx3-ubyte.gz to NumPy Array ...
   Done
   Converting train-labels-idx1-ubyte.gz to NumPy Array ...
   Done
   Converting t10k-images-idx3-ubyte.gz to NumPy Array ...
   Done
   Converting t10k-labels-idx1-ubyte.gz to NumPy Array ...
   Done
   Creating pickle file ...
   Done!
   >>>
   >>> print(x_train.shape)    # データ形状の確認：学習用 ラベルデータセット
   (60000, 784)
   >>> print(t_train.shape)    # データ形状の確認：学習用 画像データセット
   (60000,)
   >>> print(x_test.shape)    # データ形状の確認：検証用 ラベルデータセット
   (10000, 784)
   >>> print(t_test.shape)    # データ形状の確認：検証用 画像データセット
   (10000,)
   >>>
  ```

- load_mnist関数の概要<br>
引数 normalize は、入力画像を**0.0 ～ 1.0 に正規化するかどうか**Bool値で設定する。<br>
Falseの場合、入力画像のピクセルは 0 ～ 255 となる。<br>
引数 flatten は、入力画像を**1次元にするかどうか**Bool 値で設定する。<br>
Falseの場合、入力画像は1 * 28 * 28 の3次元配列として格納され、Trueの場合、1次元配列(要素：784)として格納される。<br>
引数 one_hot_label は、ラベルを **one_hot表現で格納するか**Bool値で設定する。<br>
one_hot 表現の場合は、正解となるラベルのみ 1 でそれ以外は、0 の配列となる。<br>
戻り値は、（訓練画像, 訓練ラベル）, （テスト画像, テストラベル）の形式でMNISTデータを返す。

### 画像データ表示確認
`ch03/mnist_show.py`に訓練画像1枚目「5」の確認用ソースコードが記載されている。<br>
下記は、この中の`show`にあたる箇所を`save`に置換え、画像ファイルを出力するサンプル。
```bash
$ python
 >>> import sys, os
 >>> sys.path.append(os.pardir)
 >>> import numpy as np
 >>> from dataset.mnist import load_mnist
 >>> from PIL import Image
 >>>
 >>> def img_save(img):
 ...     pil_img = Image.fromarray(np.uint8(img))
 ...     pil_img.save('/var/www/vops/ops/macuos/static/macuos/img/pid19_1.png')    # ＊1 mnist_show.py では、pil_img.show()
 ...
 >>> (x_train, t_train), (x_test, t_test) = load_mnist(flatten=True, normalize=False)
 >>>
 >>> img = x_train[0]
 >>> label = t_train[0]
 >>> print(label)
 5
 >>> print(img.shape)
 (784,)
 >>> img = img.reshape(28, 28)
 >>> print(img.shape)
 (28, 28)
 >>> img_save(img)    # ＊1 mnist_show.py では、img_show()
 >>>
```

- pid19_1.png<br>
期待通り、数字の手書き画像「5」が出力された。<br>
![pid19_1](/static/tblog/img/pid19_1.png)

### 参考文献
- 斎藤 康毅（\\(2018\\)）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
