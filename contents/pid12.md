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

- 一次元配列同士の四則演算<br>
**要素数が同じ**である場合、それぞれの要素同士で四則演算が可能。<br>
※ 但し、下記ブロードキャストは例外で 要素数が一致していなくても 四則演算が可能。
  ```bash
  $ python
   >>> import numpy as np
   >>> list_a = np.array([1.0, 2.0, 3.0])
   >>> list_b = np.array([2.0, 2.5, 3.0])
   >>> list_a + list_b    # 加算
   array([3. , 4.5, 6. ])
   >>> list_a - list_b    # 減算
   array([-1. , -0.5,  0. ])
   >>> list_a * list_b    # 乗算
   array([2., 5., 9.])
   >>> list_a / list_b    # 除算
   array([0.5, 0.8, 1. ])
   >>>
  ```

- 多次元配列（行列）の四則演算<br>
上記一次元配列同士の四則演算と同様に**行列が同じ**である場合、それぞれの要素同士で四則演算が可能。
  ```bash
  $ python
   >>> matrix_b = np.array([[5, 10], [15, 20]])
   >>> matrix_a + matrix_b    # 加算
   array([[ 6, 12],
           [18, 24]])
   >>> matrix_a - matrix_b    # 減算
   array([[ -4,  -8],
           [-12, -16]])
   >>> matrix_a * matrix_b    # 乗算
   array([[ 5, 20],
           [45, 80]])
   >>> matrix_a / matrix_b    # 除算
   array([[0.2, 0.2],
           [0.2, 0.2]])
   >>>
  ```
  - 形状とデータ型の確認<br>
  shapeで形状 (行列) を、dtypeでデータ型を確認できる。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_a = np.array([[1, 2], [3, 4]])
     >>> print(matrix_a)
     [[1 2]
       [3 4]]
     >>> matrix_a.shape    # 形状の確認
     (2, 2)
     >>> matrix_a.dtype    # データ型の確認
     dtype('int64')
    >>>
    ```

- ブロードキャスト<br>
NumPyでは、ブロードキャストという機能により、下記3つの例のように**形状(行列)が異なる配列**でも演算が可能。
  - 一次元配列とスカラ値（単一の数値）<br>
    一次元配列とスカラ値｢2｣との四則演算。
    ```bash
    $ python
     >>> import numpy as np
     >>> list_a = np.array([1.0, 2.0, 3.0])
     >>> list_a + 2    # 加算
     array([3., 4., 5.])
     >>> list_a - 2    # 減算
     array([-1.,  0.,  1.])
     >>> list_a * 2    # 乗算
     array([2., 4., 6.])
     >>> list_a / 2    # 除算
     array([0.5, 1. , 1.5])
     >>>
    ```
  - 多次元配列とスカラ値<br>
    多次元配列とスカラ値｢16｣との四則演算。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_a + 16    # 加算
     array([[17, 18],
             [19, 20]])
     >>> matrix_a - 16    # 減算
     array([[-15, -14],
             [-13, -12]])
     >>> matrix_a * 16    # 乗算
     array([[16, 32],
             [48, 64]])
     >>> matrix_a / 16    # 除算
     array([[0.0625, 0.125 ],
             [0.1875, 0.25  ]])
     >>>
    ```
  - 多次元配列と一次元配列<br>
    多次元配列と一次元配列との四則演算。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_a = np.array([[1, 2], [4, 8], [16, 32]])
     >>> matrix_b = np.array([2, 4])
     >>> matrix_a + matrix_b    # 加算
     array([[ 3,  6],
             [ 6, 12],
             [18, 36]])
     >>> matrix_a - matrix_b    # 減算
     array([[-1, -2],
             [ 2,  4],
             [14, 28]])
     >>> matrix_a * matrix_b    # 乗算
     array([[  2,   8],
             [  8,  32],
             [ 32, 128]])
     >>> matrix_a / matrix_b    # 除算
     array([[0.5, 0.5],
             [2. , 2. ],
             [8. , 8. ]])
     >>>
    ```

- 各要素の取得<br>
  - インデックスで要素を指定<br>
    他言語と同様にNumPyでもインデックス0から始まり、下記要領でアクセスできる。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_c = np.array([[1, 5], [10, 15], [20, 25]])
     >>> print(matrix_c)
     [[ 1  5]
       [10 15]
       [20 25]]
     >>> matrix_c[0]    # 行 1
     array([1, 5])
     >>> matrix_c[1]    # 行 2
     array([10, 15])
     >>> matrix_c[2]    # 行 3
     array([20, 25])
     >>> matrix_c[0][0]    # 行 1 、列 1
     1
     >>> matrix_c[0][1]    # 行 1 、列 2
     5
     >>> matrix_c[1][0]    # 行 2 、列 1
     10
     >>> matrix_c[1][1]    # 行 2 、列 2
     15
     >>> matrix_c[2][0]    # 行 3 、列 1
     20
     >>> matrix_c[2][1]    # 行 3 、列 2
     25
     >>>
    ```
  - 配列で要素を指定<br>
    インデックスだけでなく一次元配列に対して、配列で要素を指定することもできる。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_d = np.array([1, 5,10, 15, 20, 25])
     >>> print(matrix_d)
     [ 1  5 10 15 20 25]
     >>> matrix_d[np.array([1, 3, 5])]    # インデックス 1, 3, 5 (2、4、6個目)を指定
     array([ 5, 15, 25])
     >>>
    ```
  - 任意の条件で要素を指定<br>
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_e = np.array([1, 5, 2, 10, 3, 15, 4, 20, 5, 25])
     >>> matrix_e > 4    # 一次元配列に対して直接比較する
     array([False, True, False, True, False, True, False,  True, True, True])
     >>> matrix_e[matrix_e > 4]    # 上記の結果がTrueの要素のみ抽出する
     array([ 5, 10, 15, 20,  5, 25])
     >>>
     >>> matrix_e[matrix_e == 5]   # 5のみ抽出する
     array([5, 5])
     >>>
    ```

### 参考文献
- 斎藤 康毅（2018）『ゼロから作るDeep Learning - Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
