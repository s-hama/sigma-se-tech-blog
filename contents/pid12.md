## タイトル
Python - NumPy：ndarrayの基本操作と配列計算の使い方

## 概要

NumPyのndarrayによる配列の作成、四則演算、形状確認、ブロードキャスト、条件抽出を整理する。

3日分・2地点の気温データで地点別と日別の補正を比べる。行と列が何を表すかを決め、演算が失敗したときにshapeのどこを確認するかまで追う。補正の比較例はPython 3.12.2・NumPy 2.5.3で確認。

## この記事の構成
- [NumPyの環境準備](#numpyの環境準備)<br>
  NumPyの環境準備の手順と確認ポイントを整理。
- [NumPyの使用方法](#numpyの使用方法)<br>
  基本操作から地点別・日別の補正と形状エラーの切り分けへ進む。

## 実施内容
### NumPyの環境準備
**NumPy**は、高速な数値演算をはじめ、科学技術計算で広く利用されるPythonの外部ライブラリ。
同じデータ型の要素を持つ多次元配列`ndarray`と、Cなどで実装されたベクトル化処理を提供する。配列をまとめて計算するとPythonで要素ごとにループする場合より効率よく処理できることがあるが、効果はデータ量や演算内容に依存する。

- NumPyインストール<br>
使用するPython環境を明確にするため、次のようにPython経由でpipを実行。
  ```bash
  $ python -m pip install numpy
  ```
  インストール後は`python -c "import numpy as np; print(np.__version__)"`で、読み込まれたNumPyのバージョンを確認できる。

### NumPyの使用方法
- 配列の定義と型の確認<br>
`np.array()`へPythonのリストなどを渡すと、**numpy.ndarray型**の配列を生成できる。<br>
変数名に`list`を使うとPython組み込みの`list`を上書きしてしまうため、ここでは`values`とする。
  ```bash
  $ python
   >>> import numpy as np
   >>> values = np.array([0.5, 1.5, 2.5, 3.5, 4.5, 5.5])
   >>> print(values)
   [0.5 1.5 2.5 3.5 4.5 5.5]
   >>> type(values)
   <class 'numpy.ndarray'>
   >>>
  ```

- 一次元配列同士の四則演算<br>
**形状が同じ**配列同士、または後述するブロードキャストが可能な形状同士では、それぞれの要素を対応させて四則演算できる。
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
一次元配列と同様に、**形状が同じ**多次元配列同士では、それぞれの要素を対応させて四則演算できる。
  ```bash
  $ python
   >>> import numpy as np
   >>> matrix_a = np.array([[1, 2], [3, 4]])
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
  `*`は行列積ではなく**要素ごとの乗算**である。線形代数の行列積には`@`または`np.matmul()`を使う。
  ```bash
  >>> matrix_a @ matrix_b
  array([[ 35,  50],
         [ 75, 110]])
  ```
  - 形状とデータ型の確認<br>
  `shape`で各軸の要素数、`ndim`で次元数、`dtype`で要素のデータ型を確認できる。<br>二次元配列の`shape`は`(行数, 列数)`の順となる。
    ```bash
    $ python
     >>> import numpy as np
     >>> matrix_a = np.array([[1, 2], [3, 4]])
     >>> print(matrix_a)
     [[1 2]
       [3 4]]
     >>> matrix_a.shape    # 形状の確認
     (2, 2)
     >>> matrix_a.ndim     # 次元数の確認
     2
     >>> matrix_a.dtype    # データ型の確認
     dtype('int64')
    >>>
    ```
    `dtype`の表示はOSやPython、NumPyの環境によって異なる場合があるため、特定の整数幅を必要とする処理では`dtype=np.int64`のように明示する。

- ブロードキャスト<br>
NumPyでは、末尾の次元から比較し、各次元の大きさが等しいか、どちらかが`1`であればブロードキャストできる。<br>単に要素数が近いだけでは演算できない。下記3つは、互換性のある形状の例である。
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

- 地点ごとの補正と日ごとの補正をshapeで区別する<br>
  次の値は説明用の気温データで、行が1〜3日目、列が地点A・Bを表す。単位はすべて℃とする。まず地点Aへ1℃、地点Bへ-1℃を加える。

  ```python
  import numpy as np

  temperatures = np.array([[20, 22], [21, 23], [19, 21]])
  by_site = np.array([1, -1])
  print(temperatures.shape, by_site.shape)
  print(temperatures + by_site)
  ```

  ```text
  (3, 2) (2,)
  [[21 21]
   [22 22]
   [20 20]]
  ```

  末尾の次元が2で一致するため、地点別の補正を各行へ適用できる。今度は1日目に1℃、2日目に0℃、3日目に-1℃を加えたいとする。

  ```python
  import numpy as np

  temperatures = np.array([[20, 22], [21, 23], [19, 21]])
  by_day = np.array([1, 0, -1])
  try:
      print(temperatures + by_day)
  except ValueError as error:
      print(type(error).__name__)
  by_day_column = by_day.reshape(3, 1)
  print(by_day_column.shape)
  print(temperatures + by_day_column)
  ```

  ```text
  ValueError
  (3, 1)
  [[21 23]
   [21 23]
   [18 20]]
  ```

  | 加える配列 | shape | 末尾からの比較 | 結果 |
  | --- | --- | --- | --- |
  | 地点別の補正 | `(2,)` | 2と2が一致 | 各地点へ同じ補正を全日適用 |
  | 日別の補正を1次元のまま指定 | `(3,)` | 2と3が不一致 | ValueError |
  | 日別の補正を列の形に変更 | `(3, 1)` | 2と1、3と3で互換 | 各日の補正を両地点へ適用 |

  `reshape(3, 1)`は値の順番を変えずに「3行・1列」の形にする。1列を2地点へ広げて対応させられるため、日別の補正になる。エラーを消すためだけに形を変えず、補正値がどの軸に対応するかを先に確かめる。配列が正方形なら意図と違う軸でも演算できる場合があるので、成功したことだけでは対応の正しさを判断できない。

- 各要素の取得<br>
  - インデックスで要素を指定<br>
    Pythonのリストと同様にNumPyでもインデックスは0から始まり、下記要領でアクセスできる。<br>多次元配列では`matrix_c[0, 1]`のように各軸をカンマで指定する書き方もできる。
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
     >>> matrix_d = np.array([1, 5, 10, 15, 20, 25])
     >>> print(matrix_d)
     [ 1  5 10 15 20 25]
     >>> matrix_d[np.array([1, 3, 5])]    # インデックス 1, 3, 5 (2、4、6個目)を指定
     array([ 5, 15, 25])
     >>> matrix_d[1:4]    # インデックス1以上4未満をスライス
     array([ 5, 10, 15])
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

## まとめ

- ndarrayではshapeと各軸の意味を対応させてから演算する。2次元配列のshapeは行数・列数の順となる。
- ブロードキャストは末尾の次元から比較し、大きさが等しいか片方が1なら適用できる。
- 3行2列への地点別補正は(2,)、日別補正は(3, 1)というように目的に合わせて形を選ぶ。
- 演算の成功は軸の対応が意図どおりである保証にはならない。具体的な行・列の結果でも確かめる。

## 参考文献
- 斎藤 康毅（\\(2016\\)）『ゼロから作るDeep Learning ―Pythonで学ぶディープラーニングの理論と実装』株式会社オライリー・ジャパン
- [NumPy, Installing NumPy（英語・公式インストール手順）](https://numpy.org/install/)
- [NumPy User Guide, NumPy: the absolute basics for beginners（英語・配列操作の公式入門）](https://numpy.org/doc/stable/user/absolute_beginners.html)
- [NumPy User Guide, Broadcasting（英語・ブロードキャスト仕様）](https://numpy.org/doc/stable/user/basics.broadcasting.html)
- [NumPy User Guide, Indexing on ndarrays（英語・配列インデックス仕様）](https://numpy.org/doc/stable/user/basics.indexing.html)
