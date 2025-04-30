## タイトル
Python - NumPy : numpy.ndarrayの使用方法

## 目的
この記事では、ndarrayの使用方法について説明する。

## 実施内容
### NumPyの環境準備
**NumPy**は、高速な数値演算をはじめ、学術計算も広く対応しているPythonの外部ライブラリ。
Python自体は、動的言語(非コンパイル型言語)で**数値演算が遅い**が、NumPyは、静的型付け言語である**C**、**C++**、**Fortran**で実装されているため、高速な数値演算を可能にしている。

- NumPyインストール<br>
インストールは、pipで`install numpy`を実行する。
  ```bash
  $ pip install numpy
   Collecting numpy
   Downloading
   https://files.pythonhosted.org/packages/ff/7f/9d804d2348471c67a7d8b5f84f9bc59fd1cefa148986f2b74552f8573555/numpy-1.15.4-cp36-cp36m-manylinux1_x86_64.whl (13.9MB)
       100% |################################| 13.9MB 1.3MB/s
   Installing collected packages: numpy
   Successfully installed numpy-1.15.4
  ```

### NumPyの使用方法
- 配列の定義と型の確認<br>
NumPy配列は、Python配列を引数を基に**numpy.ndarray型**で生成される。<br>
下記サンプルでは、Python配列`[0.5, 1.5, 2.5, 3.5, 4.5, 5.5]`を基にNumPy配列`[0.5, 1.5, 2.5, 3.5, 4.5, 5.5]`(numpy.ndarray型) を生成している。
  ```bash
  $ python
   >>> import numpy as np
   >>> list = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
   >>> print(list)
   [0.5 1.5 2.5 3.5 4.5 5.5]
   >>> type(list)
   <class 'numpy.ndarray'>
   >>>
  ```
