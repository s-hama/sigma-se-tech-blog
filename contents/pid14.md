## タイトル
MathJax - MathML・LaTeX：導入と数式表示サンプル

## 概要
MathJaxを使い、Webページ上でMathMLやLaTeX形式の数式を表示する方法を整理する。
技術記事では、数式を画像ではなくテキストとして扱えると、拡大表示、検索、修正がしやすくなる。
ここでは、MathJaxの読み込み、MathMLの基本要素、LaTeXによる数式表現をサンプルで確認する。

## この記事の構成
- [MathJaxの導入](#mathjaxの導入)<br>
  MathJaxの導入の手順と確認ポイントを整理。
- [MathMLの要素](#mathmlの要素)<br>
  MathMLを構成する主な要素と、数式を構造化して記述する方法を整理。
- [MathMLの表示サンプル](#mathmlの表示サンプル)<br>
  MathMLの表示サンプルをコードや具体例で確認。
- [LaTeXの表示サンプル](#latexの表示サンプル)<br>
  LaTeXの表示サンプルをコードや具体例で確認。

## 実施内容
### MathJaxの導入
MathJaxはCDNからJavaScriptを読み込むだけで導入できる。

- MathJax 4.xを読み込む<br>
  TeXとMathMLを入力として受け取り、CommonHTMLで表示する公式ドキュメントの構成例は次のとおり。
  ```html
  <script defer src="https://cdn.jsdelivr.net/npm/mathjax@4/tex-mml-chtml.js"></script>
  ```
  `mathjax@4`は最新の4.x系を取得する指定である。<br>再現性を重視する環境では`mathjax@4.0.0`のように完全なバージョンを固定。TeXだけを処理する場合は`tex-chtml.js`など、用途に合う小さなコンポーネントも選べる。

### MathMLの要素
MathMLでは、トップレベルの`<math>`内に`<mn>`や`<mo>`などの要素を組み合わせ、数式の構造を記述する。

- このページで使う主なMathML要素
  - `<math>`：トップレベル要素。
  - `<mrow>`：複数の要素を一つの部分式としてまとめる。
  - `<mi>`：変数名や関数名などの識別子。
  - `<mn>`：数値。
  - `<mo>`：演算子や括弧。
  - `<mfrac>`：分数。
  - `<msqrt>`：平方根。
  - `<msup>`：上付き文字。
  - `<munder>`：式の真下に付ける要素。
  - `<mtable>`、`<mtr>`、`<mtd>`：表や行列、その行、セル。

※ MathML仕様には`<mfenced>`もあるが、ブラウザ実装を重視したMathML Coreには含まれない。<br>互換性を考え、このページでは`<mrow>`と括弧を表す`<mo>`を明示的に使用する。

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
  - \(2 \times 2\)行列の逆行列を表示。ただし、逆行列が存在する条件は\(ad-bc \neq 0\)である。
  - 表示
    <div style="display: flex; overflow-x: auto; white-space: nowrap; height: 10rem; margin-left: 1rem; font-size: 1.2em; margin-top: 0.25em;">
      <math>
        <mtable>
          <mtr>
            <mtd>
              <mi>A</mi>
              <mo>=</mo>
              <mrow>
                <mo>(</mo>
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
                <mo>)</mo>
              </mrow>
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
                  <mo>⁢</mo>
                  <mi>d</mi>
                  <mo>-</mo>
                  <mi>b</mi>
                  <mo>⁢</mo>
                  <mi>c</mi>
                </mrow>
              </mfrac>
              <mo>⁢</mo>
              <mrow>
                <mo>(</mo>
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
                <mo>)</mo>
              </mrow>
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
            <mrow>
              <mo>(</mo>
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
              <mo>)</mo>
            </mrow>
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
                <mo>⁢</mo>
                <mi>d</mi>
                <mo>-</mo>
                <mi>b</mi>
                <mo>⁢</mo>
                <mi>c</mi>
              </mrow>
            </mfrac>
            <mo>⁢</mo>
            <mrow>
              <mo>(</mo>
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
              <mo>)</mo>
            </mrow>
          </mtd>
        </mtr>
      </mtable>
    </math>
    ```

### LaTeXの表示サンプル
MathJaxのTeX入力では、分数や行列をMathMLより短い記述で表せる。<br>ここでは、数式を`\[`と`\]`で囲んだ別行表示の例を確認する。

- 二次方程式の解
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     x = \frac{-b\pm\sqrt{b^{2}-4ac}}{2a}
    \]
    </div>
  - マークアップ
    ```latex
    \[
     x = \frac{-b\pm\sqrt{b^{2}-4ac}}{2a}
    \]
    ```

- 絶対値の定義
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     |x| = \begin{cases}
       x & (x\ge0\text{ のとき}) \\
       -x & (x<0\text{ のとき})
     \end{cases}
    \]
    </div>
  - マークアップ
    ```latex
    \[
     |x| = \begin{cases}
       x & (x\ge0\text{ のとき}) \\
       -x & (x<0\text{ のとき})
     \end{cases}
    \]
    ```

- \(f(x)\)の導関数
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     f'(x) = \lim_{\Delta x \to 0} \frac{f(x+\Delta x) - f(x)}{\Delta x}
    \]
    </div>
  - マークアップ
    ```latex
    \[
     f'(x) = \lim_{\Delta x \to 0} \frac{f(x+\Delta x) - f(x)}{\Delta x}
    \]
    ```

- ガウス積分
  - 表示 
    <div style="display: flex; margin-left: 1rem; font-size: 1.2em; margin-top: -1em; overflow-x: auto; white-space: nowrap;">
    \[
     \int_{-\infty}^{\infty} e^{-x^{2}} \, dx = \sqrt{\pi}
    \]
    </div>
  - マークアップ
    ```latex
    \[
     \int_{-\infty}^{\infty} e^{-x^{2}} \, dx = \sqrt{\pi}
    \]
    ```

- \(n \times n\)行列
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
    ```latex
    \[
     A = \begin{pmatrix}
     a_{11} & a_{12} & \ldots & a_{1n} \\
     a_{21} & a_{22} & \ldots & a_{2n} \\
     \vdots & \vdots & \ddots & \vdots \\
     a_{n1} & a_{n2} & \ldots & a_{nn}
     \end{pmatrix}
    \]
    ```

## まとめ
- MathJaxを使うと、Webページ上でMathMLやLaTeXの数式を表示できる。
- MathMLはHTMLに近い構造で数式を表し、LaTeXは短い記法で数式を書けるため、用途に応じて使い分ける。
- MathJaxのscriptが正しく読み込まれない場合、数式は変換されず文字列のまま表示される。
- HTMLの記号やブログの変換処理によるエスケープ漏れに注意し、数式を壊れないテキストとして管理すると記事を保守しやすい。

### 参考文献
- [MDN Web Docs「MathML要素リファレンス」（日本語・要素別解説）](https://developer.mozilla.org/ja/docs/Web/MathML/Reference/Element)
- [MathJax Documentation, Getting Started with MathJax Components（英語・導入公式手順）](https://docs.mathjax.org/en/stable/web/start.html)
- [MathJax Documentation, Input Components（英語・入力形式の公式仕様）](https://docs.mathjax.org/en/stable/web/components/input.html)
- [W3C, MathML Core（英語・Web標準仕様原文）](https://www.w3.org/TR/mathml-core/)
