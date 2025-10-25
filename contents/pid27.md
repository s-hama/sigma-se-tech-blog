## タイトル
Python - AI : 重みに対する損失関数の勾配法と実装サンプル

## 目的
この記事では、重みに対する勾配法（勾配降下法）の実装サンプルを記載する。

## 概念の説明と実装サンプル

### 重みに対する勾配法とは

**重み**は、正解に対して**入力値**がどれだけ影響するかを示す**重要度**を表す。

**重み**という言葉からは全くイメージできない意味を持つが、これは英語の**Weigh**を直訳し、**重み**となっているからであり、本来は**大切さ**、**価値**、**重要性**という意味で命名されている。

そして、この**重み**（重要度）は、一般的に**Weigh**の \\(w\\) を取り、\\(w_{0}\\)、\\(w_{1}\\)、\\(w_{2}\\) …で表現され、**評価的に具体的な数値を入れてみて損失結果を計る**ためのパラメータとなる。

ニューラルネットワークでは、この**重み**に対して、[Python - AI : 勾配降下法の実装サンプル](https://sigma-se.com/detail/26/) で解説した**勾配降下法**を実施し、最適な**重み**を求めていく。

また、下記に示す行列のよう色々なパターンの**重み**を行列計算で一斉に**偏微分**し、最適な**重み**を求めていく。

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

\\(W\\) は、一斉に偏微分しようとしている2行3列の**重み**達。<br>
\\(L\\) は、対象となる**損失関数**で \\(\displaystyle \frac{∂L}{∂W}\\) の各要素で偏微分し、**損失関数**\\(L\\) の**勾配**を求めている。

以降は、この**勾配**を求める実装サンプルについて記載する。

### 重みに対する勾配のPython実装サンプル

以下、参考文献『ゼロから作るDeep Learning』から提供されている `ch04/gradient_simplenet.py` を用いたサンプル解説をしていく。

※ サンプルコードは、下記Gitからダウンロードする。<br>
Git(deep-learning-from-scratch)：
<a href="https://github.com/oreilly-japan/deep-learning-from-scratch">https://github.com/oreilly-japan/deep-learning-from-scratch</a>

ここでは、より分かりやすく説明するため、`ch04/gradient_simplenet.py`の`simpleNet`クラスを実装するにあたりimportされている下記3つの関数をあえてPython対話モードで定義する形で記載する。

- ソフトマックス関数：common/functions.pyのsoftmax関数<br>
    ※ ソフトマックス関数の一般的な定義は下記ページを参考。<br>
    [Python - AI : 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数） > ソフトマックス関数](<https://sigma-se.com/detail/18/#:~:text=pid18_4.png%27)%0A%20%3E%3E%3E-,%E3%82%BD%E3%83%95%E3%83%88%E3%83%9E%E3%83%83%E3%82%AF%E3%82%B9%E9%96%A2%E6%95%B0,-%E5%88%86%E9%A1%9E%E5%95%8F%E9%A1%8C%E3%81%A7>)


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
    [Python - AI : 損失関数（2乗和誤差、交差エントロピー誤差）と実装サンプル > ソフトマックス関数](<https://sigma-se.com/detail/22/#:~:text=%EF%BC%89-,%E4%BA%A4%E5%B7%AE%E3%82%A8%E3%83%B3%E3%83%88%E3%83%AD%E3%83%94%E3%83%BC%E8%AA%A4%E5%B7%AE%E3%81%A8%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB,-%E5%89%8D%E9%A0%85%E3%81%A8%E5%90%8C%E6%A7%98>)
    [Python - AI : 交差エントロピー誤差のミニバッチ学習と実装サンプル](<https://sigma-se.com/detail/23/#:~:text=%E4%BA%A4%E5%B7%AE%E3%82%A8%E3%83%B3%E3%83%88%E3%83%AD%E3%83%94%E3%83%BC%E8%AA%A4%E5%B7%AE%E3%81%AE%E3%83%9F%E3%83%8B%E3%83%90%E3%83%83%E3%83%81%E5%AD%A6%E7%BF%92%EF%BC%88Python%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB%EF%BC%89>)

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
    [Python - AI : 偏微分と勾配の実装サンプル](<https://sigma-se.com/detail/25/#:~:text=%E3%81%AB%E9%81%8E%E3%81%8E%E3%81%AA%E3%81%84%E3%80%82-,%E5%8B%BE%E9%85%8D%E3%81%AEPython%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB,-%E4%B8%8A%E8%A8%98%E3%81%A7%E3%80%81>)


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
    ...         self.W = np.random.randn(2,3)
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
