## タイトル
Python - Matplotlib：pyplotでグラフを描画する基本操作

## 概要
Matplotlibのpyplotを使い、Pythonでグラフを描画する基本手順を整理する。
数値だけを眺めても傾向はつかみにくいため、折れ線グラフや散布図として可視化することで、変化、分布、外れ値を確認しやすくなる。<br>ここでは、インストール、基本的な描画、複数系列、ラベルや凡例の設定を実行例で確認する。

## この記事で扱うこと
- pyplotを使ったグラフ描画の基本的な流れ。
- x軸、y軸、タイトル、凡例を設定する方法。
- 折れ線グラフや散布図でデータの傾向を見る考え方。
- NumPy配列とMatplotlibを組み合わせる使い方。

## 実施内容
### Matplotlibの環境準備
**Matplotlib**は、折れ線グラフ、散布図、ヒストグラム、画像などを描画できるPythonライブラリで、NumPyと組み合わせて使用する場面も多い。

- Matplotlibのインストール<br>
使用するPython環境を明確にするため、次のようにPython経由でpipを実行する。
  ```bash
  $ python -m pip install matplotlib
  ```
  インストール後は`python -c "import matplotlib; print(matplotlib.__version__)"`で、読み込まれたバージョンを確認できる。以降では`matplotlib.pyplot`の基本操作に絞る。

### Matplotlibの使用方法
- 区間、刻み幅、グラフタイトル、軸ラベルの設定と表示<br>
二次関数**y = x^2**を例に区間、刻み幅、グラフタイトル、軸ラベルを設定してグラフを描画する。<br>`np.arange(0, 20, 0.01)`は、0以上20未満の値を0.01刻みで生成する。
  ```bash
  $ python
   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> x = np.arange(0, 20, 0.01)    # 0以上20未満の範囲を0.01刻みに設定
   >>> y = x**2
   >>> plt.title("y = x^2\n# arange:0, 20, 0.01, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'y = x^2\n# arange:0, 20, 0.01, xlabel:x, ylabel:y')
   >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
   >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
   >>> plt.plot(x,y)    # グラフの描画
     [<matplotlib.lines.Line2D object at 0x7fa0a479eb70>]
   >>> plt.savefig('pid13_1.png')    # 任意の保存先を指定
   >>> plt.close()    # 図を閉じ、次の描画へ状態を持ち越さない
  ```
  - 上記で出力したグラフ「pid13_1.png」
  ![0以上20未満の二次関数y=x^2を描画した折れ線グラフ](/static/tblog/img/pid13_1.png)

- 2つのグラフ、凡例の設定と表示<br>
三角関数**y = sin(x)**と**y = cos(x)**を例に凡例の設定を行い、2つのグラフを表示する。
  ```bash
  $ python
   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> x = np.arange(0, 6, 0.01)    # 0以上6未満の範囲を0.01刻みに設定
   >>> plt.title("y = sin(x), y = cos(x)\n# arange:0, 6, 0.01, xlabel:x, ylabel:y, legend:sin&cos")    # グラフタイトルを設定
   Text(0.5, 1.0, 'y = sin(x), y = cos(x)\n# arange:0, 6, 0.01, xlabel:x, ylabel:y, legend:sin&cos')
   >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
   >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
   >>> y_sin = np.sin(x)
   >>> y_cos = np.cos(x)
   >>> plt.plot(x, y_sin, label="sin")   # グラフの描画 ※実線で描画 ( デフォルト )
     [<matplotlib.lines.Line2D object at 0x7fde03617fd0>]
   >>> plt.plot(x, y_cos, linestyle="--", label="cos")    # グラフの描画 ※破線で描画
     [<matplotlib.lines.Line2D object at 0x7fde03625048>]
   >>> plt.legend()    # 凡例の描画
     <matplotlib.legend.Legend object at 0x7fde03625358>
   >>> plt.savefig('pid13_2.png')    # 任意の保存先を指定
   >>> plt.close()
  ```
  - 上記で出力したグラフ「pid13_2.png」
  ![0以上6未満のsin関数とcos関数を重ねて描画したグラフ](/static/tblog/img/pid13_2.png)

- **imread**を使った画像表示<br>
`matplotlib.image`の`imread`によって画像をNumPy配列として読み込み、`pyplot.imshow`で座標軸上に表示する。<br>
ここでは、透過背景のPythonロゴ画像「pid13_3.png」を読み込み、描画結果を「pid13_4.png」として保存する。<br>読み込んだ配列の`shape`を確認すると、画像の高さ、幅、色チャンネル数も確認できる。

  - 読み込み元の画像「pid13_3.png」
  ![imreadで読み込む透過背景のPythonロゴ画像](/static/tblog/img/pid13_3.png)

  - 「pid13_3.png」を`imread`で読み込み、`imshow`で表示して「pid13_4.png」として保存
    ```bash
    $ python
     >>> import matplotlib.pyplot as plt
     >>> from matplotlib.image import imread
     >>> img = imread('pid13_3.png')    # Pythonロゴ画像を読み込み
     >>> img.shape
     (500, 500, 4)
     >>> plt.imshow(img)    # 画像表示
     <matplotlib.image.AxesImage object at 0x7f4b80106f60>
     >>> plt.title('b_id36_3.png Read with image.imread \n and output as b_id36_4.png in pyplot.imshow')
     >>> plt.savefig('pid13_4.png')
     >>> plt.close()
    ```

  - 上記で出力した画像「pid13_4.png」
  ![Pythonロゴ画像をimshowで描画した結果](/static/tblog/img/pid13_4.png)

  掲載画像のタイトルにある`b_id36_3.png`と`b_id36_4.png`は、旧サイトで使用していたファイル名である。<br>`shape`の値や保存画像の余白は、元画像やMatplotlibのバージョン・設定によって異なる。

- その他のグラフ<br>
上記以外にも`plt.scatter()`による散布図、`plt.hist()`によるヒストグラムなど、さまざまなグラフに対応している。<br>目的に合うグラフを選び、軸名、単位、凡例を付けると、画像だけを見ても意味を判断しやすくなる。

## まとめ
- MatplotlibはPythonでグラフを描く代表的なライブラリ。
- pyplotでは、要素数をそろえたxとyのデータを渡して描画する。要素数が異なると描画エラーになる。
- 軸名や凡例を付けるとグラフの意味が伝わりやすくなり、数値の傾向や異常を判断しやすくなる。
- スクリプトから画面に表示する場合は`plt.show()`、画像として保存する場合は`plt.savefig()`を使用する。
- `imread`で読み込んだ画像はNumPy配列として扱われ、`imshow`で表示できる。

## 参考文献
- 斎藤 康毅（\\(2016\\)）『ゼロから作るDeep Learning ―Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
- [Matplotlib, Getting started（英語・公式導入手順）](https://matplotlib.org/stable/users/getting_started/)
- [Matplotlib, Pyplot tutorial（英語・グラフ描画の公式入門）](https://matplotlib.org/stable/tutorials/pyplot.html)
- [Matplotlib, Image tutorial（英語・画像表示の公式解説）](https://matplotlib.org/stable/tutorials/images.html)
