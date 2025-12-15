## タイトル
Python - 算術演算子まとめ : +, -, *, /, //, **

## 目的
この記事では、算術演算子について基本的な使い方を記載する。

## 各算術演算子の使い方と実装サンプル

### 算術演算子の種類
**算術演算子**は、一般的な**四則演算**とプログラム特有の表現である**単項プラス演算**と**単項マイナス演算**を合わせた演算子を指す。

- 算術演算子一覧
  <table class="table" style="width: 100%;">
    <thead>
      <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
      </tr>
    </thead>
    <tbody>
      <tr><td>+</td><td>+a</td><td>正の整数：実質 a と同義。（暗黙的変換で用いる）</td></tr>
      <tr><td>-</td><td>-a</td><td>符号反転：a の符号を反転する。</td></tr>
      <tr><td>+</td><td>a + b</td><td>加算：a に b を足す。</td></tr>
      <tr><td>-</td><td>a - b</td><td>減算：a から b を引く。</td></tr>
      <tr><td>*</td><td>a * b</td><td>乗算：a に b を掛ける。</td></tr>
      <tr><td>/</td><td>a / b</td><td>除算：a を b で割る。</td></tr>
      <tr><td>//</td><td>a // b</td><td>整数除算：a を b で割った結果から小数以下を切り捨てる。</td></tr>
      <tr><td>%</td><td>a % b</td><td>剰余：a を b で割った余り。</td></tr>
      <tr><td>**</td><td>a ** b</td><td>べき乗：a の b 乗。</td></tr>
    </tbody>
  </table>

以降、簡単な実装サンプルを対話モード（インタプリタ）で解説する。

※ 演算結果の **最大値**、**最小値** についてはPCのスペックに依存する。詳しくは下記を参考。<br>
- [Python - 組込みデータ型まとめ : bool , int, float, complex > int型 : 数値（整数）](<https://sigma-se.com/detail/30/#:~:text=%E5%88%A4%E5%AE%9A%E3%81%95%E3%82%8C%E3%82%8B%E3%80%82-,int%E5%9E%8B%20%3A%20%E6%95%B0%E5%80%A4%EF%BC%88%E6%95%B4%E6%95%B0%EF%BC%89,-%E6%95%B4%E6%95%B0%E5%9E%8B%E3%81%A7>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > float型 : 浮動小数点数型](<https://sigma-se.com/detail/30/#:~:text=maxsize)%0A%20%20%20%209223372036854775807%0A%20%20%20%20%3E%3E%3E-,float%E5%9E%8B%20%3A%20%E6%B5%AE%E5%8B%95%E5%B0%8F%E6%95%B0%E7%82%B9%E6%95%B0%E5%9E%8B,-float%E5%9E%8B%E3%81%AF>)
- [Python - 組込みデータ型まとめ : bool , int, float, complex > complex型 : 複素数型](<https://sigma-se.com/detail/30/#:~:text=rounds%3D1)%0A%20%20%20%20%3E%3E%3E-,complex%E5%9E%8B%20%3A%20%E8%A4%87%E7%B4%A0%E6%95%B0%E5%9E%8B,-complex%E5%9E%8B%E3%81%AF>)
