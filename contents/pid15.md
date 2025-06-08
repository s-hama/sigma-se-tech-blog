## タイトル
Python - AI : 単純パーセプトロンの概念と実装サンプル

## 目的
この記事では、単純パーセプトロンの概念と簡単な実装サンプルについて記載する。

## 概念の説明と実装サンプル
### パーセプトロンとは
アメリカの心理学者・計算機科学者であるフランク・ローゼンブラットが1943年に発表された最初の**人工ニューロン**（形式ニューロン）の考え方を基に1957年に考案したアルゴリズム。<br>
※ 形式ニューロンとは、**脳神経細胞**（ニューロン）をモデル化したニューロンのことを指す。

パーセプトロンは、ニューラルネットワークやディープラーニングなどAI分野の礎になっており、これらを理解する上では必要不可欠な概念となる。

パーセプトロンには、**入力層**と**出力層**のみの2層からなる**単純パーセプトロン**と多層からなる**多層パーセプトロン**があるが、ここでは**単純パーセプトロン**についての簡単な実装サンプルについて記載する。

### 単純パーセプトロンの動作原理
**入力信号が2つ**である場合を例にすると、**入力信号** \\(x_{1}\\), \\(x_{2}\\) と**重み** \\(w_{1}\\), \\(w_{2}\\) があった時、それぞれを乗算した**合計** \\(x_{1}w_{1} + x_{2}w_{2}\\) が**閾値** \\(\theta\\) 以下である場合、出力信号 \\(y\\) を \\(0\\) で出力し、閾値 \\(\theta\\) より大きければ、出力信号 \\(y\\) を\\(1\\) で出力する。<br>
※ 閾値 \\(\theta\\) を超え、\\(y = 1\\) となるとき「ニューロンが発火する」と表現することもある。

これが単純パーセプトロンの動作原理で下記は、**上記の説明を数式**で表したもの。
<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
y =
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}x_{1}w_{1} + x_{2}w_{2} \leqq \theta\\
1 \hspace{5pt}\text{if}\hspace{5pt}x_{1}w_{1} + x_{2}w_{2} > \theta
\end{cases}\hspace{5mm}･･･（A）
}
\]
</div>

そして、上記\\(（A）\\)の**入力信号**を \\(n\\) 個とし、一般化すると
<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
y =
{\small
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}x_{1}w_{1} + … +  x_{n}w_{n}\leqq \theta\\
1 \hspace{5pt}\text{if}\hspace{5pt}x_{1}w_{1} + … +  x_{n}w_{n} > \theta
\end{cases}\hspace{5mm}･･･（B）
}
\]
</div>

さらにまとめて
<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
y =
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}\sum_{i=0}^{n} x_{i}w_{i} \leqq \theta\\
1 \hspace{5pt}\text{if}\hspace{5pt}\sum_{i=0}^{n} x_{i}w_{i} > \theta
\end{cases}\hspace{5mm}･･･（C）
}
\]
</div>

となり上記\\(（C）\\)のように表すことができる。

### 単純パーセプトロンを論理回路表現
上記数式\\(（A）\\)の**入力信号が2つある単純パーセプトロン**をANDゲート、NANDゲート、ORゲートで表現し、Pythonの実装サンプルを用いてそれぞれ説明する。

- **1. ANDゲート**の単純パーセプトロンサンプル<br>
  - ANDゲート真理値表
    <table class="table" style="width: 50%;">
      <thead>
        <tr>
          <th scope="col">\(x_{1}\)</th>
          <th scope="col">\(x_{2}\)</th>
          <th scope="col">\(y\)</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>0</td><td>0</td><td>0</td></tr>
        <tr><td>1</td><td>0</td><td>0</td></tr>
        <tr><td>0</td><td>1</td><td>0</td></tr>
        <tr><td>1</td><td>1</td><td>1</td></tr>
      </tbody>
    </table>
  - Pyhonサンプル<br>
  上記のANDゲートを満たすパラメータとなるように \\(w_{1}, w_{2}, \theta\\) を \\((w_{1}, w_{2}, \theta) = (0.5, 0.5, 0.9)\\) と置いて、Pyhonで表現してみる。
    ```bash
    $ python
    >>> def AND(x1, x2):
    ...     w1, w2, theta = 0.5, 0.5, 0.9
    ...     y = x1*w1 + x2*w2
    ...     if y <= theta:
    ...         return 0
    ...     elif y > theta:
    ...         return 1
    ...
    >>> AND(0, 0)    # ANDゲートのパラメータ x1 = 0, x2 = 0 ⇒ y = 0
    0
    >>> AND(1, 0)    # ANDゲートのパラメータ x1 = 1, x2 = 0 ⇒ y = 0
    0
    >>> AND(0, 1)    # ANDゲートのパラメータ x1 = 0, x2 = 1 ⇒ y = 0
    0
    >>> AND(1, 1)    # ANDゲートのパラメータ x1 = 1, x2 = 1 ⇒ y = 1
    1
    >>>
    ```

- **2. NANDゲート**の単純パーセプトロンサンプル
  - NANDゲート真理値表
    <table class="table" style="width: 50%;">
      <thead>
        <tr>
          <th scope="col">\(x_{1}\)</th>
          <th scope="col">\(x_{2}\)</th>
          <th scope="col">\(y\)</th>
        </tr>
      </thead>
      <tbody>
        <tr><td>0</td><td>0</td><td>1</td></tr>
        <tr><td>1</td><td>0</td><td>1</td></tr>
        <tr><td>0</td><td>1</td><td>1</td></tr>
        <tr><td>1</td><td>1</td><td>0</td></tr>
      </tbody>
    </table>
  - Pyhonサンプル<br>
  上記 **1.** と同様に上記のNANDゲートを満たすパラメータ \\(w_{1}, w_{2}, \theta\\) を \\((w_{1}, w_{2}, \theta) = (-0.5, -0.5, -0.9)\\) と置いて、Pyhonで表現したもの。
    ```bash
    $ python
    >>> def NAND(x1, x2):
    ...     w1, w2, theta = -0.5, -0.5, -0.9
    ...     y = x1*w1 + x2*w2
    ...     if y <= theta:
    ...         return 0
    ...     elif y > theta:
    ...         return 1
    ...
    >>> NAND(0, 0)    # NANDゲートのパラメータ x1 = 0, x2 = 0 ⇒ y = 1
    1
    >>> NAND(1, 0)    # NANDゲートのパラメータ x1 = 1, x2 = 0 ⇒ y = 1
    1
    >>> NAND(0, 1)    # NANDゲートのパラメータ x1 = 0, x2 = 1 ⇒ y = 1
    1
    >>> NAND(1, 1)    # NANDゲートのパラメータ x1 = 1, x2 = 1 ⇒ y = 0
    0
    >>>
    ```
