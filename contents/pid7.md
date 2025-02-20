## タイトル
Python - 開発向けVim設定 : 基礎からコードチェックまで

## 目的
この記事では、Python開発向けのVim設定とコードチェックの手順について説明する。

## 実施内容
### Vimの共通設定
- ホームディレクトリに`.vimrc`ファイルを作成<br>
`.vimrc`に設定を追記することでVim に反映される。<br>
  ```bash
  touch ~/.vimrc
  ```

- Pythonを使う上で最低限必要な**自動インデント**と**シンタックスハイライト**のみ設定<br>
  ```bash
  $ vim ~/.vimrc
   filetype plugin indenton    # 自動インデントの設定
   syntax on    # シンタックスハイライトの設定
  ```

### Python用のVim設定
- ホームディレクトリに`.vim/ftplugin/python.vim`ファイルを作成<br>
設定ファイルをファイルタイプ別に分割できるため、Pythonスクリプト専用の設定を定義することができる。<br>
  ```bash
  $ mkdir ~/.vim
  $ mkdir ~/.vim/ftplugin
  $ touch ~/.vim/ftplugin/python.vim
  ```

- Vimの設定を追記<br>
下記は、Pythonコミュニティが推奨する**PEP8 ※1, 2：コーディング規約**に準拠した設定となる。<br>
※1 PEP8（en） : https://www.python.org/dev/peps/pep-0008/<br>
※2 PEP8（ja） : https://github.com/mumumu/pep8-ja<br>
  ```bash
  $ vim ~/.vim/ftplugin/python.vim
   setlocal expandtab    # タブをスペースに置き換える設定
   setlocal tabstop=4    # タブのインデント幅を4に設定
   setlocal shiftwidth=4    # 自動インデント時の幅を4に設定
   setlocal softtabstop=0    # キーボードから入るタブの数
   autocmd BufWritePre * :%s/\s\+$//ge    # 保存時、行末スペースを除去する
   setlocal textwidth=80    # 行折り返しを80文字に設定
  ```

### コードチェックツールのインストール
- **flake8**のインストール<br>
Pythonで多く使用されているコードチェックツール**flake8**をインストールする。<br>
下記、`pip show flake8`のRequires(依存ライブラリ)にもある通り、flake8は、pyflakes、pycodestyle、mccabe 3つライブラリをラップしているため、それぞれ個別のチェックも可能。<br>
  ```bash
  $ pip install flake8
  $ pip show flake8
   Name: flake8
   Version: 3.6.0
   Summary: the modular source code checker: pep8, pyflakes and co
   Home-page: https://gitlab.com/pycqa/flake8
   Author: Tarek Ziade
   Author-email: tarek@ziade.org
   License: MIT
   Location: /var/www/vops/lib/python3.6/site-packages
   Requires: pycodestyle, setuptools, pyflakes, mccabe
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
  ※ 参考URLより抜粋 : https://github.com/pycqa/mccabe#plugin-for-flake8<br>
  ```bash
  $ flake8 --max-complexity 10 coolproject
    ...
    coolproject/mod.py:1204:1: C901 'CoolFactory.prepare' is too complex (14)
  ```
<br>
その他、**flake8**には、**flake8-docstrings**や**flake8-import-order**など色々なプラグインが用意されており、必要に応じてカスタマイズすることができる。
