## タイトル
Python - AI : 活性化関数の実装サンプルまとめ（ステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数）

## 目的
この記事では、活性化関数であるステップ、シグモイド、ReLU、恒等関数、ソフトマックス関数関数の実装サンプルについて記載する。

## 概念の説明と実装サンプル
### ステップ関数
[前の記事 > ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/) で触れた**ステップ関数**で、線形の**活性化関数**であり**階段関数**とも呼ばれる。

- 定義<br>
\\(x\\) が \\(0\\) より大きければ、\\(1\\) を出力し、\\(0\\) 以下であれば \\(0\\) を出力する。
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
 ...    return np.array(x > 0, dtype=np.int)
 ...
```

- グラフ出力
```bash
$ python
 >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5 まで、描画制度を 0.1 刻みに設定
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
 >>> plt.savefig('/var/www/vops/ops/macuos/static/macuos/img/pid18_1.png'))    # グラフの出力
```
![pid18_1](/static/tblog/img/pid18_1.png)

### シグモイド関数
[前の記事 > ニューラルネットワークの活性化関数と実装サンプル](https://sigma-se.com/detail/17/) で触れた**シグモイド関数**で、非線形のの**活性化関数**に分類される。

- 定義<br>
出力値は、\\(x\\) が小さいほど \\(0\\) になく近づき、\\(x\\) が大きいほど \\(1\\) に限りなく近づく。
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
 ...     return 1 / (1 + np.exp(-x))    # 自然対数の低 (e) の -x 乗
 ...
```

- グラフ出力
```bash
$ python
 >>> x = np.arange(-5.0, 5.0, 0.1)    # 区間を-5～5 まで、描画制度を 0.1 刻みに設定
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

