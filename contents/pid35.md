## タイトル
Python - 論理演算子まとめ : or, and, not

## 目的
この記事では、Pythonで使用する論理演算子について基本的な使い方を記載する。

## 各論理演算子の使い方と実装サンプル

### 論理演算子の種類

**論理演算子**には、bool型に加え、数値型である int型、float型、complex型や文字列である str型、リスト型であるlist型、tuple型、dict型の指定ができる。

- 各データ型の参考
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > bool型 : 真偽リテラル](<https://sigma-se.com/detail/30/#:~:text=%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E8%A8%98%E8%BC%89%E3%81%99%E3%82%8B%E3%80%82-,bool%E5%9E%8B%20%3A%20%E7%9C%9F%E5%81%BD%E3%83%AA%E3%83%86%E3%83%A9%E3%83%AB,-%E8%AB%96%E7%90%86%E5%9E%8B%E3%81%A8%E3%82%82>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#:~:text=%E5%88%A4%E5%AE%9A%E3%81%95%E3%82%8C%E3%82%8B%E3%80%82-,int%E5%9E%8B%20%3A%20%E6%95%B0%E5%80%A4%EF%BC%88%E6%95%B4%E6%95%B0%EF%BC%89,-%E6%95%B4%E6%95%B0%E5%9E%8B%E3%81%A7>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#:~:text=maxsize)%0A%20%20%20%209223372036854775807%0A%20%20%20%20%3E%3E%3E-,float%E5%9E%8B%20%3A%20%E6%B5%AE%E5%8B%95%E5%B0%8F%E6%95%B0%E7%82%B9%E6%95%B0%E5%9E%8B,-float%E5%9E%8B%E3%81%AF>)
  - [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#:~:text=rounds%3D1)%0A%20%20%20%20%3E%3E%3E-,complex%E5%9E%8B%20%3A%20%E8%A4%87%E7%B4%A0%E6%95%B0%E5%9E%8B,-complex%E5%9E%8B%E3%81%AF>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > str型 : 文字列型](<[str型 : 文字列型](https://sigma-se.com/detail/31/#:~:text=%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E8%A8%98%E8%BC%89%E3%81%99%E3%82%8B%E3%80%82-,str%E5%9E%8B%20%3A%20%E6%96%87%E5%AD%97%E5%88%97%E5%9E%8B,-%E6%96%87%E5%AD%97%E5%88%97%EF%BC%88Unicode)>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > list型 : 配列型](<https://sigma-se.com/detail/31/#:~:text=print(str_a)%0A%20%20%20%20Let%27s%0A%20%20%20%20%3E%3E%3E-,list%E5%9E%8B%20%3A%20%E9%85%8D%E5%88%97%E5%9E%8B,-%E8%AB%96%E7%90%86%E5%9E%8B%E3%82%84>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > tuple型 : 定数の配列型](<https://sigma-se.com/detail/31/#:~:text=%2C%2010%5D%0A%20%20%20%20%3E%3E%3E-,tuple%E5%9E%8B%20%3A%20%E5%AE%9A%E6%95%B0%E3%81%AE%E9%85%8D%E5%88%97%E5%9E%8B,-tuple%E5%9E%8B%E3%81%AF>)
  - [Python - 組込みデータ型まとめ : str, list, tuple, range, dict > range型 : 範囲指定](<https://sigma-se.com/detail/31/#:~:text=%27index%27%2C%20...%5D%0A%20%20%20%20%3E%3E%3E-,range%E5%9E%8B%20%3A%20%E7%AF%84%E5%9B%B2%E6%8C%87%E5%AE%9A,-range%E5%9E%8B%E3%81%AF>)

- 論理演算子一覧（or, and, not の三つのみ）
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>or</td><td>a or b</td><td>a、b の論理和</td></tr>
        <tr><td>and</td><td>a and b</td><td>a、b の論理積</td></tr>
        <tr><td>not</td><td>not a</td><td>a の否定</td></tr>
    </tbody>
    </table>

### True/Falseの判定基準

論理演算で最も重要となるTrue/Falseの判定基準として、**空文字**や**空リスト**等も`False`と判定される。<br>
下記一覧で示す要素以外は、すべて`True`として判定される。

- False判定一覧
    <table class="table" style="width: 80%;">
    <thead>
        <tr>
        <th scope="col">False判定となる要素</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>False</td><td>bool型のFalse</td></tr>
        <tr><td>None</td><td>何もないことを示すオブジェクト（≒多言語のNull）</td></tr>
        <tr><td>0</td><td>int型（整数）のゼロ</td></tr>
        <tr><td>0.0</td><td>float型（浮動小数点数）のゼロ</td></tr>
        <tr><td>0j</td><td>complex型（複素数）のゼロ</td></tr>
        <tr><td>Decimal(0)</td><td>decimal型のゼロ</td></tr>
        <tr><td>Fraction(0, 1)</td><td>fraction型（有理数）のゼロ</td></tr>
        <tr><td>''</td><td>str型（文字列）の空文字</td></tr>
        <tr><td>[]</td><td>list型（配列）の空配列</td></tr>
        <tr><td>{}</td><td>dict型（連想配列）の空配列</td></tr>
        <tr><td>()</td><td>tuple型（タプル）の空配列</td></tr>
        <tr><td>set()</td><td>set型（集合）の空配列</td></tr>
        <tr><td>range(0)</td><td>range型（数値配列）の空配列</td></tr>
    </tbody>
    </table>
<br>

※ 各実装サンプルについては、下記ページを参考。
- [Python - 組込みデータ型まとめ : bool , int, float, complex > bool型 : 真偽リテラル](<https://sigma-se.com/detail/30/#:~:text=%E3%81%AB%E3%81%A4%E3%81%84%E3%81%A6%E8%A8%98%E8%BC%89%E3%81%99%E3%82%8B%E3%80%82-,bool%E5%9E%8B%20%3A%20%E7%9C%9F%E5%81%BD%E3%83%AA%E3%83%86%E3%83%A9%E3%83%AB,-%E8%AB%96%E7%90%86%E5%9E%8B%E3%81%A8%E3%82%82>)

以降、論理演算子に関する簡単な実装サンプルを対話モード（インタプリタ）で解説する。
