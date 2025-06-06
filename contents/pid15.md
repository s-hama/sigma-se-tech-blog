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
