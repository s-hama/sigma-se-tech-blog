## タイトル
MathJax - MathML・LaTeX：導入と数式表示サンプル

## 概要
MathJaxを使い、Webページ上でMathMLやLaTeX形式の数式を表示する方法を整理する。
技術記事では、数式を画像ではなくテキストとして扱えると、拡大表示、検索、修正がしやすくなる。
ここでは、MathJaxの読み込み、MathMLの基本要素、LaTeXによる数式表現をサンプルで確認する。

## この記事で理解できること
- MathJaxをWebページへ読み込む基本。
- MathMLで数式を構造的に表す考え方。
- LaTeX記法で分数、添字、平方根などを表示する方法。
- ブログ記事で数式を書くときの注意点。

## 作業前に確認すること
| 確認項目 | 内容 |
| --- | --- |
| HTMLの基礎 | scriptタグやHTML要素の読み方を確認しておく。 |
| 数式表記 | 分数、指数、添字などの基本的な数式表現を理解しておく。 |
| 表示確認 | ブラウザでHTMLを表示し、MathJaxが読み込まれているか確認できるようにする。 |

## 注意したい点
| 注意したい点 | 確認する観点 |
| --- | --- |
| MathMLとLaTeXの違い | MathMLはHTMLに近い構造、LaTeXは短い記法で数式を書く方法として捉える。 |
| エスケープ漏れ | HTML内では記号の扱いに注意し、ブログの変換処理で壊れない形にする。 |
| 読み込み順序 | MathJaxのscriptが読み込まれないと、数式がそのまま文字として表示される。 |

## 実施内容
### MathJaxの導入
導入はJavaScriptの読み込みのみ。

- MathJax.jsを読み込む<br>
  ```html
  <script type="text/javascript" async src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.4/MathJax.js?config=TeX-MML-AM_CHTML"></script>
  ```
  URLパラメータのconfigを**TeX-MML-AM_CHTML**と指定することにより、**MathML**、**LaTeX**、**AsciiMath**すべて認識できる状態となる。<br>
  LaTeXのみ認識するのであれば、**TeX-AMS_CHTML**とするなど色々な設定方法があるため、詳細については下記ドキュメントを参考。<br>
  ※ https://docs.mathjax.org/en/latest/config-files.html<br>

### MathMLの要素
基本的には`<math>`内に、**mnタグ**や**moタグ**などのMathML要素を記述する形になる。<br>

- MathMLの全要素<br>
※ より詳細なルールや使用方法は下記を参考。<br>
https://developer.mozilla.org/ja/docs/Web/MathML/Element/math

  - `<math>`：トップレベル要素
  - `<maction>`：部分式にバインドされたアクション
  - `<maligngroup>`：揃えグループ
  - `<malignmark>`：揃えポイント
  - `<menclose>`：囲みコンテンツ
  - `<merror>`：囲み構文エラーメッセージ
  - `<mfenced>`：括弧
  - `<mfrac>`：分数
  - `<mglyph>`：非標準記号の表示
  - `<mi>`：識別子
  - `<mlabeledtr>`：表または行列のラベル付き行
  - `<mlongdiv>`：割り算の筆算表記
  - `<mmultiscripts>`：前置字とテンソル添字
  - `<mn>`：数字
  - `<mo>`：演算子
  - `<mover>`：真上付き
  - `<mpadded>`：コンテンツまわりの空白
  - `<mphantom>`：予約スペースを持つ不可視コンテンツ
  - `<mroot>`：累乗根
  - `<mrow>`：グループ化された部分式
  - `<ms>`：文字列リテラル
  - `<mscarries>`：carries などのアノテーション
  - `<mscarry>`：Single carry, <mscarries> の子要素
  - `<msgroup>`：<mstack> および <mlongdiv> 要素のグループ化された行
  - `<msline>`：<mstack> 要素内の水平線
  - `<mspace>`：空白
  - `<msqrt>`：平方根
  - `<msrow>`：<mstack> 要素の行
  - `<mstack>`：スタック揃え
  - `<mstyle>`：書式変更
  - `<msub>`：下付き
  - `<msup>`：上付き
  - `<msubsup>`：下付き上付きの組
  - `<mtable>`：表または行列
  - `<mtd>`：表または行列のセル
  - `<mtext>`：テキスト
  - `<mtr>`：表または行列の列
  - `<munder>`：真下付き
  - `<munderover>`：真下付きと真上付きの組
  - `<semantics>`：セマンティックアノテーション用のコンテナ
  - `<annotation>`：Data アノテーション
  - `<annotation-xml>`：XML アノテーション

### MathMLの表示サンプル
以下の表示サンプルで確認する。
- 黄金比
  - 表示
    <div style="margin-left: 1rem; font-size: 1.8em; margin-top: 0.25em;">
      <math>
        <mfrac>
          <mrow>
            <mn>1</mn><mo>+</mo><msqrt><mn>5</mn></msqrt>
          </mrow>
          <mn>2</mn>
        </mfrac>
      </math>
    </div><br>
  - マークアップ
    ```xml
    <math>
      <mfrac>
        <mrow>
          <mn>1</mn><mo>+</mo><msqrt><mn>5</mn></msqrt>
        </mrow>
        <mn>2</mn>
      </mfrac>
    </math>
    ```

- 極限値
  - 表示
    <div style="display: flex; overflow-x: auto; white-space: nowrap; height: 4.5rem; margin-left: 1rem; font-size: 1.5em; margin-top: 0.25em;">
      <math>
        <munder>
          <mi>lim</mi>
          <mrow>
            <mi>x</mi>
            <mo>→</mo>
            <mn>0</mn>
          </mrow>
        </munder>
        <mfrac>
          <mrow>
            <mi>sin</mi>
            <mo>⁡</mo>
            <mi>x</mi>
          </mrow>
          <mi>x</mi>
        </mfrac>
        <mo>=</mo>
        <mn>1</mn>
      </math>
    </div><br>
  - マークアップ
    ```xml
    <math>
      <munder>
        <mi>lim</mi>
        <mrow>
          <mi>x</mi>
          <mo>→</mo>
          <mn>0</mn>
        </mrow>
      </munder>
      <mfrac>
        <mrow>
          <mi>sin</mi>
          <mo>⁡</mo>
          <mi>x</mi>
        </mrow>
        <mi>x</mi>
      </mfrac>
      <mo>=</mo>
      <mn>1</mn>
    </math>
    ```

- 逆行列
  - 表示
    <div style="display: flex; overflow-x: auto; white-space: nowrap; height: 10rem; margin-left: 1rem; font-size: 1.2em; margin-top: 0.25em;">
      <math>
        <mtable>
          <mtr>
            <mtd>
              <mi>A</mi>
              <mo>=</mo>
              <mfenced>
                <mtable>
                  <mtr>
                    <mtd>
                      <mi>a</mi>
                    </mtd>
                    <mtd>
                      <mi>b</mi>
                    </mtd>
                  </mtr>
                  <mtr>
                    <mtd>
                      <mi>c</mi>
                    </mtd>
                    <mtd>
                      <mi>d</mi>
                    </mtd>
                  </mtr>
                </mtable>
              </mfenced>
            </mtd>
          </mtr>
          <mtr>
            <mtd>
              <msup>
                <mi>A</mi>
                <mrow>
                  <mo>-</mo>
                  <mn>1</mn>
                </mrow>
              </msup>
              <mo>=</mo>
              <mfrac>
                <mn>1</mn>
                <mrow>
                  <mi>a</mi>
                  <mo></mo>
                  <mi>d</mi>
                  <mo>-</mo>
                  <mi>b</mi>
                  <mo></mo>
                  <mi>c</mi>
                </mrow>
              </mfrac>
              <mo></mo>
              <mfenced>
                <mtable>
                  <mtr>
                    <mtd>
                      <mi>d</mi>
                    </mtd>
                    <mtd>
                      <mo>-</mo>
                      <mi>b</mi>
                    </mtd>
                  </mtr>
                  <mtr>
                    <mtd>
                      <mo>-</mo>
                      <mi>c</mi>
                    </mtd>
                    <mtd>
                      <mi>a</mi>
                    </mtd>
                  </mtr>
                </mtable>
              </mfenced>
            </mtd>
          </mtr>
        </mtable>
      </math>
    </div><br>
  - マークアップ
    ```xml
    <math>
      <mtable>
        <mtr>
          <mtd>
            <mi>A</mi>
            <mo>=</mo>
            <mfenced>
              <mtable>
                <mtr>
                  <mtd>
                    <mi>a</mi>
                  </mtd>
                  <mtd>
                    <mi>b</mi>
                  </mtd>
                </mtr>
                <mtr>
                  <mtd>
                    <mi>c</mi>
                  </mtd>
                  <mtd>
                    <mi>d</mi>
                  </mtd>
                </mtr>
              </mtable>
            </mfenced>
          </mtd>
        </mtr>
        <mtr>
          <mtd>
            <msup>
              <mi>A</mi>
              <mrow>
                <mo>-</mo>
                <mn>1</mn>
              </mrow>
            </msup>
            <mo>=</mo>
            <mfrac>
              <mn>1</mn>
              <mrow>
                <mi>a</mi>
                <mo></mo>
                <mi>d</mi>
                <mo>-</mo>
                <mi>b</mi>
                <mo></mo>
                <mi>c</mi>
              </mrow>
            </mfrac>
            <mo></mo>
            <mfenced>
              <mtable>
                <mtr>
                  <mtd>
                    <mi>d</mi>
                  </mtd>
                  <mtd>
                    <mo>-</mo>
                    <mi>b</mi>
                  </mtd>
                </mtr>
                <mtr>
                  <mtd>
                    <mo>-</mo>
                    <mi>c</mi>
                  </mtd>
                  <mtd>
                    <mi>a</mi>
                  </mtd>
                </mtr>
              </mtable>
            </mfenced>
          </mtd>
        </mtr>
      </mtable>
    </math>
    ```

### LaTeXの表示サンプル
  続いてLaTeX。<br>
  以下の表示サンプルで確認する。
- 二次方程式の解
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     x = \frac{-b\pm\sqrt{b^{2}-4ac}}{2a}
    \]
    </div>
  - マークアップ
    ```bash
    \[
     x = \frac{-b\pm\sqrt{b^{2}-4ac}}{2a}
    \]
    ```

- 絶対値の定義
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     |x| = \begin{cases}
       x & \text{\(x\ge0\) のとき} \\
       -x & \text{\(x<0\) のとき}
     \end{cases}
    \]
    </div>
  - マークアップ
    ```bash
    \[
     |x| = \begin{cases}
       x & \text{\(x\ge0\) のとき} \\
       -x & \text{\(x<0\) のとき}
     \end{cases}
    \end{cases}
    \]
    ```

- \(f(x)\)の導関数
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     f’(x) = \lim_{\Delta x \to 0} \frac{ f(x+\Delta x) - f(x) }{\Delta x}
    \]
    </div>
  - マークアップ
    ```bash
    \[
     f’(x) = \lim_{\Delta x \to 0} \frac{ f(x+\Delta x) - f(x) }{\Delta x}
    \]
    ```

- ガウス積分
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     f’(x) = \lim_{\Delta x \to 0} \frac{ f(x+\Delta x) - f(x) }{\Delta x}
    \]
    </div>
  - マークアップ
    ```bash
    \[
     \int_{-\infty}^{\infty} e^{-x^{2}} \, dx = \sqrt{\pi}
    \]
    ```

- n × n行列
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
    A = \begin{pmatrix}
    a_{11} & a_{12} & \ldots & a_{1n} \\
    a_{21} & a_{22} & \ldots & a_{2n} \\
    \vdots & \vdots & \ddots & \vdots \\
    a_{n1} & a_{n2} & \ldots & a_{nn}
    \end{pmatrix}
    \]
    </div>
  - マークアップ
    ```bash
    \[
     A = \begin{pmatrix}
     a_{11} & a_{12} & \ldots & a_{1n} \\
     a_{21} & a_{22} & \ldots & a_{2n} \\
     \vdots & \vdots & \ddots & \vdots \\
     a_{n1} & a_{n2} & \ldots & a_{nn}
     \end{pmatrix}
    \]
    ```

## 実務とのつながり
- 技術ブログでの数式表現<br>
    機械学習、暗号技術、情報処理試験の記事では、数式を読みやすく表示できると理解しやすくなる。
- 保守しやすい記事作成<br>
    画像化した数式より、テキストで書いた数式の方が後から修正しやすい。

## 要約
- MathJaxを使うと、Webページ上でMathMLやLaTeXの数式を表示できる。
- MathMLは構造的、LaTeXは短く書きやすい表現として使い分ける。
- 数式をテキストとして管理すると、技術記事の保守性が上がる。
