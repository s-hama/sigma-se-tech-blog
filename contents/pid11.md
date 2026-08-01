## タイトル
Django - Django Debug Toolbar：2/2 デバッグ情報とカスタマイズ

## 概要

Django Debug Toolbarで確認できる代表的な表示パネルと、`DEBUG_TOOLBAR_PANELS`によるカスタマイズ方法を整理する。

Toolbarの各パネルは、バージョン、処理時間、SQL、テンプレート、キャッシュ、ログなど、画面表示時の内部情報を確認する入口になる。<br>どのパネルで何を見られるかを知っておくと、原因調査の流れを作りやすい。

掲載画像はDjango 2.0.2を利用していた当時の画面であり、現行版とはパネル名や構成が異なる。<br>画像は画面の見方をつかむための旧版例として使用し、現行版との差分もあわせて説明する。

## この記事の構成
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [表示パネルの概要説明](#表示パネルの概要説明)<br>
  各パネルで確認できるリクエスト、SQL、テンプレートなどの情報を整理。
- [現行版での主な違い](#現行版での主な違い)<br>
  現行版での主な違いを対比し、それぞれの特徴を整理。
- [表示パネルのカスタマイズ](#表示パネルのカスタマイズ)<br>
  表示するパネルを設定で追加・削除・並べ替える方法を確認。

## 作業時の注意点

- パネルの見方<br>
全パネルを見るより、調査目的に合わせて見る場所を決める。
- Timerの解釈<br>
サーバー処理とブラウザ側の表示時間を混同しない。
- SQLの多さ<br>
クエリ数だけでなく、同じSQLが繰り返されていないかを見る。
- Redirects<br>
有効化するとリダイレクト動作が変わるため、調査時だけ使う。
- 公開環境での利用<br>
設定値やSQLなどの内部情報を表示するため、外部公開された本番環境では有効にしない。

## 実施内容
### 表示パネルの概要説明
以下は、掲載画像を取得した旧バージョンで表示されていたパネルについての説明である。<br>現行版の構成は後述の「現行版での主な違い」で補足する。
1. Versions<br>
Python、Django、インストール済みアプリなど、調査対象の**バージョン情報**を確認。依存ライブラリ固有の不具合を調べるときは、まずここで実行環境を特定する。<br>
![Versionsパネルに表示されたDjangoなどのバージョン情報](/static/tblog/img/pid11_1.png)

2. Timer（掲載画像では「時刻」）<br>
リクエスト処理の**CPU時間と経過時間**を確認。<br>掲載画像ではブラウザ側のタイミングも別欄に表示されている。<br>
![Timerパネルに表示されたCPU時間と経過時間](/static/tblog/img/pid11_2.png)<br>
    - Resource usage > User CPU time<br>
    Pythonプロセスがユーザーモードで実際にCPUを使用した時間。
    - Resource usage > System CPU time<br>
    OSカーネルがシステムコールなどの処理にCPUを使用した時間。
    - Resource usage > Total CPU time<br>
    User CPU timeとSystem CPU timeの合計。
    - Resource usage > Elapsed time<br>
    処理開始から終了までに経過した実時間。I/O待ちなども含むため、通常はTotal CPU timeと一致しない。ブラウザの描画時間そのものを表す値ではない。
    - Resource usage > Context switches<br>
    voluntaryはI/O待ちなどで処理が自発的にCPUを譲った回数、involuntaryはOSのスケジューラによって実行が切り替えられた回数。

3. Settings<br>
**settings.py**の設定値を一覧で確認できる。
![Settingsパネルに表示されたDjango設定値の一覧](/static/tblog/img/pid11_3.png)

1. Headers<br>
**HTTP**の**リクエストヘッダー情報**、**レスポンスヘッダー情報**、WSGI環境情報を確認できる。
![旧版のHeadersパネルに表示されたリクエスト・レスポンスヘッダーとWSGI環境情報](/static/tblog/img/pid11_4.png)

1. Request<br>
ViewやCookie、Sessionなどの**リクエスト情報**を確認できる。
![旧版のRequestパネルに表示されたView、Cookie、Session情報](/static/tblog/img/pid11_5.png)

1. SQL<br>
画面が表示されるまでに**実行されたSQL文**、各クエリの**実行時間**、類似・重複クエリ、スタックトレースなどを確認できる。
![旧版のSQLパネルに表示されたSQL文、実行時間、類似・重複クエリ](/static/tblog/img/pid11_6.png)

1. Static Files<br>
画面を表示する際に読み込んだ**Staticファイル**を確認できる。<br>
![Static Filesパネルに表示された使用済み静的ファイル](/static/tblog/img/pid11_7.png)

1. Templates<br>
画面を表示する際に使用された**テンプレート、継承関係、コンテキスト**を確認できる。<br>想定外のテンプレートが選ばれた場合や、変数が渡っていない場合の切り分けに使う。<br>
![Templatesパネルに表示されたテンプレートとコンテキスト](/static/tblog/img/pid11_8.png)

1. Cache<br>
リクエスト中に行われた**キャッシュ操作**や処理時間を確認。<br>キャッシュが期待どおり使われているか、同じキーへ不要なアクセスがないかを調べる入口になる。<br>
![Cacheパネルに表示されたキャッシュ操作の情報](/static/tblog/img/pid11_9.png)

1.   Signals<br>
Djangoの**シグナルと登録済みレシーバー**を一覧で確認。<br>意図したレシーバーが登録されているかを調べる際に役立つ。<br>
![Signalsパネルに表示されたシグナルとレシーバーの一覧](/static/tblog/img/pid11_10.png)

1.   Logging<br>
当時の組み込みLoggingパネルでは、Pythonのloggingモジュールで出力したログを確認できた。<br>現行版の組み込みパネル一覧には含まれていないため、現在の環境では通常のログ出力や対応する外部ツールを利用。<br>
![旧版のLoggingパネルに表示されたリクエスト処理中のログ](/static/tblog/img/pid11_11.png)

1.   Intercept redirects<br>
有効にするとリダイレクト前に中間ページを表示し、その時点のデバッグ情報を確認できる。<br>ただし、現行版では非推奨で、リダイレクトされたリクエストの情報はHistoryパネルから確認する方法が推奨されている。

### 現行版での主な違い
掲載画像の旧版と比べ、現行版の組み込みパネルにはHistory、Alerts、Communityなどが追加されている。<br>一方、旧版のLoggingパネルは現行版の組み込み一覧には含まれない。

- History<br>
    過去のリクエストを選び、その時点のToolbar情報を確認。<br>
    リダイレクト前後の調査にも利用できる。
- Alerts<br>
    ファイル入力を含むフォームで`enctype="multipart/form-data"`が不足している場合など、既知の問題を通知する。
- Redirects<br>
    現行版にも含まれるが既定では無効で、バージョン6.0から非推奨となっている。
- Profiling<br>
    リクエスト処理中の関数呼び出しを確認するパネル。<br>
    現行版では構成に含まれるが既定では無効である。

### 表示パネルのカスタマイズ
表示するパネルは、**settings.py**の`DEBUG_TOOLBAR_PANELS`で変更できる。<br>現行版の既定値は次の構成で、**並び替え**、**削除**、**追加**が可能である。<br>ただし、既定値をそのままコピーすると将来の改善を取り込めなくなるため、変更が必要な場合だけ設定する。

  ```python
  DEBUG_TOOLBAR_PANELS = [
      'debug_toolbar.panels.history.HistoryPanel',
      'debug_toolbar.panels.versions.VersionsPanel',
      'debug_toolbar.panels.timer.TimerPanel',
      'debug_toolbar.panels.settings.SettingsPanel',
      'debug_toolbar.panels.headers.HeadersPanel',
      'debug_toolbar.panels.request.RequestPanel',
      'debug_toolbar.panels.sql.SQLPanel',
      'debug_toolbar.panels.staticfiles.StaticFilesPanel',
      'debug_toolbar.panels.templates.TemplatesPanel',
      'debug_toolbar.panels.alerts.AlertsPanel',
      'debug_toolbar.panels.cache.CachePanel',
      'debug_toolbar.panels.signals.SignalsPanel',
      'debug_toolbar.panels.community.CommunityPanel',
      'debug_toolbar.panels.redirects.RedirectsPanel',
      'debug_toolbar.panels.profiling.ProfilingPanel',
  ]
  ```

- **プロファイリング情報**の確認例<br>
  Profilingパネルを有効にすると、関数ごとの呼び出し回数や処理時間を確認できる。<br>Python 3.12以降では、公式ドキュメントに記載された実行条件もあわせて確認。<br>
  ![旧版のProfilingパネルに表示された関数ごとの処理時間](/static/tblog/img/pid11_12.png)

- その他のパネルについて
公式ドキュメントには**サードパーティ製**のパネルも掲載されているが、Django Debug Toolbar本体による正式サポートの対象外である。<br>導入前に、対応バージョンや更新状況を確認。

## まとめ
- Django Debug Toolbarの各パネルは、Django画面表示の内部状態を確認するための入口になる。
- SQL、Templates、Timerなどは、性能調査や表示不具合の確認で特に役立つ。
- `DEBUG_TOOLBAR_PANELS`を使うと、必要なパネルだけに絞って調査しやすくできる。
- パネル構成はバージョンによって変わるため、旧版の画面例と利用中の公式ドキュメントを照合する。

### 参考文献
- [Django ドキュメント「データベースアクセスの最適化」（日本語・クエリ分析とデバッグツールの公式解説）](https://docs.djangoproject.com/ja/5.2/topics/db/optimization/)
- [Django Debug Toolbar Documentation, Panels（英語・表示パネル仕様）](https://django-debug-toolbar.readthedocs.io/en/stable/panels.html)
- [Django Debug Toolbar Documentation, Configuration（英語・パネル設定仕様）](https://django-debug-toolbar.readthedocs.io/en/stable/configuration.html)
