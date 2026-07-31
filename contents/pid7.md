## タイトル
Python - 開発向けVim設定：インデント・PEP8・コードチェック

## 概要

Python開発で使うVimの基本設定と、flake8などのコードチェックツールの使い方を整理する。

Pythonではインデントが構文に影響するため、エディタ設定は見た目だけでなく実行結果にも関係する。<br>Vimのファイルタイプ別設定とコードチェックを組み合わせることで、保存前後のミスを見つけやすくなる。

## この記事で扱うこと
- .vimrcで共通設定を行う方法。
- Python専用のftplugin設定を分ける方法。
- PEP 8を参考にしたインデントと行幅の考え方。
- flake8、pyflakes、pycodestyle、mccabeの役割。
- コードチェック結果の読み方。

## 作業時の注意点

- filetype設定<br>
Python用設定が読み込まれない場合はディレクトリやファイル名を確認する。
- タブとスペース<br>
混在するとインデントエラーや読みにくさにつながる。
- flake8の警告<br>
行番号、列番号、エラーコードの順に読む。
- プラグイン追加<br>
最初から入れすぎず、必要なチェックから増やす。

## 実施内容
### Vimの共通設定
- ホームディレクトリに`.vimrc`ファイルを作成<br>
`.vimrc`に設定を追記することでVimに反映される。<br>
  ```bash
  touch ~/.vimrc
  ```

- Pythonを使う上で最低限必要な**自動インデント**と**シンタックスハイライト**のみ設定<br>
  ```bash
  $ vim ~/.vimrc
   filetype plugin indent on    # 自動インデントの設定
   syntax on    # シンタックスハイライトの設定
  ```

### Python用のVim設定
- ホームディレクトリに`.vim/ftplugin/python.vim`ファイルを作成<br>
設定ファイルをファイルタイプ別に分割できるため、Pythonスクリプト専用の設定を定義することができる。<br>
  ```bash
  $ mkdir -p ~/.vim/ftplugin
  $ touch ~/.vim/ftplugin/python.vim
  ```

- Vimの設定を追記<br>
下記は、**PEP 8**が示す「1段につきスペース4つ」「コードは原則79文字以内」という基本に合わせた設定例となる。これだけでPEP 8のすべてへ準拠するわけではなく、行長などの方針はプロジェクトの規約を優先する。<br>
  ```bash
  $ vim ~/.vim/ftplugin/python.vim
   setlocal expandtab    # タブをスペースに置き換える設定
   setlocal tabstop=4    # タブのインデント幅を4に設定
   setlocal shiftwidth=4    # 自動インデント時の幅を4に設定
   setlocal softtabstop=4    # Tabキー入力時の幅を4に設定
   autocmd BufWritePre <buffer> %s/\s\+$//e    # このバッファの保存時に行末スペースを除去
   setlocal textwidth=79    # 自動折り返しの幅を79文字に設定
  ```
  PEP 8ではコードを原則79文字以内、コメントとdocstringを72文字以内としている。一方、チームで合意している場合はコードを99文字まで広げる選択肢も示されているため、`textwidth`やflake8の設定は開発ルールに合わせる。

### コードチェックツールのインストール
- **flake8**のインストール<br>
Pythonで多く使用されているコードチェックツール**flake8**をインストールする。<br>
flake8は、pyflakes、pycodestyle、mccabeを組み合わせて、論理的な誤り、コーディングスタイル、循環的複雑度を確認できる。インストールされるバージョンはPython環境によって異なるため、`flake8 --version`で確認する。<br>
  ```bash
  $ python -m pip install flake8
  $ flake8 --version
  ```

### コードチェックの一例
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
<br>
その他、**flake8**には、**flake8-docstrings**や**flake8-import-order**など色々なプラグインが用意されており、必要に応じてカスタマイズすることができる。

## まとめ
- Python開発では、Vimのインデント設定がコード品質に直結する。
- flake8を使うと、コーディングスタイルや未定義名を確認でき、`--max-complexity`を指定すれば複雑度も検査できる。
- まずは最小限の設定から始め、必要に応じてチェックを増やすと扱いやすい。

### 参考文献
- [Python ドキュメント「間奏曲：コーディングスタイル」（日本語・PEP 8の要点をまとめた公式解説）](https://docs.python.org/ja/3/tutorial/controlflow.html#intermezzo-coding-style)
- [Python Enhancement Proposals, PEP 8：Style Guide for Python Code（英語・Pythonコーディング規約原文）](https://peps.python.org/pep-0008/)
- [Vim Reference Manual, filetype.txt（英語・ファイルタイプ設定仕様）](https://github.com/vim/vim/blob/master/runtime/doc/filetype.txt)
- [Flake8 Documentation, Using Flake8（英語・コードチェック公式手順）](https://flake8.pycqa.org/en/latest/user/index.html)
- [PyCQA, mccabe（英語・複雑度チェック実装元）](https://github.com/PyCQA/mccabe)
