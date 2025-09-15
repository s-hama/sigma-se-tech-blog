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
