## タイトル
Python - ニューラルネットワーク：13/14 重みに対する勾配とパラメータ更新

## 概要
ニューラルネットワークの重みに対して損失関数の勾配を求め、パラメータを更新する流れを整理する。
前の記事までで扱った損失関数、数値微分、勾配降下法を、ニューラルネットワークの重み更新に結び付ける段階となる。
ここでは、重みを少し変えたときに損失がどう変化するかを確認し、損失が小さくなる方向へ更新する考え方を実装する。

## この記事の構成
- [重みに対する勾配法とは](#重みに対する勾配法とは)<br>
  重みに対する勾配法の意味と基本的な考え方を整理。
- [重みに対する勾配のPython実装サンプル](#重みに対する勾配のpython実装サンプル)<br>
  重みに対する勾配のPython実装サンプルをコードや具体例で確認。
- [実装サンプルの実行確認](#実装サンプルの実行確認)<br>
  実装サンプルの実行確認をコードや具体例で確認。

## 概念の説明と実装サンプル

### 重みに対する勾配法とは

**重み**（weight）は、入力をどの程度増幅・減衰させて次の層へ伝えるかを決める係数で、一般に \\(w_{0}\\)、\\(w_{1}\\)、\\(w_{2}\\) …のように表す。学習では、損失が小さくなるようにこの値を更新する。重みの絶対値だけで入力特徴の重要度を常に判断できるわけではなく、他の重みや活性化関数も含めて解釈する必要がある。

ニューラルネットワークでは、この**重み**に対して、[Python - ニューラルネットワーク： 勾配降下法の実装サンプル](https://sigma-se.com/detail/26/) で解説した**勾配降下法**を実施し、損失が小さくなるように値を更新していく。

層の重みを行列で管理する場合、各要素に対する損失の偏微分を同じ形状の行列にまとめる。以下の数値勾配の実装では、重み要素を一つずつ変化させて偏微分を近似する。

<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
W =
\begin{pmatrix}
w_{11} & w_{12} & w_{13} \\
w_{21} & w_{22} & w_{23} \\
\end{pmatrix}
\]
</div>

<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
\frac{∂L}{∂W} =
\begin{pmatrix}
\frac{∂L}{∂w_{11}} & \frac{∂L}{∂w_{12}} & \frac{∂L}{∂w_{13}} \\
\frac{∂L}{∂w_{21}} & \frac{∂L}{∂w_{22}} & \frac{∂L}{∂w_{23}} \\
\end{pmatrix}
\]
</div>

\\(W\\) は2行3列の重み行列。<br>
\\(L\\) は対象となる損失関数で、\\(\displaystyle \frac{∂L}{∂W}\\) は各重みに対する偏微分をまとめた勾配行列を表す。

以降は、この**勾配**を求める実装サンプルを確認する。

### 重みに対する勾配のPython実装サンプル

以下、参考文献『ゼロから作るDeep Learning』から提供されている `ch04/gradient_simplenet.py` を用いたサンプル解説をしていく。

※ サンプルコードは、下記Gitからダウンロードする。<br>
Git（deep-learning-from-scratch）：
[ch04/gradient_simplenet.py](https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/ch04/gradient_simplenet.py)

ここでは、処理の流れを追いやすくするため、`ch04/gradient_simplenet.py`の`simpleNet`クラスで使われる下記3つの関数を、あえてPython対話モードで定義して確認する。

- ソフトマックス関数：common/functions.pyのsoftmax関数<br>
    ※ ソフトマックス関数の一般的な定義は下記ページを参考。<br>
    [Python - ニューラルネットワーク： 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数） > ソフトマックス関数](<https://sigma-se.com/detail/18/#ソフトマックス関数>)


    ```python
    $ python
    >>> import numpy as np
    >>>
    >>> def softmax(x):
    ...     if x.ndim == 2:
    ...         x = x.T
    ...         x = x - np.max(x, axis=0)
    ...         y = np.exp(x) / np.sum(np.exp(x), axis=0)
    ...         return y.T
    ...     x = x - np.max(x)
    ...     return np.exp(x) / np.sum(np.exp(x))
    ...
    >>>
    ```

- 交差エントロピー誤差：common/functions.py の cross_entropy_error関数<br>
    ※ 交差エントロピー誤差の処理内容については、下記ページを参考。<br>
    [Python - ニューラルネットワーク： 損失関数（2乗和誤差、交差エントロピー誤差）と実装サンプル > 交差エントロピー誤差と実装サンプル](<https://sigma-se.com/detail/22/#交差エントロピー誤差と実装サンプル>)
    [Python - ニューラルネットワーク： 交差エントロピー誤差のミニバッチ学習と実装サンプル](<https://sigma-se.com/detail/23/#交差エントロピー誤差のミニバッチ学習python実装サンプル>)

    ```python
    >>> # 上記対話モードの続き
    >>> def cross_entropy_error(y, t):
    ...     if y.ndim == 1:
    ...         t = t.reshape(1, t.size)
    ...         y = y.reshape(1, y.size)
    ...
    ...     if t.size == y.size:
    ...         t = t.argmax(axis=1)
    ...
    ...     batch_size = y.shape[0]
    ...     return -np.sum(np.log(y[np.arange(batch_size), t] + 1e-7)) / batch_size
    ...
    >>>
    ```

- 勾配処理：common/gradient.pyのnumerical_gradient関数<br>
    ※ 勾配の処理内容は下記ページの勾配関数(num_gradient)を参考。<br>
    [Python - ニューラルネットワーク： 偏微分と勾配の実装サンプル](<https://sigma-se.com/detail/25/#勾配のpython実装サンプル>)


    ```python
    >>> # 上記対話モードの続き
    >>> def numerical_gradient(f, x):
    ...     h = 1e-4
    ...     grad = np.zeros_like(x)
    ...
    ...     it = np.nditer(x, flags=['multi_index'], op_flags=['readwrite'])
    ...
    ...     while not it.finished:
    ...         idx = it.multi_index
    ...         tmp_val = x[idx]
    ...         x[idx] = float(tmp_val) + h
    ...         fxh1 = f(x)
    ...
    ...         x[idx] = tmp_val - h
    ...         fxh2 = f(x)
    ...         grad[idx] = (fxh1 - fxh2) / (2*h)
    ...
    ...         x[idx] = tmp_val
    ...         it.iternext()
    ...
    ...     return grad
    ...
    >>>
    ```

- 重みに対する勾配処理：3つの関数を呼び出した形で`ch04/gradient_simplenet.py`の`simpleNet`クラスを実装

    ```python
    >>> # 上記対話モードの続き
    >>> import sys, os
    >>>
    >>> class simpleNet:
    ...     def __init__(self):
    ...         self.W = np.array([[0.5, -0.2, 0.1],
    ...                            [0.3,  0.4, -0.5]])
    ...
    ...     def predict(self, x):
    ...         return np.dot(x, self.W)
    ...
    ...     def loss(self, x, t):
    ...         z = self.predict(x)
    ...         y = softmax(z)
    ...         loss = cross_entropy_error(y, t)
    ...
    ...         return loss
    ...
    >>>
    ```

    \\(x\\) は、**入力データ**で \\(t\\) が**教師データ**。

    predict関数は、入力データ \\(x\\) と`__init__`で設定した仮（ランダム）の重みパラメータ`self.W`の**評価結果**（積）を返す。

    loss関数は、predict関数、softmax関数を実施した \\(y\\) と教師データ \\(t\\) の**損失関数**（交差エントロピー誤差：cross_entropy_error関数）を返す。

### 実装サンプルの実行確認

以降、上記`simpleNet`の実行例を基に解説する。

- インスタンスの結果確認
    ```python
    >>> # 上記対話モードの続き
    >>> net = simpleNet()
    >>> print(net.W)
    [[ 0.5 -0.2  0.1]
     [ 0.3  0.4 -0.5]]
    >>>
    ```

    説明を再現できるように、ここでは2x3行列の重みを固定している。実際の学習では一般に、適切な方法で初期化した重みを利用する。

- 評価結果（積）の確認
    ```python
    >>> # ↑↑↑ 上記対話モードの続き
    >>> x = np.array([0.6, 0.9])
    >>> p = net.predict(x)
    >>> print(p)
    [ 0.57  0.24 -0.39]
    >>> np.argmax(p)
    0
    >>>
    ```

    `predict(x)`により、入力データ \\([0.6, 0.9]\\) と重みパラメータ`net.W`の評価結果（積）を算出している。
    （最大インデックスは0）

- 損失関数の結果確認
    ```python
    >>> # 上記対話モードの続き
    >>> t = np.array([0, 0, 1])
    >>> net.loss(x, t)
    1.7028014787132717
    >>>
    ```

    正解ラベルを\\(2\\)としたときの損失は約\\(1.70\\)となる。現在の予測クラス0とは一致していない。

- 勾配の結果確認
    ```python
    >>> # 上記対話モードの続き
    >>> def f(W):
    ...     return net.loss(x, t)
    ...
    >>> dW = numerical_gradient(f, net.W)
    >>> print(dW)
    [[ 0.28546734  0.20522925 -0.49069659]
     [ 0.42820101  0.30784387 -0.73604488]]
    >>>
    ```

    `net.loss(x, t)`を`f(W)`とし、勾配処理（`numerical_gradient`）を実施している。

    ※ `f(W)`の`W`は、勾配処理：common/gradient.pyのnumerical_gradient関数の\\(（A）\\)、\\(（B）\\)と整合性が取れるように定義したもの。

- 重みの更新確認
    ```python
    >>> loss_before = net.loss(x, t)
    >>> learning_rate = 0.1
    >>> net.W -= learning_rate * dW
    >>> loss_after = net.loss(x, t)
    >>> loss_before, loss_after
    (1.7028014787132717, 1.5860075067483186)
    ```

    勾配の逆方向へ重みを1回更新すると、この例では損失が約1.70から約1.59へ減少する。

- 結果から見る結論

    重みパラメータ \\(w_{11}\\) と重みパラメータ \\(w_{23}\\) にスポットを当てた結果を見る。

    \\(\displaystyle \frac{∂L}{∂w_{11}}\\) は約\\(0.29\\)であるため、\\(w_{11}\\)を微小量\\(h\\)増やすと、損失はおよそ\\(0.29h\\)増える。

    一方、\\(\displaystyle \frac{∂L}{∂w_{23}}\\) は約\\(-0.74\\)であるため、\\(w_{23}\\)を微小量\\(h\\)増やすと、損失はおよそ\\(0.74h\\)減る。

    よって、
    重みパラメータ \\(w_{11}\\) は、**マイナス方向**に。<br>
    重みパラメータ \\(w_{23}\\) は、**プラス方向**に**更新すべき**という結論となる。

    ※ 以上の要領で重みパラメータを**より損失が少ない重みパラメータへ**更新していくことが目的。


## まとめ
- 重みに対する勾配は、重みを変えたときの損失の変化を表し、重み行列のshapeは入力数と出力数から決まる。
- 勾配は損失が増える方向を示すため、学習では逆方向へ重みを更新。
- 数値勾配は仕組みを理解しやすい一方、大きなネットワークでは計算量が大きくなる。

### 参考文献
- 斎藤 康毅（\\(2016\\)）[『ゼロから作るDeep Learning ―Pythonで学ぶディープラーニングの理論と実装』（日本語・本記事シリーズの基礎文献）](https://www.oreilly.co.jp/books/9784873117584/) 株式会社オライリー・ジャパン
- [O'Reilly Japan「deep-learning-from-scratch」gradient_simplenet.py（Python・公式サンプルコード）](https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/ch04/gradient_simplenet.py)
