## タイトル
Python - Matplotlib : matplotlib.pyplotの使用方法

## 目的
この記事では、pyplotの使用方法について説明する。

## 実施内容
### Matplotlibの環境準備
**Matplotlib**は、グラフ描画のライブラリでNumPyやScipyと組み合わせて使用するケースが多い。

- NumPyインストール<br>
インストールは、pipで`install matplotlib`を実行する。
  ```bash
  $ pip install matplotlib
   Collecting matplotlib
     Downloading https://files.pythonhosted.org/packages/71/07/16d781df15be30df4acfd536c479268f1208b2dfbc91e9ca5d92c9caf673/matplotlib-3.0.2-cp36-cp36m-manylinux1_x86_64.whl (12.9MB)
       100% |################################| 12.9MB 1.7MB/s
   Collecting python-dateutil>=2.1 (from matplotlib)
     Downloading https://files.pythonhosted.org/packages/74/68/d87d9b36af36f44254a8d512cbfc48369103a3b9e474be9bdfe536abfc45/python_dateutil-2.7.5-py2.py3-none-any.whl (225kB)
       100% |################################| 235kB 10.3MB/s
   Collecting cycler>=0.10 (from matplotlib)
     Downloading https://files.pythonhosted.org/packages/f7/d2/e07d3ebb2bd7af696440ce7e754c59dd546ffe1bbe732c8ab68b9c834e61/cycler-0.10.0-py2.py3-none-any.whl
   Collecting pyparsing!=2.0.4,!=2.1.2,!=2.1.6,>=2.0.1 (from matplotlib)
     Downloading https://files.pythonhosted.org/packages/71/e8/6777f6624681c8b9701a8a0a5654f3eb56919a01a78e12bf3c73f5a3c714/pyparsing-2.3.0-py2.py3-none-any.whl (59kB)
       100% |################################| 61kB 13.5MB/s
   Collecting kiwisolver>=1.0.1 (from matplotlib)
     Downloading https://files.pythonhosted.org/packages/69/a7/88719d132b18300b4369fbffa741841cfd36d1e637e1990f27929945b538/kiwisolver-1.0.1-cp36-cp36m-manylinux1_x86_64.whl (949kB)
       100% |################################| 952kB 8.0MB/s
   Requirement already satisfied: numpy>=1.10.0 in /var/www/vops/lib/python3.6/site-packages (from matplotlib) (1.15.4)
   Collecting six>=1.5 (from python-dateutil>=2.1->matplotlib)
     Downloading https://files.pythonhosted.org/packages/67/4b/141a581104b1f6397bfa78ac9d43d8ad29a7ca43ea90a2d863fe3056e86a/six-1.11.0-py2.py3-none-any.whl
   Requirement already satisfied: setuptools in /var/www/vops/lib/python3.6/site-packages (from kiwisolver>=1.0.1->matplotlib) (40.5.0)
   Installing collected packages: six, python-dateutil, cycler, pyparsing, kiwisolver, matplotlib
   Successfully installed cycler-0.10.0 kiwisolver-1.0.1 matplotlib-3.0.2 pyparsing-2.3.0 python-dateutil-2.7.5 six-1.11.0
  ```
  ※ 以降でmatplotlib.pyplotの使用方法について基本的な部分しか触れないため、詳細な使用方法については、下記チュートリアルで確認すること。<br>
  Matplotlibチュートリアル：https://matplotlib.org/tutorials/index.html<br>

### Matplotlibの使用方法
- 区間、描画精度、グラフタイトル、軸ラベルの設定と表示<br>
二次関数**y = x^2**を例に区間、描画精度、グラフタイトル、軸ラベルの設定を行いグラフ表示する。
  ```bash
  $ python
   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> x = np.arange(0, 20, 0.01)    # 区間を0～20 まで、描画制度を 0.01 刻みに設定
   >>> y = x**2
   >>> plt.title("y = x^2\n# arange:0, 20, 0.01, xlabel:x, ylabel:y")    # グラフタイトルを設定
     Text(0.5, 1.0, 'y = x^2\n# arange:0, 20, 0.01, xlabel:x, ylabel:y')
   >>> plt.xlabel("x")    # x軸のラベルを設定
     Text(0.5, 0, 'x')
   >>> plt.ylabel("y")    # y軸のラベルを設定
     Text(0, 0.5, 'y')
   >>> plt.plot(x,y)    # グラフの描画
     [<matplotlib.lines.Line2D object at 0x7fa0a479eb70>]
   >>> plt.savefig('/var/www/projs/sweb/static/tblog/img/pid13_1.png')    # 各自の環境に合わせ、任意のパス、ファイル名を指定
  ```
  - 上記で出力したグラフ「pid13_1.png」
  ![pid13_1](/static/tblog/img/pid13_1.png)

- 2つのグラフ、凡例の設定と表示<br>
三角関数**y = sin(x)**と**y = cos(x)**を例に凡例の設定を行い、2つのグラフを表示する。
  ```bash
  $ python
   >>> import numpy as np
   >>> import matplotlib.pyplot as plt
   >>> x = np.arange(0, 6, 0.01)    # 区間を0～6 まで、描画制度を 0.01 刻みに設定
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
   >>> plt.savefig('/var/www/projs/sweb/static/tblog/img/pid13_2.png')    # 各自の環境に合わせ、任意のパス、ファイル名を指定
  ```
  - 上記で出力したグラフ「pid13_2.png」
  ![pid13_2](/static/tblog/img/pid13_2.png)

- **imread**を使った画像表示<br>
`matplotlib.imagen`の`imread`によって読み込んだ画像を`pyplot.imshow`で表示する。<br>
※ あらかじめ任意の画像を準備して`imread`で読み込み`imshow`で表示する。

  - 任意の画像「pid13_3.png」を準備<br>
  ![pid13_3](/static/tblog/img/pid13_3.png)

  - 「pid13_3.png」を`imread`で読み込み`imshow`で表示し、ファイル名を「pid13_4.png」として出力
    ```bash
    $ python
     >>> import matplotlib.pyplot as plt
     >>> from matplotlib.image import imread
     >>> img = imread('/var/www/projs/sweb/static/tblog/img/pid13_3.png')    # 任意の画像をimgに読込み
     >>> plt.imshow(img)    # 画像表示
     <matplotlib.image.AxesImage object at 0x7f4b80106f60>
     >>> plt.title('b_id36_3.png Read with image.imread \n and output as b_id36_4.png in pyplot.imshow')    # グラフタイトルを設定
     >>> plt.savefig('/var/www/projs/sweb/static/tblog/img/pid13_4.png')
    ```

  - 上記で出力したグラフ「pid13_4.png」
  ![pid13_4](/static/tblog/img/pid13_4.png)

- その他のグラフ<br>
上記以外にも`numpy.random`を使った分散図やヒストグラムなど様々なグラフに対応している。<br>
より詳細な使用方法は、下記ユーザーズガイドを参考。<br>
Matplotlibユーザーズガイド：https://matplotlib.org/users/index.html

### 参考文献
- 斎藤 康毅（2018）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
