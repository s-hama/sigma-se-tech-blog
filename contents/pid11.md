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
FrameWorkに備わっている各アクション単位での通知の受け渡し一覧。<br>
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
