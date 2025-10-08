## タイトル
Python - AI : 偏微分と勾配の実装サンプル

## 目的
この記事では、偏微分と勾配についての簡単な実装サンプルを記載する。

## 概念の説明と実装サンプル
### 偏微分のおさらい
大まかに言うと偏微分は、**微分対象（変数）が複数になる場合の微分のこと**だが、数式で表現すると少し長くなるため、微分対象が2つ（\\(x_{0} と x_{1}\\)）で、\\(x_{0}\\) で偏微分する場合を例にした以下の定義にとどめる。

<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
 f_{x_{0}}(x_{0}, x_{1}) = ∂_{x_{0}}(x_{0}, x_{1}) = \frac{∂\ (x_{0}, x_{1})}{∂x_{0}}
\]
</div>
<div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
\[
= \lim_{\Delta x_{0} \to 0} \frac{ f(x_{0}+\Delta x_{0}, x_{1}) - f(x_{0}, x_{1}) }{\Delta x_{0}}
\]
</div>

- \\(f_{x_{0}}(x_{0}, x_{1})\\)、\\(∂_{x_{0}}(x_{0}, x_{1})\\)、\\(\frac{∂\ (x_{0}, x_{1})}{∂x_{0}}\\) は、\\(f(x)\\) を \\(x_{0}\\) で偏微分した結果（偏導関数）を表す記号。

- 微分の定義については、前ページを参考のこと
[Python - AI : 損失関数と数値微分（勾配）の実装サンプル > 微分のおさらい](https://sigma-se.com/detail/24/#:~:text=%E3%82%8C%E3%81%A6%E3%81%84%E3%82%8B%E3%80%82-,%E5%BE%AE%E5%88%86%E3%81%AE%E3%81%8A%E3%81%95%E3%82%89%E3%81%84,-%E5%BE%AE%E5%88%86%E3%81%A8%E3%81%AF)
