## タイトル
Python - 開発向けVim設定 : 基礎からコードチェックまで

## 目的
この記事では、Python開発向けのVim設定とコードチェックの手順について説明する。

## 実施内容
### Vimの共通設定
- ホームディレクトリに`.vimrc`ファイルを作成<br>
`.vimrc`に設定を追記することでVim に反映される。<br>
  ```
  touch ~/.vimrc
  ```

- Pythonを使う上で最低限必要な**自動インデント**と**シンタックスハイライト**のみ設定<br>
  ```
  $ vim ~/.vimrc
   filetype plugin indenton    " 自動インデントの設定
   syntax on    " シンタックスハイライトの設定
  ```

### Python用のVim設定
- ホームディレクトリに`.vim/ftplugin/python.vim`ファイルを作成<br>
設定ファイルをファイルタイプ別に分割できるため、Pythonスクリプト専用の設定を定義することができる。<br>
  ```
  $ mkdir ~/.vim
  $ mkdir ~/.vim/ftplugin
  $ touch ~/.vim/ftplugin/python.vim
  ```

- Vimの設定を追記<br>
下記は、Pythonコミュニティが推奨する**PEP8 ※1, 2：コーディング規約**に準拠した設定となる。<br>
※1 PEP8（en） : https://www.python.org/dev/peps/pep-0008/<br>
※2 PEP8（ja） : https://github.com/mumumu/pep8-ja<br>
  ```
  $ vim ~/.vim/ftplugin/python.vim
   setlocal expandtab    " タブをスペースに置き換える設定
   setlocal tabstop=4    " タブのインデント幅を4に設定
   setlocal shiftwidth=4    " 自動インデント時の幅を4に設定
   setlocal softtabstop=0    " キーボードから入るタブの数
   autocmd BufWritePre * :%s/\s\+$//ge    " 保存時、行末スペースを除去する
   setlocal textwidth=80    " 行折り返しを80文字に設定
  ```

### コードチェックツールのインストール
- **flake8**のインストール<br>
Pythonで多く使用されているコードチェックツール**flake8**をインストールする。<br>
下記、`pip show flake8`のRequires(依存ライブラリ)にもある通り、flake8は、pyflakes、pycodestyle、mccabe 3つライブラリをラップしているため、それぞれ個別のチェックも可能。<br>
  ```
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
