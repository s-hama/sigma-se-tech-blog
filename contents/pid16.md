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

  下記の入力値が2つあるパーセプトロン\\(（A）\\)に対して、ORゲートを満たす、パラメータ \\((b, w_{1}, w_{2})\\) \\(= (-0.5, 1.0, 1.0)\\) を与えた場合を例にその根拠を説明する。

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

  パラメータ \\((b, w_{1}, w_{2})\\) \\(= (-0.5, 1.0, 1.0)\\) を指定すると

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

- **4.** XORゲートの真理値表<br>
  上記 **1.** ～ **3.** の単純パーセプトロンを左辺 \\(s_{1}\\), \\(s_{2}\\), \\(y\\) で結合すると、下記 **XORゲートの真理値表**として表現することができる。
  <table class="table" style="width: 100%; margin-bottom: 2em;">
    <thead>
      <tr>
        <th scope="col">\(x_{1}\)</th>
        <th scope="col">\(x_{2}\)</th>
        <th scope="col">\(s_{1}\)</th>
        <th scope="col">\(s_{2}\)</th>
        <th scope="col">\(y\)</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>入力値1</td><td>入力値2</td><td>1. の出力</td><td>2. の出力</td><td>3. の出力</td></tr>
      <tr><td>0</td><td>0</td><td>1</td><td>0</td><td>0</td></tr>
      <tr><td>1</td><td>0</td><td>1</td><td>1</td><td>1</td></tr>
      <tr><td>0</td><td>1</td><td>1</td><td>1</td><td>1</td></tr>
      <tr><td>1</td><td>1</td><td>0</td><td>1</td><td>0</td></tr>
    </tbody>
  </table>

  - 補足
    - 入力値1（\\(x_{1}\\)）、入力値2（\\(x_{2}\\)）のNANDゲートが **1. の出力**（\\(s_{1}\\)）となる。
    - 入力値1（\\(x_{1}\\)）、入力値2（\\(x_{2}\\)）のORゲートが **2. の出力**（\\(s_{2}\\)）となる。
    - 1.の出力（\\(s_{1}\\)）、2.の出力（\\(s_{2}\\)）のANDゲートが **3. の出力**（\\(y\\)）となる。

### 多層パーセプトロンの実装サンプル
最後に実装サンプル。

- AND、NAND、ORゲートを定義<br>
[前の記事 > 単純パーセプトロンの実装サンプル](https://sigma-se.com/detail/15/#:~:text=%E3%81%A8%E8%A1%A8%E7%8F%BE%E3%81%A7%E3%81%8D%E3%82%8B%E3%80%82-,%E5%8D%98%E7%B4%94%E3%83%91%E3%83%BC%E3%82%BB%E3%83%97%E3%83%88%E3%83%AD%E3%83%B3%E3%81%AE%E5%AE%9F%E8%A3%85%E3%82%B5%E3%83%B3%E3%83%97%E3%83%AB) で触れている**ANDゲート**に加え、パラメータ \\(w_{1}\\)（重み1）, \\(w_{2}\\)（重み2）,  \\(b\\)（バイアス）を**NANDゲート**、**ORゲート**の真理値表を満たすように変え、以下のように定義する。
  ```bash
  $ python
  >>> import numpy as np
  >>> def AND(x1, x2):    # （＊1）ANDゲートの定義
  ...     x = np.array([x1, x2])    # 入力
  ...     w = np.array([0.5, 0.5])    # 重み
  ...     b = -0.7    # バイアス
  ...     tmp = np.sum(w*x) + b
  ...     if tmp <= 0:
  ...         return 0
  ...     else:
  ...         return 1
  ...
  >>> def NAND(x1, x2):    # （＊2）NANDゲートの定義
  ...     x = np.array([x1, x2])    # 入力
  ...     w = np.array([-0.5, -0.5])    # 重み
  ...     b = 0.7    # バイアス
  ...     tmp = np.sum(w*x) + b
  ...     if tmp <= 0:
  ...         return 0
  ...     else:
  ...         return 1
  ...
  >>> def OR(x1, x2):    # （＊3）ORゲートの定義
  ...     x = np.array([x1, x2])    # 入力
  ...     w = np.array([0.5, 0.5])    # 重み
  ...     b = -0.2    # バイアス
  ...     tmp = np.sum(w*x) + b
  ...     if tmp <= 0:
  ...         return 0
  ...     else:
  ...         return 1
  ...
  ```
  あとは、上記（＊1）～（＊3）それぞれの引数と戻り値を上記**XORゲートの真理値表**に合わせて実装するだけ。

- XORゲートの実装サンプル
  ```bash
  >>> def XOR(x1, x2):    # XORゲートの定義
  ...     s1 = NAND(x1, x2)
  ...     s2 = OR(x1, x2)
  ...     y = AND(s1, s2)
  ...     return y
  ...
  >>> XOR(0, 0)    # （＊4） 0 を出力
  0
  >>> XOR(1, 0)    # （＊5） 1 を出力
  1
  >>> XOR(0, 1)    # （＊6） 1 を出力
  1
  >>> XOR(1, 1)    # （＊7） 0 を出力
  0
  ```
  上記（＊4）～（＊7）の通り、**XORゲート**が実装できた。<br>
  （**XORゲートの真理値表**の \\(y\\) が出力できている。）

### 参考文献
- 斎藤 康毅（2018）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
