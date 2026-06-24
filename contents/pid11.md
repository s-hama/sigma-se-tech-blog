## タイトル
Django - Django Debug Toolbar：2/2 デバッグ情報とカスタマイズ

## 概要

Django Debug Toolbarで確認できる代表的な表示パネルと、DEBUG_TOOLBAR_PANELSによるカスタマイズ方法を整理する。

Toolbarの各パネルは、バージョン、処理時間、SQL、テンプレート、キャッシュ、ログなど、画面表示時の内部情報を確認する入口になる。どのパネルで何を見られるかを知っておくと、原因調査の流れを作りやすい。

## この記事で扱うこと
- Versions、Time、Settingsなどの基本パネルの役割。
- Headers、Request、SQL、Templatesで確認できる情報。
- Cache、Signals、Logging、Redirectsの使いどころ。
- DEBUG_TOOLBAR_PANELSで表示パネルを変更する方法。
- プロファイリング用パネルを追加する考え方。

## 作業前に確認すること

| 項目 | 確認内容 |
| --- | --- |
| 表示パネル | 調査したい対象に応じて見るパネルを選ぶ。 |
| SQLパネル | N+1問題やクエリ回数の確認に使う。 |
| Templatesパネル | どのテンプレートが使われたかを確認する。 |
| Loggingパネル | 画面表示時に出力されたログを確認する。 |
| カスタマイズ | 必要なパネルだけを表示して調査しやすくする。 |

## 作業時の注意点

| 作業時の注意点 | 確認ポイント |
| --- | --- |
| パネルの見方 | 全パネルを見るより、調査目的に合わせて見る場所を決める。 |
| Timeの解釈 | サーバー処理とブラウザ側の表示時間を混同しない。 |
| SQLの多さ | クエリ数だけでなく、同じSQLが繰り返されていないかを見る。 |
| Redirects | 有効化するとリダイレクト動作が変わるため、調査時だけ使う。 |

## 実施内容
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
    「Total CPU time」は、HTML、CSS、JavaScriptに関するサーバー処理とクライアント側のレンダリング時間を含めた値。
    - Resource usage > Context switches<br>
    voluntary context switchesは、複数のプロセスを効率良く実行するため、自発的にコンテキストスイッチを実行した回数でinvoluntary context switchesは、実行優先度が高いプロセスを実行するために、強制的にコンテキストスイッチを実行した回数。

3. Settings<br>
**settings.py**を一覧で確認できる。<br>
![pid11_3](/static/tblog/img/pid11_3.png)

4. Headers<br>
**HTTP**の**リクエストヘッダー情報**、**レスポンスヘッダー情報**を確認できる。<br>
![pid11_4](/static/tblog/img/pid11_4.png)

5. Request<br>
ViewやCookie、Sessionなどの**リクエスト情報**を確認できる。<br>
![pid11_5](/static/tblog/img/pid11_5.png)

6. SQL<br>
画面が表示されるまでに**実行されたSQL文**をはじめ、それぞれに要した**実行時間**や**Stacktrace**を確認できる。<br>
![pid11_6](/static/tblog/img/pid11_6.png)

7. Static Files<br>
画面を表示する際に読み込んだ**Staticファイル**を確認できる。<br>
![pid11_7](/static/tblog/img/pid11_7.png)

8. Templates<br>
画面を表示する際に使用された継承も含む**Templateファイル**を確認できる。<br>
![pid11_8](/static/tblog/img/pid11_8.png)

9. Cache<br>
画面を表示する際に利用された**キャッシュバックエンド情報**を確認できる。<br>
![pid11_9](/static/tblog/img/pid11_9.png)

10.  Signals<br>
フレームワークに備わっている各アクション単位での通知の受け渡し一覧。<br>
![pid11_10](/static/tblog/img/pid11_10.png)

11.  Logging<br>
loggingモジュールで出力したログが確認できる。<br>
![pid11_11](/static/tblog/img/pid11_11.png)

12.  Intercept redirects<br>
デフォルト無効であるチェックボックスを有効にすると**リダイレクトが中断**されるようになる。<br>
※ リダイレクト処理をデバッグするときに使用する。

### 表示パネルのカスタマイズ
上記デフォルトパネルは、**settings.py**の`DEBUG_TOOLBAR_PANELS`に設定されている。
- settings.pyの`DEBUG_TOOLBAR_PANELS`（デフォルト）
下記`DEBUG_TOOLBAR_PANELS`を変更することで**パネルの並び替え**や**削除**、**追加**ができるようになる。
  ```ini
  DEBUG_TOOLBAR_PANELS = [
      'debug_toolbar.panels.versions.VersionsPanel',
      'debug_toolbar.panels.timer.TimerPanel',
      'debug_toolbar.panels.settings.SettingsPanel',
      'debug_toolbar.panels.headers.HeadersPanel',
      'debug_toolbar.panels.request.RequestPanel',
      'debug_toolbar.panels.sql.SQLPanel',
      'debug_toolbar.panels.staticfiles.StaticFilesPanel',
      'debug_toolbar.panels.templates.TemplatesPanel',
      'debug_toolbar.panels.cache.CachePanel',
      'debug_toolbar.panels.signals.SignalsPanel',
      'debug_toolbar.panels.logging.LoggingPanel',
      'debug_toolbar.panels.redirects.RedirectsPanel'
  ]
  ```

- **プロファイリング情報**の追加例
  ```ini
  DEBUG_TOOLBAR_PANELS = [
      'debug_toolbar.panels.versions.VersionsPanel',
      'debug_toolbar.panels.timer.TimerPanel',
      'debug_toolbar.panels.settings.SettingsPanel',
      'debug_toolbar.panels.headers.HeadersPanel',
      'debug_toolbar.panels.request.RequestPanel',
      'debug_toolbar.panels.sql.SQLPanel',
      'debug_toolbar.panels.staticfiles.StaticFilesPanel',
      'debug_toolbar.panels.templates.TemplatesPanel',
      'debug_toolbar.panels.cache.CachePanel',
      'debug_toolbar.panels.signals.SignalsPanel',
      'debug_toolbar.panels.logging.LoggingPanel',
      'debug_toolbar.panels.profiling.ProfilingPanel'    # 追記
  ]
  ```
  末尾に追加した**プロファイリング情報**が確認できるようになる。<br>
  ![pid11_12](/static/tblog/img/pid11_12.png)

- その他のパネルについて
下記**サードパーティ製**のパネルを参照。<br>
https://django-debug-toolbar.readthedocs.io/en/stable/panels.html#third-party-panels

## 実務とのつながり
- 性能改善<br>
    SQL回数や処理時間を見てボトルネックを探せる。
- テンプレート調査<br>
    継承関係や読み込まれたテンプレートを確認できる。
- デバッグ設計<br>
    調査に必要なパネルだけを残すと、確認作業が効率化する。

## まとめ
- Django Debug Toolbarの各パネルは、Django画面表示の内部状態を確認するための入口になる。
- SQL、Templates、Timeなどは、性能調査や表示不具合の確認で特に役立つ。
- DEBUG_TOOLBAR_PANELSを使うと、必要なパネルだけに絞って調査しやすくできる。
