## タイトル
VPSで作るDjangoサイト構築手順 (Apache＆PostgreSQL編)：[1/3] ドメイン＆SSHの初期設定

## この記事の目的
下記VPS環境下でDjangoサイトを構築するため、ドメインとSSHの初期設定手順を説明する
```
OS：CentOS
言語：Python
WEBサーバー：Apache
FW：Django
DB：PostgresSQL
```

## やったこと
### VPS契約
- 価格に見合ったスペック（容量、メモリ、CPUなど）、安全性、操作性など、何を重視するかの基準を決めてVPSを選ぶ
- この記事では、コストパフォーマンスとサポートの充実、プラン変更の柔軟性に基準を置き「さくらのVPS」で契約
