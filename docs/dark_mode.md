# ダークモードの管理

## 構成

共通テンプレートで `html[data-bs-theme]` を切り替える。初回は必ず `light` とし、OS設定には連動しない。明示的に選択された `light` / `dark` を `localStorage` の `sigma-se-theme` に保存する。

`theme_dm.js` は `<head>` で同期読み込みし、CSS・本文より前に保存済みテーマを適用する。保存領域が使えない場合はライトで開始し、そのページ内では切り替え可能。別タブでの変更と戻る／進むの復元にも追従する。JavaScript無効時はライト表示を維持し、操作できないボタンは表示しない。

ボタンはヘッダー右端の1個。ライトでは月、ダークでは太陽を表示する。標準の `button` を使い、Enter・Spaceで操作できる。操作先を示す読み上げラベルとフォーカス枠を持つ。Bootstrap Icons 1.13.1の `moon-stars` / `sun` のSVGを同梱し、アイコンフォントや新しい実行時ライブラリは追加しない。

## 配色

`custom.css` にはライトモードの既存配色と、両モード共通のレイアウト・切り替えボタンの位置や操作時のスタイルを置く。後から読み込む `custom_dm.css` には、`[data-bs-theme="dark"]` を条件とする配色とアイコンの切り替えだけを置く。

| 対象 | Bootstrap変数 |
| --- | --- |
| ページ外側・ナビゲーション・コード背景 | `--bs-gray-900` |
| サイト紹介・カード見出し・サイドメニュー見出し・情報帯・検索欄 | `--bs-gray-800` |
| 本文カード・記事一覧・サイドメニューの項目 | `--bs-gray-700` |
| 内部の区切り線 | `--bs-gray-600` |
| パネル・サイドメニュー・検索欄・ボタン・ページネーションの枠、コード内のコメント | `--bs-gray-500` |
| リンク | `--bs-gray-500` |
| リンクのホバー | `--bs-gray-400` |
| 日付などの補足 | `--bs-gray-300` |
| 本文・数式・コード文字 | `--bs-gray-200` |
| 見出し・SVGの文字と線 | `--bs-white` |

大枠ほど暗く、文章を読む面ほど明るくする。本文背景のgray-700に対する本文色gray-200のコントラスト比は約6.9:1。記事一覧とサイドメニューの項目は、ホバー時に背景をgray-800へ変えて操作対象を示す。

枠は通常時・ホバー時ともgray-500、太さはBootstrapの `--bs-border-width`（1px）に統一する。色は `--theme-frame-color-dm` で共通管理する。サイドメニューの外枠は操作を遮らない疑似要素をセルの手前に重ね、ホバー・キーボードフォーカス中のセルの枠は内側へのアウトラインで描く。通常の内部区切り線（gray-600）とセルの寸法は維持する。

ダークモードのカテゴリー・タグの背景は、親カテゴリーgray-900、子カテゴリーgray-600、タグgray-400とする。記事一覧の通常背景gray-700・ホバー背景gray-800のどちらとも同色にならず、ホバー・クリック中もラベルの色は変えない。リンクは通常文字と区別しやすいgray-500、ホバー時はgray-400とし、既存の下線を維持する。

ライトモードの記事一覧とページネーションは、サイドメニューと同じ淡いグレー（`--bs-light-border-subtle`）をホバー背景に使用し、記事一覧の文字・タグは反転させない。

グレー系と白以外の新規色は定義せず、Bootstrapの青いリンク・フォーカス色やコードの構文色もグレーに統一する。リンクは既存の下線、操作部品は枠・ホバー・フォーカスで識別する。サイト全体や画像への反転フィルターは使用しない。

PNGなどのスクリーンショット・既存画像は内容と色を維持し、透過画像内の暗い文字が消えないよう記事内画像の背面に白を敷く。広告など外部iframeの内容はサイトCSSの対象外。

## SVGの更新

元の `pidNN_NN.svg` が編集元。色以外は変更せず、同じ場所の `pidNN_NN_dm.svg` を生成する。外部SVG内の色はBootstrapの既存グレー／白に対応するカラーコードで明示する。背景矩形は追加せず、元の透過キャンバスを保つ。

```sh
# SVGを追加・編集した後に生成する（Python標準ライブラリのみ）
python3 -m tblog.svg_dm

# 未生成・更新漏れを検査する。問題があれば終了コード1
python3 -m tblog.svg_dm --check
```

文字・線に使われているgray-700は白へ、白抜き文字や白い塗りはgray-900へ変換する。これにより、塗りつぶされた帯の中の文字などの区別を保つ。新しい未対応色が見つかった場合は生成を止める。色の役割を確認したうえで `tblog/svg_dm.py` の対応表を更新する。

調査時点で既存のSVG生成処理はなく、SVGが直接管理されていたため、変種生成を独立したPythonモジュールとして追加した。新たに生成元を作る場合も、その処理の後で上記コマンドを実行する。

同一オリジンの `/static/tblog/img/pidNN_NN.svg` を参照する `img` は自動的に切り替わる。記事のHTML・Markdownにテーマ別の分岐は不要。動的な追加・src変更にも追従する。元のURLのクエリー・フラグメントを保持する。切り替え中のライト版のちらつきを抑え、ダーク版が見つからない場合は白背景付きの元画像へ戻す。従来の `post_media.js` による縮小・横スクロールは変更しない。

## 変更・追加ファイル

- 変更：`tblog/templates/tblog/base.html` — 初期テーマ、CSS・JS読み込み、ボタンの共通組み込み。
- 追加：`tblog/templates/tblog/theme_toggle_dm.html` — Bootstrap Iconsを使用する切り替えボタン。
- 追加：`static/tblog/theme_dm.js` — 初期適用、保存、操作、SVG切り替え。
- 変更：`static/tblog/custom.css` — 両モード共通のレスポンシブレイアウトと切り替えボタンの表示・位置。
- 追加：`static/tblog/custom_dm.css` — ダーク配色とダーク時のアイコン表示。
- 追加：`tblog/svg_dm.py` — SVGの生成と更新漏れ検査。
- 追加：`tblog/tests_dm.py` — 共通テンプレート、SVG構造・色・更新状態の検証。
- 追加：`docs/bootstrap_icons_license_dm.txt` — 同梱アイコンのMITライセンス。
- 追加：`docs/dark_mode.md` — 本書。

追加したSVG（元ファイルは変更しない）：

- `static/tblog/img/pid17_1_dm.svg`
- `static/tblog/img/pid46_1_dm.svg`
- `static/tblog/img/pid71_1_dm.svg`
- `static/tblog/img/pid71_2_dm.svg`
- `static/tblog/img/pid71_3_dm.svg`
- `static/tblog/img/pid71_4_dm.svg`
- `static/tblog/img/pid72_1_dm.svg`
- `static/tblog/img/pid72_2_dm.svg`
- `static/tblog/img/pid72_3_dm.svg`
- `static/tblog/img/pid73_1_dm.svg`
- `static/tblog/img/pid73_2_dm.svg`
- `static/tblog/img/pid73_3_dm.svg`
- `static/tblog/img/pid74_1_dm.svg`
- `static/tblog/img/pid74_2_dm.svg`
- `static/tblog/img/pid75_1_dm.svg`
- `static/tblog/img/pid75_2_dm.svg`
- `static/tblog/img/pid76_1_dm.svg`
- `static/tblog/img/pid76_2_dm.svg`
- `static/tblog/img/pid77_1_dm.svg`
- `static/tblog/img/pid78_1_dm.svg`
- `static/tblog/img/pid78_2_dm.svg`
- `static/tblog/img/pid78_3_dm.svg`
- `static/tblog/img/pid79_1_dm.svg`
- `static/tblog/img/pid80_1_dm.svg`
- `static/tblog/img/pid86_1_dm.svg`
- `static/tblog/img/pid87_1_dm.svg`
- `static/tblog/img/pid89_1_dm.svg`
- `static/tblog/img/pid89_2_dm.svg`
- `static/tblog/img/pid89_3_dm.svg`
- `static/tblog/img/pid89_4_dm.svg`
- `static/tblog/img/pid89_5_dm.svg`
- `static/tblog/img/pid89_6_dm.svg`
- `static/tblog/img/pid89_7_dm.svg`
- `static/tblog/img/pid89_8_dm.svg`
- `static/tblog/img/pid89_9_dm.svg`
- `static/tblog/img/pid89_10_dm.svg`
- `static/tblog/img/pid89_11_dm.svg`
- `static/tblog/img/pid89_12_dm.svg`
- `static/tblog/img/pid89_13_dm.svg`
- `static/tblog/img/pid91_1_dm.svg`
- `static/tblog/img/pid91_2_dm.svg`

## 検証

```sh
python manage.py test tblog --settings=config.test_settings
python3 -m tblog.svg_dm --check
```

2026-11-14の確認：

- Djangoテスト32件成功（既存28件、新規4件）。本番DBを使用しないSQLiteテスト設定。
- 全41SVGについて、生成状態、XML構文、色以外の属性・要素・文字の一致を確認。元SVGのSHA-256も作業開始時と一致。
- ローカルでレンダリングしたトップ・一覧・検索（結果あり／なし）・カテゴリ・タグ・記事・プロフィール・お問い合わせ・プライバシーポリシー・サイトマップをChromeで確認。
- 幅375 / 768 / 992 / 1440pxで、変更前後のライト表示の位置・寸法・色・余白に差分なし（トップ、一覧、記事79・89を比較）。
- 幅320 / 375 / 768 / 992 / 1024 / 1440pxでヘッダーのボタンと既存メニューが重ならないことを確認。ログイン時の管理リンクも対象。
- OSがダーク設定でも初回はライト。保存済みダークの早期適用、再読み込み、ページ移動、別タブ同期、Enter・Space操作、保存領域の利用不可を確認。
- ダークSVG41枚のロード、テーマ切り替え後の寸法維持、スマホ幅の画像横スクロール、モバイルメニューを確認。
- 本文・テーブル・コード・MathJaxの表示色が許可パレット内にあることを確認。リンク・入力・ボタンのホバー／フォーカス時も確認。記事89と共通UIの文字コントラストは最小4.68:1。
- 動的なSVG追加・src変更、外部SVGを切り替え対象から除外すること、ダーク版欠落時の元画像への復帰を確認。

実機のiPhone／Safariでの確認は未実施。PNGなどは元の色を維持するため、画像内にはライト背景が残る。本番デプロイ、既存CSS・JSのキャッシュ更新用URL変更は行わない。

2026-11-15の配色階層変更時の確認：

- Chromeの幅375 / 700 / 880 / 1440pxでトップ・一覧・検索・記事79・89を確認。
- ライトモード16条件の変更前後で、要素の位置・寸法・文字色・背景色・枠色・余白に差分なし。
- ダークモード20条件で、外側gray-900、タイトル帯・情報帯gray-800、本文・サイドメニュー項目gray-700を確認。ページ全体の横はみ出しなし。
- 本文・表・MathJaxの文字色、SVGの読み込み、一覧とサイドメニューのホバー、切り替え後のテーマ保存を確認。
- PC・スマホ幅のスクリーンショットで配色を確認。共通CSS・テンプレート・JavaScript・SVGの変更なし。

同日のホバー・サイドメニュー外枠変更時の確認：

- Chromeの幅375 / 700 / 880 / 1440px、ライト・ダーク、一覧・検索・記事の24条件で通常表示の位置・寸法・配色を比較。追加したダークの外枠以外に変更なし。
- ライトの記事一覧・ページネーションのホバー背景がサイドメニューと一致し、一覧の文字・タグは反転しないことを確認。ページネーションの選択中表示は通常時に維持。
- ダークの外枠、ホバー中のセル、展開した子カテゴリー、キーボードフォーカスを確認。内部区切り線とセルの寸法を維持し、疑似要素が操作を遮らないことを確認。PCのスクリーンショットでも外枠の描画を確認。

同日の枠・リンク・タグの明暗調整時の確認（上記の白い枠をgray-500へ変更）：

- Chromeの幅375 / 700 / 880 / 1440pxで、ライト12条件に表示差分なし。ダーク16条件と検索欄・検索ボタンで、通常時・ホバー時の枠がgray-500・1pxで揃うことを確認。
- リンクはgray-400、ホバー時gray-300。本文背景gray-700とのコントラスト比は通常時約5.47:1。
- 記事一覧のラベル色がホバー・クリック・キーボードフォーカス中も変わらず、通常時とホバー時のパネル背景のどちらとも異なることを確認。
- 通常の内部区切り線、横はみ出し、キーボード操作を確認。PC・スマホ幅のスクリーンショットでも確認。

その後、通常文字との区別を強める依頼に合わせ、リンクをgray-500、ホバー時をgray-400へ調整。Chromeの幅375 / 1440pxで、リンク色・下線の維持・ライト表示に差分がないことを確認した。本文背景gray-700に対する通常リンクのコントラスト比は約3.94:1となるため、上記の約5.47:1は調整前の値。

## 参照

- [Bootstrap 5.3 Color modes](https://getbootstrap.com/docs/5.3/customize/color-modes/)
- [Bootstrap Icons: moon-stars](https://icons.getbootstrap.com/icons/moon-stars/)
- [Bootstrap Icons: sun](https://icons.getbootstrap.com/icons/sun/)
