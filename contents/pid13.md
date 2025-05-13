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
