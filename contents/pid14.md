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

### MathMLの要素
基本`<math>`内に、下記で記載するMathMLの**mnタグ**や**moタグ**など記述する形になる。<br>

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
