# サイトマップ

- `/sitemap/`：読者向けの全記事一覧。大カテゴリ・小カテゴリ・シリーズ順に表示し、連載番号を数値順に並べます。トップでの掲載件数制限は適用しません。
- `/sitemap.xml`：Google向けのXML。公開記事とトップ・サイトマップ・プロフィール・お問い合わせ・プライバシーポリシーの正規URLを自動出力します。
- `/robots.txt`：XMLサイトマップのURLを案内します。公開ページのクロールを許可し、管理画面を除外します。

両サイトマップとも、`is_publick=True` で `PaidContent` カテゴリ以外の記事を掲載します。ログイン中のアクセスでも掲載範囲は変わりません。検索結果・タグ一覧・カテゴリ一覧・管理画面のURLはXMLに含めません。

シリーズの説明・判定条件は `tblog/series.py` でトップと共有しています。判定条件に当てはまらない公開記事も、HTMLサイトマップの該当カテゴリ内に必ず掲載します。

HTMLサイトマップの表示名は、ヘッダー・本文・フッターとも「サイトマップ」です。「サイトのご案内」セクションは設けず、固定ページへのリンクは共通ヘッダーから利用できます。

各セクションは、大カテゴリの見出し、小カテゴリの箇条書き、字下げした説明文、入れ子の箇条書きによる記事リンクの順に表示します。シリーズ名の重複見出しは表示しません。大カテゴリの見出しと説明文・リンクの書式はトップページと共有しています。

HTMLサイトマップでは共通テンプレートの `ads` ブロックを空にし、AdSenseスクリプトを読み込みません。

## 更新日

XMLの `lastmod` は記事の `Post.updated_at` を使います。閲覧やXML生成の日時ではありません。更新日を管理していない固定ページでは `lastmod` を省略します。

`updated_at` はモデル保存時に自動更新されます。本文などの実質的な変更を保存した日時として運用し、日付を新しく見せる目的で記事を一括保存しないでください。`QuerySet.update()` や直接SQLで本文を更新する場合は、`updated_at` も実際の変更日時へ更新する必要があります。

## 本番反映後の確認・送信

本番の `config/settings.py` には、その環境のDB接続情報などが含まれます。ローカルのファイルで丸ごと上書きせず、変更前の本番設定を保存したうえで、既存の `INSTALLED_APPS` に次の1行だけを追加してください。すでに追加済みなら重複させません。

```python
'django.contrib.sitemaps',
```

`DATABASES`、`SECRET_KEY`、`ALLOWED_HOSTS`、ログ設定などは既存の本番設定を維持します。

1. 上記の設定差分と、その他のアプリケーションファイル・CSSを本番へ反映し、既存の運用手順でuWSGIを再読み込み・再起動します。この変更のためのDBマイグレーションは不要です。
2. 次のURLがログインせずにHTTP 200で開けることを確認します。
   - https://sigma-se.com/sitemap/
   - https://sigma-se.com/sitemap.xml
   - https://sigma-se.com/robots.txt
3. Nginxなどで既存の `robots.txt` を別途配信している場合は、`Sitemap: https://sigma-se.com/sitemap.xml` の記載を反映します。
4. [Google Search Console](https://search.google.com/search-console) で `sigma-se.com` の所有権確認済みプロパティを開き、「サイトマップ」に `https://sigma-se.com/sitemap.xml` を送信します。URLプレフィックスのプロパティで入力欄の先頭が補完される場合は `sitemap.xml` を入力します。
5. 送信結果と読み取りエラーを確認します。以後の記事追加・公開取り消し・更新はXMLに自動反映されるため、記事を追加するたびの再送信は不要です。

Search Consoleへの送信は本番での公開後に行います。コードを配置しただけでは、Search Consoleへの送信やインデックス登録は完了しません。

参考：[Googleのサイトマップ作成ガイド](https://developers.google.com/search/docs/crawling-indexing/sitemaps/build-sitemap?hl=ja)、[Djangoのサイトマップ機能](https://docs.djangoproject.com/en/4.2/ref/contrib/sitemaps/)

## DBのパスワード認証エラーで500になる場合

ログに `OperationalError` と「ユーザのパスワード認証に失敗しました」が出る場合は、Djangoが使用している接続情報でPostgreSQLへ認証できていません。設定ファイルを置き換えた直後なら、変更前の本番設定と `DATABASES` の内容を照合します。

1. サーバーの `/var/www/projs/sweb/config/settings.py` を編集し、`DATABASES['default']` の接続先・DB名・ユーザー名・パスワードを正しい本番設定へ戻します。パスワードをチャットや公開リポジトリへ貼り付ける必要はありません。
2. 元の設定ファイル全体を復元した場合は、`INSTALLED_APPS` に `'django.contrib.sitemaps'` があることも確認します。
3. uWSGIと同じ実行ユーザー・仮想環境で、次の接続確認を行います。接続情報そのものは出力しません。

   ```sh
   /var/www/venvs/sweb/bin/python -B /var/www/projs/sweb/manage.py shell --settings=config.settings -c "from django.db import connection; connection.ensure_connection(); print('DB接続OK')"
   ```

4. `DB接続OK` を確認したら、既存の運用手順でuWSGIを再読み込み・再起動し、トップページと両サイトマップを再確認します。

## テスト

DjangoとPillowをインストールした環境で実行します。本番DBや本番ログファイルには接続しません。

```sh
python manage.py test tblog --settings=config.test_settings
```
