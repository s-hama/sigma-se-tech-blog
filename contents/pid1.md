## タイトル
VPSで作るDjangoサイト構築手順 (Apache＆PostgreSQL編)：[1] ドメイン＆SSHの初期設定

## 目的
本記事では、以下のVPS環境でDjangoサイトを構築するために必要な「ドメインとSSHの初期設定手順」を説明する
- OS：CentOS
- 言語：Python
- WEBサーバー：Apache
- FW：Django
- DB：PostgresSQL

## 実施内容
### VPS契約
- 価格に見合ったスペック（容量、メモリ、CPUなど）、安全性、操作性など、何を重視するかの基準を決めてVPSを選ぶ
- この記事では、コストパフォーマンスとサポートの充実、プラン変更の柔軟性に基準を置き「さくらのVPS」で契約

### OSインストール
- 開発環境(Apache, Django, PostgreSQL)がインストール可能なOSを選ぶ
- この記事では、英語圏のコミュニティが大きく、日本語情報が豊富で個人的に使い慣れているCentOSを選んだ
- CentOS7_x64_x84(標準)をインストール
インストールはSAKURA VPS管理者用のコントロールパネルからGUI操作でインストールする
```
$ cat /etc/redhat-release
CentOS Linux release 7.4.1708 (Core)
```
