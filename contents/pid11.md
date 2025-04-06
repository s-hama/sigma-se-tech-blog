## タイトル
Django - Django Debug Toolbar : デバッグ情報とカスタマイズ

## 目的
この記事では、Django Debug Toolbarのデバッグ情報とカスタマイズ方法について説明する。

## 概要説明と実施内容
### 表示パネルの概要説明
以下、インストール後の初期状態から表示されている**デフォルトパネル**について説明する。
1. Versions<br>
Webアプリで使用されている**モジュール（フレームワーク、言語、プラグイン等）のバージョン情報**が表示される。<br>
![pid11_1](/static/tblog/img/pid11_1.png)

2. Time（時刻）<br>
現在の画面が表示されるまでの**各処理に要した時間**が確認できる。<br>
![pid11_2](/static/tblog/img/pid11_2.png)<br>
    - Resource usage > User CPU time<br>
    クライアントからリクエストを受信してからページ構成を準備するまでの時間。
    - Resource usage > System CPU time<br>
    「User CPU time」の後にサーバーがレスポンス情報を作成し、クライアントに返すまでの時間。
    - Resource usage > Total CPU time<br>
    リクエストを受信してからクライアントに返すまでの時間。<br>
    （「User CPU time」 + 「System CPU time」 の合計）
    - Resource usage > Elapsed time<br>
    Total CPU time」にHTML、CSS、Javascriptに関するサーバー処理とクライアントでレタリングする時間を加えた時間。
    - Resource usage > Context switches<br>
    voluntary context switchesは、複数のプロセスを効率良く実行するため、自発的にコンテキストスイッチを実行した回数でinvoluntary context switchesは、実行優先度が高いプロセスを実行するために、強制的にコンテキストスイッチを実行した回数。

3. Settings<br>
**settings.py**を一覧で確認できる。<br>
![pid11_3](/static/tblog/img/pid11_3.png)

4. Headers<br>
**HTTP**の**リクエストヘッダー情報**、**レスポンスヘッダー情報**を確認できる。<br>
![pid11_4](/static/tblog/img/pid11_4.png)
