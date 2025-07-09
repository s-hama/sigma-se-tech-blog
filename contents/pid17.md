## タイトル
Python - AI : ニューラルネットワークの活性化関数と実装サンプル

## 目的
この記事では、ニューラルネットワークの活性化関数と実装サンプルについて記載する。

※ 活性化関数は、パーセプトロンの原理を基にしてニューラルネットワークを理解するための架け橋的な役割を持つ。

## 概念の説明と実装サンプル
### パーセプトロンと活性化関数
**活性化関数**（activation function）は、**伝達関数**（transfer function）とも呼ばれ、入力値の**総和を出力に変換する**関数のことを言い、入力値がどのように発火するか（活性化するか・伝達されるか）を決定する役割を持つ。

[前の記事 > 多層パーセプトロンの概念と実装サンプル](https://sigma-se.com/detail/16/) で触れた入力値が2つあるパーセプトロン\\(（A）\\)も活性化関数と言えるが、一般的な活性化関数の表現に書き換えると右辺を \\(a = b + x_{1}w_{1} + x_{2}w_{2} \\) と置き、\\(（B）\\) 、\\(y\\) を \\(h(a)\\) で表現した\\(（C）\\)のように表せる。

<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
y =
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} \leqq 0 \\
1 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} > 0
\end{cases}\hspace{5mm}･･･（A）
}
\]
</div>

\\(a = b + x_{1}w_{1} + x_{2}w_{2} \\) と置き

<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
y =
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}a \leqq 0 \\
1 \hspace{5pt}\text{if}\hspace{5pt}a > 0
\end{cases}\hspace{5mm}･･･（B）
}
\]
</div>

\\(y\\) = \\(h(a)\\) とすると

<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
y = h(b + x_{1}w_{1} + x_{2}w_{2})
}
\]
</div>
<div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
{\small
h(a) =
\begin{cases}
0 \hspace{5pt}\text{if}\hspace{5pt}a \leqq 0 \\
1 \hspace{5pt}\text{if}\hspace{5pt}a > 0
\end{cases}\hspace{5mm}･･･（C）
}
\]
</div>

となり、**入力値の総和**を \\(h(a)\\) によって変換し、出力値である \\(y\\) となることを表わしている。

※ \\(（C）\\) のイメージ
<div style="text-align: center;">
　<img src="/static/tblog/img/pid17_1.svg" alt="pid17_1" style="width: 80%; height: auto; margin-top: -1.25rem;" />
</div>

上記の \\(a\\)、\\(h(x)\\)、\\(y\\) の 〇 を **ニューロン**（またはノード）と呼ぶ。

上記の通り、\\(（C）\\)で表される活性化関数は、バイアスを境に出力が切り替わる関数となっているが、このような関数を**ステップ関数**または、**階段関数**という。

従ってパーセプトロンは、活性化関数に分類される**ステップ関数**を用いて表現されてる。

この活性化関数は、**ステップ関数**ではなく、次項で触れる**シグモイト関数**を用いることで、自動学習が可能なニューラルネットワークを表現できるようになる。

※ 単純/多層パーセプトロンでは、意図した論理回路が実現するように適切な \\(w\\)（重み）を人力で判断しなければならなかったが、ニューラルネットワークでは、その判断を自動学習できるようになる。
