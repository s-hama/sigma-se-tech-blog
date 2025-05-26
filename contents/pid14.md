## タイトル
MathJax - MathML、LaTeX : 導入と数式表示サンプル

## 目的
この記事では、MathJaxの導入説明とMathML、LaTeXの数式表示サンプルを記載する。

MathJaxは、**MathML**、**LaTeX**、**AsciiMath**で記述された数式をウェブブラウザ上で表示するためのJavaScriptライブラリ。<br>
また、ブラウザ依存せず、如何なる環境下でも動作を保証するクロスブラウザ仕様となる。<br>

※ MathMLの対応ブラウザについては、2018年1月時点で**Firefox**、**Safari**、**iOS Safari**のみ。<br>
より詳細な使用方法は、公式ドキュメントを参考。<br>
MathML3ドキュメント：https://www.w3.org/TR/MathML3/

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
