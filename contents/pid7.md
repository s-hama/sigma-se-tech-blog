## タイトル
Python - 開発向けVim設定：インデント・PEP8・コードチェック

## 概要

Python開発で使うVimのインデント設定とflake8によるコードチェックを整理する。

設定ファイルの置き場所だけでなく、実際に有効な設定とその読み込み元を確認する。コードチェックでは未使用のimportと未定義名を含む小さなファイルを使い、行・列・エラーコードから修正箇所を特定する。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [Vimの共通設定](#vimの共通設定)<br>
  ファイルタイプ別の設定とインデントを有効にする。
- [Python用のVim設定](#python用のvim設定)<br>
  Python用の設定を作り、有効な値と読み込み元を確認。
- [コードチェックツールのインストール](#コードチェックツールのインストール)<br>
  利用するPythonとflake8の実行環境をそろえる。
- [コードチェックの一例](#コードチェックの一例)<br>
  警告の行・列・コードを読み、修正前後を比較。

## 対象環境と利用上の注意

- 本文記載時の環境<br>
Vimの`ftplugin`とPython向けのflake8を利用する、Unix系OSの設定例。<br>
Vim・Python・flake8の特定バージョンには固定していない。
- 確認時期<br>
2026年9月に公式資料と照合。Vim 9.1では一時ディレクトリの設定を読み込み、インデント設定と保存時の行末空白除去を確認。<br>
コードチェックの比較例はPython 3.12.2・flake8 7.4.1で確認。
- 現在そのまま利用できない箇所<br>
警告内容や設定の推奨値はツールのバージョンとプロジェクト規約で変わる。<br>
行長などは掲載値を固定的に採用せず、利用中のツールとチームの規約へ合わせる。

## 作業時の注意点

- filetype設定<br>
Python用設定が読み込まれない場合はディレクトリやファイル名を確認。
- タブとスペース<br>
混在するとインデントエラーや読みにくさにつながる。
- flake8の警告<br>
行番号、列番号、エラーコードの順に読む。
- プラグイン追加<br>
最初から入れすぎず、必要なチェックから増やす。

## 実施内容
### Vimの共通設定

- `.vimrc`でファイルタイプ別の設定を有効にする<br>
  ホームディレクトリの`.vimrc`へ次のVim scriptを記述する。すでに同じ設定があれば重複して追加する必要はない。

  ```vim
  " ファイルタイプの判定・専用設定・インデントを有効にする
  filetype plugin indent on
  " シンタックスハイライトを有効にする
  syntax on
  ```

  従来のVim scriptではコメントに`"`を使う。シェルのコマンドやPythonコードで使う`#`とは区別する。

### Python用のVim設定

- ファイルタイプ専用の設定を作る<br>
  次のコマンドをシェルで実行し、`~/.vim/ftplugin/python.vim`を編集する。

  ```bash
  mkdir -p ~/.vim/ftplugin
  touch ~/.vim/ftplugin/python.vim
  ```

  `python.vim`には次のVim scriptを記述する。

  ```vim
  " Tabキー入力などで使うインデントをスペース4つにそろえる
  setlocal expandtab
  setlocal tabstop=4
  setlocal shiftwidth=4
  setlocal softtabstop=4
  " 自動折り返しの幅
  setlocal textwidth=79

  " このバッファの保存時に行末の空白を除去する
  augroup sigma_python_whitespace
      autocmd! * <buffer>
      autocmd BufWritePre <buffer> %s/\s\+$//e
  augroup END
  ```

  `expandtab`は新たに入力するタブをスペースへ置き換える設定であり、ファイル内の既存タブを一括変換するものではない。保存時の置換は複数行文字列の末尾にも作用するため、末尾空白をデータとして保持するコードでは自動除去の設定を外す。

  PEP 8ではインデントをスペース4つ、コードを原則79文字以内、コメントとdocstringを72文字以内としている。チームで合意した場合はコードを99文字まで広げる選択肢もあるため、行長はプロジェクトの規約を優先する。この設定だけでPEP 8のすべてに準拠するわけではない。

- 設定したのに反映されない場合の確認順序<br>
  `.py`ファイルを開き直し、Vimのコマンドラインで順に確認する。

  ```vim
  :set filetype?
  :setlocal expandtab? tabstop? shiftwidth? softtabstop? textwidth?
  :verbose setlocal shiftwidth?
  :scriptnames
  ```

  この設定が有効なら`filetype=python`、`expandtab`、`tabstop=4`、`shiftwidth=4`、`softtabstop=4`、`textwidth=79`を確認できる。

  まず`filetype`がpythonかを調べる。次に各設定値を読み、想定と違う値があれば`verbose`で最後に設定したファイルと行を確認する。`scriptnames`には読み込まれたスクリプトが表示されるので、専用設定が未読なのか、後から別の設定で上書きされたのかを分けて調べられる。Python用設定が未読なら共通設定とファイル名・配置先を確認する。

### コードチェックツールのインストール
- **flake8**のインストール<br>
Pythonで多く使用されているコードチェックツール**flake8**をインストール。<br>
flake8は、pyflakes、pycodestyle、mccabeを組み合わせて、論理的な誤り、コーディングスタイル、循環的複雑度を確認できる。インストールされるバージョンはPython環境によって異なるため、`python -m flake8 --version`で確認。<br>
  ```bash
  $ python -m pip install flake8
  $ python -m flake8 --version
  ```

### コードチェックの一例
- 小さなファイルで指摘と修正を対応させる<br>
  次の5行を`lint_example.py`として保存する。未使用のimportと変数名の取り違えを含む確認用のコードである。

  ```python
  import os


  def total(prices):
      return sum(price)
  ```

  ```bash
  python -m flake8 --isolated lint_example.py
  ```

  ```text
  lint_example.py:1:1: F401 'os' imported but unused
  lint_example.py:5:16: F821 undefined name 'price'
  ```

  `--isolated`は既存のflake8設定ファイルの影響を避けてこの例を試すための指定である。通常のプロジェクトではプロジェクト側の設定に従う。

  1件目は1行目1列目のimportが未使用という指摘で、2件目は5行目16列目の`price`が未定義という指摘になる。引数名は`prices`なので次のように直す。

  ```python
  def total(prices):
      return sum(prices)


  print(total([100, 200, 300]))
  ```

  同じflake8コマンドを再実行すると指摘がなくなり、`python lint_example.py`では`600`を表示する。チェックを通ることと計算結果が正しいことは別なので、入力と期待値でも確認する。論理的な計算ミスを追う方法は[Pdbの記事](https://sigma-se.com/detail/9/)で扱う。

以下、**flake8**、**pyflakes**、**pycodestyle**、**mccabe**の一例。
- **flake8** : コードチェック<br>
  ```bash
  $ flake8 example.py
   example.py:11:1: E302 expected 2 blank lines, found 1
   example.py:12:21: W291 trailing whitespace
  …
  ```

- **pyflakes** : コードチェック<br>
  ```bash
  $ pyflakes example.py
   example.py:74: undefined name 'Http404'
  …
  ```

- **pycodestyle** : PEP8に準拠しているかチェック<br>
  ```bash
  $ pycodestyle example.py
   example.py:10:1: W293 blank line contains whitespace
   example.py:11:1: E302 expected 2 blank lines, found 1
   example.py:12:21: W291 trailing whitespace
  …
  ```

- **mccabe** : 循環的複雑度のチェック<br>
  **flake8**ではデフォルト無効になっているため、下記のように `--max-complexity`を指定すれば循環的複雑度のチェックが可能となる。<br>
  ```bash
  $ flake8 --max-complexity 10 coolproject
    ...
    coolproject/mod.py:1204:1: C901 'CoolFactory.prepare' is too complex (14)
  ```

その他、**flake8**には、**flake8-docstrings**や**flake8-import-order**など色々なプラグインが用意されており、必要に応じてカスタマイズすることができる。

## まとめ

- Python用設定が効かない場合はfiletype、有効な設定値、最後に設定したスクリプトの順に確認する。
- expandtabなどの入力設定と既存ファイルのタブ・空白は区別する。保存時の空白除去も文字列データへの影響を確認して使う。
- flake8の指摘はファイル・行・列・コードから読み、修正後に再実行する。計算の正しさは具体的な入力と期待値でも確認する。

### 参考文献
- [Python ドキュメント「間奏曲：コーディングスタイル」（日本語・PEP 8の要点をまとめた公式解説）](https://docs.python.org/ja/3/tutorial/controlflow.html#intermezzo-coding-style)
- [Python Enhancement Proposals, PEP 8：Style Guide for Python Code（英語・Pythonコーディング規約原文）](https://peps.python.org/pep-0008/)
- [Vim Reference Manual, filetype.txt（英語・ファイルタイプ設定仕様）](https://github.com/vim/vim/blob/master/runtime/doc/filetype.txt)
- [Flake8 Documentation, Using Flake8（英語・コードチェック公式手順）](https://flake8.pycqa.org/en/latest/user/index.html)
- [PyCQA, mccabe（英語・複雑度チェック実装元）](https://github.com/PyCQA/mccabe)
