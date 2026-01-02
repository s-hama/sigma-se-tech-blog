## タイトル
Python - 複合代入演算子まとめ : +=, -=, *=, /=, //=, %=, **=

## 目的
この記事では、Pythonで使用する複合代入演算子について基本的な使い方を記載する。

## 各複合代入演算子の使い方と実装サンプル

### 複合代入演算子の種類

**代入演算子**には、一般的な右辺から左辺へ代入する**代入演算子**（＝）と右辺から左辺へ**算術演算子**を添えて代入する**複合代入演算子**（+=, -=など）がある。

- 複合代入演算子一覧
    <table class="table" style="width: 100%;">
    <thead>
        <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>+=</td><td>a += b</td><td>a = a + b と同義。<br>（ a に b を加算した結果を a に代入 ）</td></tr>
        <tr><td>-=</td><td>a -= b</td><td>a = a - b と同義。<br>（ a から b を減算した結果を a に代入 ）</td></tr>
        <tr><td>*=</td><td>a *= b</td><td>a = a * b と同義。<br>（ a に b を乗算した結果を a に代入 ）</td></tr>
        <tr><td>/=</td><td>a /= b</td><td>a = a / b と同義。<br>（ a を b で除算した結果を a に代入 ）</td></tr>
        <tr><td>//=</td><td>a //= b</td><td>a = a // b と同義。<br>（ a を b で整数除算した結果を a に代入 ）</td></tr>
        <tr><td>%=</td><td>a %= b</td><td>a = a % b と同義。<br>（ a と b で剰余した結果を a に代入 ）</td></tr>
        <tr><td>**=</td><td>a **= b</td><td>a = a ** b と同義。<br>（ a を b でべき乗した結果を a に代入 ）</td></tr>
    </tbody>
    </table>

以降、簡単な実装サンプルを対話モード（インタプリタ）で解説する。

※ 演算結果の **最大値**、**最小値** についてはPCのスペックに依存する。詳しくは下記を参考。<br>
- [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#:~:text=%E5%88%A4%E5%AE%9A%E3%81%95%E3%82%8C%E3%82%8B%E3%80%82-,int%E5%9E%8B%20%3A%20%E6%95%B0%E5%80%A4%EF%BC%88%E6%95%B4%E6%95%B0%EF%BC%89,-%E6%95%B4%E6%95%B0%E5%9E%8B%E3%81%A7>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#:~:text=maxsize)%0A%20%20%20%209223372036854775807%0A%20%20%20%20%3E%3E%3E-,float%E5%9E%8B%20%3A%20%E6%B5%AE%E5%8B%95%E5%B0%8F%E6%95%B0%E7%82%B9%E6%95%B0%E5%9E%8B,-float%E5%9E%8B%E3%81%AF>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#:~:text=rounds%3D1)%0A%20%20%20%20%3E%3E%3E-,complex%E5%9E%8B%20%3A%20%E8%A4%87%E7%B4%A0%E6%95%B0%E5%9E%8B,-complex%E5%9E%8B%E3%81%AF>)
