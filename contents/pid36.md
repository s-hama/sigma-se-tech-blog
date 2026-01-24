## タイトル
Python - ビット演算子まとめ : |, ^, &, ~, <<, >>

## 目的
この記事では、Pythonで使用するビット演算子の基本的な使い方について記載する。

## 各ビット演算子の使い方と実装サンプル

### ビット演算子の種類

**ビット演算子**は、\\(2\\)進数で表したint型の各ビットに対する演算子で、論理演算や反転、シフト等、以下の種類がある。

- ビット演算子一覧
    <table class="table" style="width: 100%;">
    <thead>
        <tr>
        <th scope="col">演算子</th>
        <th scope="col">使用例</th>
        <th scope="col">説明</th>
        </tr>
    </thead>
    <tbody>
        <tr><td>|</td><td>a | b</td><td>aとbのビット単位の論理和</td></tr>
        <tr><td>^</td><td>a ^ b</td><td>aとbのビット単位の排他的論理和</td></tr>
        <tr><td>&</td><td>a & b</td><td>aとbのビット単位の論理積</td></tr>
        <tr><td>~</td><td>~a</td><td>aのビット単位の反転（否定）</td></tr>
        <tr><td><<</td><td>a << b</td><td>aをbビット分、左にシフト</td></tr>
        <tr><td>>></td><td>a >> b</td><td>aをbビット分、右にシフト</td></tr>
    </tbody>
    </table>

以降、ビット演算子に関する簡単な実装サンプルを対話モード（インタプリタ）で解説する。
