## タイトル
Python - AI : 多層パーセプトロンの概念と実装サンプル

## 目的
この記事では、多層パーセプトロンの概念と簡単な実装サンプルについて記載する。

## 概念の説明と実装サンプル
### 単純パーセプトロンの限界
[前の記事](https://sigma-se.com/detail/15/) で単純パーセプトロンを**AND、NAND、OR の論理回路**で実装できることを説明したが、**排他的論理和**と呼ばれる下記**XORゲート**になると、以下で示す**非線形**でしか \\(0\\) と \\(1\\) の領域を分けられない。<br>
（単純パーセプトロンは、線形（直線）でしか \\(0\\) と \\(1\\) の領域を分けられない。）

- **XORゲート**の真理値表
  <table class="table" style="width: 50%; margin-bottom: 2em;">
    <thead>
      <tr>
        <th scope="col">\(x_{1}\)</th>
        <th scope="col">\(x_{2}\)</th>
        <th scope="col">\(y\)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>0</td><td>0</td><td>0</td></tr>
      <tr><td>1</td><td>0</td><td>1</td></tr>
      <tr><td>0</td><td>1</td><td>1</td></tr>
      <tr><td>1</td><td>1</td><td>0</td></tr>
    </tbody>
  </table>

  下記の入力値が2つあるパーセプトロン\\(（A）\\)に対して、ORゲートを満たす、パラメータ \\((b, w_{1}, w_{2}) = (-0.5, 1.0, 1.0)\\) を与えた場合を例にその根拠を説明する。

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

  パラメータ \\((b, w_{1}, w_{2}) = (-0.5, 1.0, 1.0)\\) を指定すると

  <div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
  \[
  {\small
  y =
  \begin{cases}
  0 \hspace{5pt}\text{if}\hspace{5pt}-0.5 + x_{1} + x_{2} \leqq 0 \\
  1 \hspace{5pt}\text{if}\hspace{5pt}-0.5 + x_{1} + x_{2} > 0
  \end{cases}\hspace{5mm}･･･（B）
  }
  \]
  </div>

  よって、上記\\(（B）\\)の境界線は

  <div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
  \[
  {\small
  -0.5 + x_{1} + x_{2} = 0\hspace{5mm}･･･（C）
  }
  \]
  </div>

  となるため、下記グラフが**境界線**となる。

  ![pid16_1](/static/tblog/img/pid16_1.png)

  そして、グラフ上の4つの点「**△**」は、下記ORゲートの真理値表で \\(y = 0\\) となる <span style="color:red">**△**</span> と \\(y = 1\\) となる <span style="color:blue">**△**</span> を表している。

  <table class="table" style="width: 50%; margin-bottom: 2em;">
    <thead>
      <tr>
        <th scope="col">\(x_{1}\)</th>
        <th scope="col">\(x_{2}\)</th>
        <th scope="col">\(y\)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>0</td><td>0</td><td>0</td></tr>
      <tr><td>1</td><td>0</td><td>1</td></tr>
      <tr><td>0</td><td>1</td><td>1</td></tr>
      <tr><td>1</td><td>1</td><td>1</td></tr>
    </tbody>
  </table>

  このように\\(（B）\\) は、 \\(0\\) と \\(1\\) の領域を**線形**（直線）で分けることができる。
  <br>
  一方、冒頭で触れた**XORゲート**になると、上記**XORゲートの真理値表**の通り、\\((x_{1}, x_{2}) = (1, 1)\\) の時、\\(y=0\\) となるため、
下記グラフの <span style="color:blue">**△**</span> と <span style="color:red">**△**</span> で領域を分けているように、**非線形**でしか分けることができない。

  ![pid16_2](/static/tblog/img/pid16_2.png)

### 多層パーセプトロンの概念
上記で触れたの通り、単純パーセプトロン（入力層と出力層のみの2層）では、XORゲートを表現できないが**多層パーセプトロン**（入力層が多層）だとそれが**可能**になる。

単純パーセプトロンの説明で触れてきた**AND、NAND、ORゲート**を下記 **1.** ～ **3.** で組み合わせれば、**4. XORゲートの真理値表**の通り、多層パーセプトロンを表現できる。

- **1.** NANDゲート
  <div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
  \[
  {\small
  s_{1} =
  \begin{cases}
  0 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} \leqq 0 \\
  1 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} > 0
  \end{cases}
  }
  \]
  </div>

- **2.** ORゲート
  <div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
  \[
  {\small
  s_{2} =
  \begin{cases}
  0 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} \leqq 0 \\
  1 \hspace{5pt}\text{if}\hspace{5pt}b + x_{1}w_{1} + x_{2}w_{2} > 0
  \end{cases}
  }
  \]
  </div>

- **3.** ANDゲート
  <div style="display: flex; margin-left: 1rem; font-size: 1.3em; margin-top: -0.75em; overflow-x: auto; white-space: nowrap;">
  \[
  {\small
  y =
  \begin{cases}
  0 \hspace{5pt}\text{if}\hspace{5pt}b + s_{1}w_{1} + s_{2}w_{2} \leqq 0 \\
  1 \hspace{5pt}\text{if}\hspace{5pt}b + s_{1}w_{1} + s_{2}w_{2} > 0
  \end{cases}
  }
  \]
  </div>
