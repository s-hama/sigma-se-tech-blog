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
  <table class="table" style="width: 100%; margin-bottom: 2em;">
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
  <table class="table" style="width: 100%; margin-bottom: 2em;">
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
