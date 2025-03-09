## タイトル
Python - 標準デバッガー（Pdb）: 使用例と基本操作方法

## 目的
この記事では、Pythonの標準デバッガー（Pdb）の使用例と基本操作方法について説明する。

## 実施内容
### Pdbの使用例
- 説明用のサンプルプログラムを作成<br>
説明用に下記`debug_sample.py`を作成する。<br>
  ```python
  1 def add(a, b, c):
  2     return a + b + c
  3 
  4 step = 0
  5
  6 step = add(1, 2, 3)
  7 step = add(4, 5, 6)
  ```

- 4行目に`import pdb; pdb.set_trace()`を挿入<br>
この状態で4行目の直後となる6行目の`step = 0`がブレイクポイントとなる。
  ```python
  1 def add(a, b, c):
  2     return a + b + c
  3
  4 import pdb; pdb.set_trace()
  5
  6 step = 0
  7
  8 step = add(1, 2, 3)
  9 step = add(4, 5, 6)
  ```
