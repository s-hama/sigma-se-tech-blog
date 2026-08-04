## タイトル
Python - ニューラルネットワーク：4/14 代表的な活性化関数の実装まとめ

## 概要
ステップ関数、シグモイド関数、ReLU関数、恒等関数、ソフトマックス関数をPythonで実装し、それぞれの使いどころを整理する。
活性化関数はすべて同じ役割ではなく、中間層で使いやすいもの、回帰の出力層で使うもの、分類の出力層で使うものがある。
ここでは、関数ごとの特徴とNumPy実装をまとめて確認する。

## この記事の構成
- [ステップ関数](#ステップ関数)<br>
  ステップ関数の仕組みと要点を具体例から整理。
- [シグモイド関数](#シグモイド関数)<br>
  シグモイド関数の仕組みと要点を具体例から整理。
- [ReLU関数](#relu関数)<br>
  ReLU関数の仕組みと要点を具体例から整理。
- [恒等関数](#恒等関数)<br>
  恒等関数の仕組みと要点を具体例から整理。
- [ソフトマックス関数](#ソフトマックス関数)<br>
  ソフトマックス関数の仕組みと要点を具体例から整理。

## 概念の説明と実装サンプル
### ステップ関数
- 0と1を切り替える処理<br>
    [前の記事 > ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/) で触れた**ステップ関数**で、不連続な非線形の**活性化関数**であり**階段関数**とも呼ばれる。

    - 定義<br>
    \\(x\\) が \\(0\\) より大きければ、\\(1\\) を出力し、\\(0\\) 以下であれば \\(0\\) を出力。
    <div style="display: flex; margin-left: 1rem; font-size: 1.1em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
    \[
    {\normalsize
    h(x) =
    \begin{cases}
    0 \hspace{5pt}\text{if}\hspace{5pt}x \leqq 0 \\
    1 \hspace{5pt}\text{if}\hspace{5pt}x > 0
    \end{cases}
    }
    \]
    </div>

    - 実装
    ```bash
    $ python
     >>> import numpy as np
     >>> import matplotlib.pylab as plt
     >>> def step_func(x):    # ステップ関数の定義
     ...    return np.array(x > 0, dtype=int)
     ...
    ```

    - グラフ出力
    ```bash
    $ python
     >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5まで、描画間隔を0.1刻みに設定
     >>> y = step_func(x)    # ステップ関数をコール
     >>> plt.title("step_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'step_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y')
     >>> plt.ylim(-0.1, 1.1)    # y軸の範囲を設定
     (-0.1, 1.1)
     >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
     >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
     >>> plt.plot(x, y)    # グラフの描画
     [&lt;matplotlib.lines.Line2D object at 0x7fc13041e278&gt;]
     >>> plt.savefig('pid18_1.png')    # グラフの出力
    ```
    ![pid18_1](/static/tblog/img/pid18_1.png)

### シグモイド関数
- 滑らかな出力への変換<br>
    [前の記事 > ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/) で触れた**シグモイド関数**で、非線形の**活性化関数**に分類される。

    - 定義<br>
    出力値は、\\(x\\) が小さいほど \\(0\\) に近づき、\\(x\\) が大きいほど \\(1\\) に近づく。
    <div style="display: flex; margin-left: 1rem; font-size: 1.1em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
    \[
    h(x) = \frac{1}{1+e^{-x}}
    \]
    </div>

    - 実装
    ```bash
    $ python
     >>> import numpy as np
     >>> import matplotlib.pylab as plt
     >>> def sigmoid_func(x):    # シグモイド関数の定義
     ...     return 1 / (1 + np.exp(-x))    # 自然対数の底 (e) の -x 乗
     ...
    ```

    - グラフ出力
    ```bash
    $ python
     >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5まで、描画間隔を0.1刻みに設定
     >>> y = sigmoid_func(x)    # シグモイド関数をコール
     >>> plt.title("sigmoid_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'sigmoid_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y')
     >>> plt.ylim(-0.1, 1.1)    # y軸の範囲を設定
     (-0.1, 1.1)
     >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
     >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
     >>> plt.plot(x, y)
     [&lt;matplotlib.lines.Line2D object at 0x7f727fbc1be0&gt;]
     >>> plt.savefig('/var/www/vops/ops/macuos/static/macuos/img/pid18_2.png')    # グラフの出力
    ```
    ![pid18_2](/static/tblog/img/pid18_2.png)

### ReLU関数
- 0以下を0にする処理<br>
    **ReLU**（Rectified Linear Unit：正規化線形ユニット）と呼ばれ、非線形の**活性化関数**に分類される。<br>
    ※ 最近では、ニューラルネットワークにおいて、**シグモイド関数**より、**ReLU関数**が多く用いられるようになった。<br>

    - 定義<br>
    \\(x\\) が \\(0\\) より大きい場合、\\(x\\) を出力し、\\(0\\) 以下である場合、\\(0\\) を出力。
    <div style="display: flex; margin-left: 1rem; font-size: 1.1em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
    \[
    {\normalsize
    h(x) =
    \begin{cases}
    x \hspace{5pt}\text{if}\hspace{5pt}x > 0 \\
    0 \hspace{5pt}\text{if}\hspace{5pt}x \leqq 0
    \end{cases}
    }
    \]
    </div>

    - 実装
    ```bash
    $ python
     >>> import numpy as np
     >>> import matplotlib.pylab as plt
     >>> def relu_func(x):    # ReLU関数の定義
     ...     return np.maximum(0, x)
     ...
    ```

    - グラフ出力
    ```bash
    $ python
     >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5まで、描画間隔を0.1刻みに設定
     >>> y = relu_func(x)    # ReLU関数をコール
     >>> plt.title("relu_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'relu_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y')
     >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
     >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
     >>> plt.plot(x, y)
     [&lt;matplotlib.lines.Line2D object at 0x7fbf1cfeecc0&gt;]
     >>> plt.savefig('/var/www/vops/ops/macuos/static/macuos/img/pid18_3.png')
     >>>
    ```
    ![pid18_3](/static/tblog/img/pid18_3.png)

### 恒等関数
- 入力をそのまま出力する処理<br>
    **出力層**で使われる線形の**活性化関数**に分類される。

    - 定義<br>
    \\(x\\) をそのまま出力。
    <div style="display: flex; margin-left: 1rem; font-size: 1.1em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
    \[
    {\normalsize
    h(x) = x
    }
    \]
    </div>


    - 実装
    ```bash
    $ python
     >>> import numpy as np
     >>> import matplotlib.pylab as plt
     >>> def identity_func(x):    # 恒等関数の定義
     ...     return x
     ...
    ```

    - グラフ出力
    ```bash
    $ python
     >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5まで、描画間隔を0.1刻みに設定
     >>> y = identity_func(x)    # 恒等関数をコール
     >>> plt.title("identity_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'identity_func\n# arange:-5.0, 5.0, 0.1, xlabel:x, ylabel:y')
     >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
     >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
     >>> plt.plot(x, y)
     [&lt;matplotlib.lines.Line2D object at 0x7fba4d928f60&gt;]
     >>> plt.savefig('/var/www/vops/ops/macuos/static/macuos/img/pid18_4.png')
     >>>

    ```
    ![pid18_4](/static/tblog/img/pid18_4.png)

### ソフトマックス関数
- 確率分布への変換<br>
    **分類問題**で使われる非線形の**活性化関数**に分類される。

    - 定義<br>
    \\(k=1,\ldots,n\\) とすると、\\(k\\) 番目の出力 \\(h(x_{k})\\) を次の式で表す。各出力は入力ベクトル全体に依存し、出力の合計は\\(1\\)になる。
    <div style="display: flex; margin-left: 1rem; font-size: 1.1em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
    \[
    {\normalsize
    h(x_{k}) = \frac{e^{x_{k}}}{\sum_{i=1}^{n} e^{x_{i}}}
    }
    \]
    </div>

    - 実装
    ```bash
    $ python
     >>> def softmax_func(x):    # ソフトマックス関数の定義
     ...     shifted_x = x - np.max(x)    # オーバーフローを防ぐ
     ...     exp_x = np.exp(shifted_x)
     ...     sum_exp_x = np.sum(exp_x)
     ...     y = exp_x / sum_exp_x
     ...     return y
     ...
    ```

    - 実行例
    ```bash
    $ python
     >>> x = np.array([0.3, 2.9, 4.0])
     >>> y = softmax_func(x)
     >>> y
     array([0.01821127, 0.24519181, 0.73659691])
     >>> np.sum(y)
     1.0
    ```

## まとめ
- ReLUは0以下を0、正の値をそのまま出力し、ステップ関数とは正の領域の扱いが異なる。中間層でよく使われる。
- 恒等関数は入力値をそのまま出力するため、主に回帰問題の出力層で使われる。
- ソフトマックス関数は多クラス分類の出力層で使われ、指数計算のオーバーフローを避ける数値安定化が必要になる。

### 参考文献
- 斎藤 康毅（\\(2016\\)）[『ゼロから作るDeep Learning ―Pythonで学ぶディープラーニングの理論と実装』（日本語・本記事シリーズの基礎文献）](https://www.oreilly.co.jp/books/9784873117584/) 株式会社オライリー・ジャパン
- [O'Reilly Japan「deep-learning-from-scratch」functions.py（Python・公式サンプルコード）](https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/common/functions.py)
- [O'Reilly Japan「deep-learning-from-scratch」relu.py（Python・公式サンプルコード）](https://github.com/oreilly-japan/deep-learning-from-scratch/blob/master/ch03/relu.py)
