## タイトル
Python - タスク指向型対話：2/5 OpenWeatherMap・Telegramの環境準備

## 概要
状態遷移ベースの天気案内Botで使用するOpenWeatherMap、Telegram、python-telegram-botの準備手順を整理する。
天気案内Botでは、天気情報を外部APIから取得し、ユーザーとのやり取りをメッセンジャー上で行う必要がある。OpenWeatherMapは天気情報の取得、Telegramはユーザーとの対話画面、python-telegram-botはBot実装の接続部分を担当する。
ここでは、API利用登録、Bot作成、ライブラリのインストール、オウム返しBotによる疎通確認までを扱う。

## この記事の構成
- [対象環境と利用上の注意](#対象環境と利用上の注意)<br>
  本文記載時の環境と現在そのまま利用できない箇所を確認。
- [作業時の注意点](#作業時の注意点)<br>
  設定変更やコマンド実行前に確認しておきたい注意点を整理。
- [天気情報を取得する「OpenWeatherMap」WebAPIの概要と利用登録](#天気情報を取得するopenweathermapwebapiの概要と利用登録)<br>
  天気情報を取得する「OpenWeatherMap」WebAPIの概要と利用登録の手順と確認ポイントを整理。
- [メッセンジャーアプリ「Telegram」の利用登録と「python-telegram-bot」のインストール](#メッセンジャーアプリtelegramの利用登録とpython-telegram-botのインストール)<br>
  メッセンジャーアプリ「Telegram」の利用登録と「python-telegram-bot」のインストールの手順と確認ポイントを整理。
- [TelegramBotを使用した対話サンプル（オウム返し）](#telegrambotを使用した対話サンプルオウム返し)<br>
  TelegramBotを使用した対話サンプル（オウム返し）の意味と要点を具体例から整理。

## 対象環境と利用上の注意
- 本文記載時の環境<br>
2020年7月時点のOpenWeatherMap APIと、python-telegram-bot \\(12.8\\)の同期APIを使った手順。
- 確認時期<br>
2026年8月にTelegram Bot API、python-telegram-bot、OpenWeatherMapの公式資料と照合し、記載内容を見直した。
- 現在そのまま利用できない箇所<br>
掲載コード全体は現行サービス・ライブラリで再実行していない。<br>
料金、呼出し上限、登録画面、APIレスポンスは変更され得る。<br>
現行のpython-telegram-botは掲載コードとAPIが異なるため、旧コードをそのまま新規利用せず、利用する版を固定して公式サンプルへ合わせる。

## 作業時の注意点
- APIキーとBotトークン<br>
コードに直書きすると漏えいリスクがあるため、環境変数や設定ファイルで管理。
- 疎通確認の順番<br>
天気APIとTelegram Botを別々に確認してから結合すると原因を切り分けやすい。
- ライブラリのバージョン<br>
python-telegram-botはバージョンで書き方が変わるため、記事のコードと環境を合わせる。

## 解説と実装サンプル

### 天気情報を取得する「OpenWeatherMap」WebAPIの概要と利用登録
- 天気APIの準備と疎通確認<br>
    天気情報は、無償で天気情報を取得できる`OpenWeatherMap`のWebAPIを用いて取得する。<br>
    下記トップページにアクセスすると`GUI`でも天気情報を確認することができる。

    【OpenWeatherMap】: https://openweathermap.org/<br>

    本文記載時はFreeプランで毎分60回までの呼出しと、3時間ごとの5日予報を利用できた。料金、呼出し上限、利用できるAPIは変更されるため、実装時はOpenWeatherMap公式の料金・APIページで現行条件を確認する。<br>
    そして、APIをコールするには、`API Key`が必要でアカウント作成する必要がある。

    - OpenWeatherMapのアカウント作成<br>
        下記のアカウント作成ページ【Create New Account】を開き、`Username`、`Enter email`、`Password`、`Repeat password`を入力し、「Create Account」ボタンクリックでアカウントを作成。

        【Create New Account】: https://home.openweathermap.org/users/sign_up

        アカウント作成後、ログインした状態で下記のAPIKey確認ページ【api_keys】開くと`Key`欄にAPIKeyが表示されるので、ここからAPIKeyを確認。<br>
        ※ 登録完了のメール本文でもAPIKeyを確認できる。

        【api_keys】: https://home.openweathermap.org/api_keys

        また、PythonからURLへアクセスするため、サードパーティライブラリである`Requests`が必要。<br>
        ※ 標準ライブラリ`urllib`でもアクセスできるが、`Requests`の方がシンプルであるため、これを使用。

    - Requestsのインストール
        ```bash
        $ pip3 install requests
        ```

        以上で`OpenWeatherMap`APIを呼ぶ準備が完了。<br>
        以下、準備されている2つのAPI**現在の天気情報**と**天気予報**の呼出確認となる。

    - 呼出し確認（現在の天気情報）<br>
        福岡県（県庁）の緯度、経度を指定して現在の天気情報（JSON）を取得。<br>
        ※ API呼出しの`units=metric`は、気温を摂氏で取得する指定とする。
        ```python
        $ python
            >>> import requests
            >>>
            >>> # 福岡県（県庁）の緯度、経度
            >>> lat = 33.60
            >>> lon = 130.41
            >>>
            >>> # 自アカウントのAPIKey
            >>> appid = '**********'
            >>>
            >>> # 現在の天気情報
            >>> current_weather_url = 'https://api.openweathermap.org/data/2.5/weather'
            >>>
            >>> # API呼出し
            >>> response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(current_weather_url,lat,lon,appid))
            >>>
            >>> # 結果出力
            >>> response.json()
            {'coord': {'lon': 130.41, 'lat': 33.6}, 'weather': [{'id': 803, 'main': 'Clouds', 'description': '曇りがち', 'icon': '04n'}], 'base': 'stations', 'main': {'temp': 25.87, 'feels_like': 29.51, 'temp_min': 24.44, 'temp_max': 27.78, 'pressure': 1010, 'humidity': 83}, 'visibility': 10000, 'wind': {'speed': 2.1, 'deg': 290}, 'clouds': {'all': 75}, 'dt': 1595079741, 'sys': {'type': 1, 'id': 7998, 'country': 'JP', 'sunrise': 1595017250, 'sunset': 1595068076}, 'timezone': 32400, 'id': 1863967, 'name': '福岡市', 'cod': 200}
            >>>
        ```

    - 呼出し確認（天気予報）
        上記と同じ、福岡県（県庁）の緯度、経度を指定して天気予報を取得。<br>
        ※ `list`配列に3時間毎の天気予報（JSON）が格納されいる。<br>
        （＊1）4つ目以降の`list`配列は割愛
        ```python
        $ python
            >>> import requests
            >>>
            >>> # 福岡県（県庁）の緯度、経度
            >>> lat = 33.60
            >>> lon = 130.41
            >>>
            >>> # 自アカウントのAPIKey
            >>> appid = '**********'
            >>>
            >>> # 明日以降の天気情報
            >>> forecast_url = 'https://api.openweathermap.org/data/2.5/forecast'
            >>>
            >>> # API呼出し
            response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(forecast_url,lat,lon,appid))
            >>>
            >>> # 結果出力
            >>> response.json()["list"][0]
            {'dt': 1595084400, 'main': {'temp': 24.97, 'feels_like': 28.68, 'temp_min': 24.37, 'temp_max': 24.97, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 1009, 'humidity': 79, 'temp_kf': 0.6}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': '厚い雲', 'icon': '04n'}], 'clouds': {'all': 100}, 'wind': {'speed': 0.72, 'deg': 54}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2020-07-18 15:00:00'}
            >>>
            >>> response.json()["list"][1]
            {'dt': 1595095200, 'main': {'temp': 24.65, 'feels_like': 27.75, 'temp_min': 24.41, 'temp_max': 24.65, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 1009, 'humidity': 75, 'temp_kf': 0.24}, 'weather': [{'id': 804, 'main': 'Clouds', 'description': '厚い雲', 'icon': '04n'}], 'clouds': {'all': 100}, 'wind': {'speed': 0.79, 'deg': 157}, 'visibility': 10000, 'pop': 0, 'sys': {'pod': 'n'}, 'dt_txt': '2020-07-18 18:00:00'}
            >>>
            >>> response.json()["list"][2]
            {'dt': 1595106000, 'main': {'temp': 24.47, 'feels_like': 26.82, 'temp_min': 24.4, 'temp_max': 24.47, 'pressure': 1010, 'sea_level': 1010, 'grnd_level': 1009, 'humidity': 75, 'temp_kf': 0.07}, 'weather': [{'id': 500, 'main': 'Rain', 'description': '小雨', 'icon': '10d'}], 'clouds': {'all': 100}, 'wind': {'speed': 1.75, 'deg': 161}, 'visibility': 10000, 'pop': 0.54, 'rain': {'3h': 0.25}, 'sys': {'pod': 'd'}, 'dt_txt': '2020-07-18 21:00:00'}
            >>>
        ```

### メッセンジャーアプリ「Telegram」の利用登録と「python-telegram-bot」のインストール
- Telegram Botの準備<br>
    最後に対話で使用するメッセンジャーアプリ`Telegram`の利用登録（アカウント作成）とPythonから`Telegram`を認識できるようにするためのライブラリである`python-telegram-bot`をインストールする。

    - Telegramインストーラのダウンロードとアカウント作成<br>
        下記のTelegramトップページ【Telegram Top】を開き、インストール端末に応じたインストーラを選択し、ダウンロード。<br>
        ※ Windowsなら「Telegram for Pc/Mac/Linux」リンク →「Get Telegram for Windows」ボタンでダウンロード。<br>
        ※ Linuxなら「Telegram for Pc/Mac/Linux」リンク →「Show all platforms」リンク→「Get Telegram for Linux 64 bit」ボタンでダウンロード。

        【Telegram Top】: https://telegram.org

        続いて、ダウンロードしたインストーラを実行後、Telegramを起動し、アカウント作成を行う。<br>
        ※ 国番号を付加した電話番号を入力後、SMS確認コードの本人確認が必要。

    - スクリーンネームの登録とアクセストークンの取得<br>
        新しいBotの作成とスクリーンネームの登録を行い、アクセストークンを取得。

        アカウント作成後、左サイドメニュー上部のユーザー検索欄から「@BotFather」で検索し、「Start」ボタンクリックで「@BotFather」と対話できる状態にする。

        以降は、下記のように**Bot名**の入力と**スクリーンネーム**を登録し、アクセストークンを取得。

        - Bot名の入力（Botの新規作成）<br>
            「Alright, a new bot. How are we going to call it? Please choose a name for your bot.」と表示されるので、任意のBot名を入力。<br>
            ※ 下記サンプルでは「SHamaBot 」と入力している。

        - スクリーンネームの登録<br>
            「Good. Now let's choose a username for your bot. It must end in `bot`. Like this, for example: TetrisBot or tetris_bot.」<br>と表示されるので、末尾が`bot`で終わるスクリーンネームを入力。（既に使用されているスクリーンネームは使用不可。）

            ※ 下記サンプルでは、Bot名と同じ「SHamaBot 」で入力したところ、既に使用されているスクリーンネームであったため「sorry this username is already taken. please try something different」とエラーが出ている。<br>
            そのため「GSHamaBot」の再入力で登録している。

        - アクセストークンの取得<br>
            スクリーンネームの登録後、「Use this token to access the HTTP API:」の直後にアクセストークンが表示される。

            ※ このアクセストークンが**Telegramクライアント**（Telegramをインストールした端末）と**Pythonの対話システム**が**Telegramのサーバー**を介して互いに連携するための`Key`となる。

            ![pid40_1](/static/tblog/img/pid40_1.png)

    - 「python-telegram-bot」のインストール<br>
        掲載コードは旧版 \\(12.8\\) のAPIを使うため、再現する場合は隔離した仮想環境で版を固定する。新規実装では現行版の公式サンプルを使用する。
        ```bash
        $ pip3 install 'python-telegram-bot==12.8'
        ```

### TelegramBotを使用した対話サンプル（オウム返し）
- オウム返しBotの実装と確認<br>
    下記の（＊1）、（＊2）が上記で登録した`@GSHamaBot`のレスポンスをPythonでオウム返しする実装サンプルで、（＊1）のTelegramBotクラスは、GSHamaBot（Telegramサーバー側）との**通信処理**で、（＊2）のEchoSystemクラスは、Botが応答する内容の**制御処理**となる。

    - （＊1）TelegramBotクラス（telegram_bot.py）<br>
        ※ 実行前にアクセストークンを環境変数`TELEGRAM_BOT_TOKEN`へ設定する。ソースコードへ直書きしない。
        ```python
        import os
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

        # アクセストークンは環境変数から取得
        TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]

        class TelegramBot:
            def __init__(self, system):
                self.system = system

            def start(self, bot, update):
                # 辞書型 inputにユーザIDを設定
                input = {'utt': None, 'sessionId': str(update.message.from_user.id)}

                # システムからの最初の発話をinitial_messageから取得し，送信
                update.message.reply_text(self.system.initial_message(input)["utt"])

            def message(self, bot, update):
                # 辞書型 inputにユーザからの発話とユーザIDを設定
                input = {'utt': update.message.text, 'sessionId': str(update.message.from_user.id)}

                # replyメソッドによりinputから発話を生成
                system_output = self.system.reply(input)

                # 発話を送信
                update.message.reply_text(system_output["utt"])

            def run(self):
                updater = Updater(TOKEN)
                dp = updater.dispatcher
                dp.add_handler(CommandHandler("start", self.start))
                dp.add_handler(MessageHandler(Filters.text, self.message))
                updater.start_polling()
                updater.idle()
        ```

    - （＊2）EchoSystemクラス（echo_system.py）<br>
        ```python
        from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
        from telegram_bot import TelegramBot

        # ユーザの入力をそのまま返す対話システム．
        class EchoSystem:
            def __init__(self):
                pass

            def initial_message(self, input):
                return {'utt': 'こんにちは。対話を始めましょう。', 'end':False}

            def reply(self, input):
                return {"utt": input['utt'], "end": False}

        if __name__ == '__main__':
            system = EchoSystem()
            bot = TelegramBot(system)
            bot.run()
        ```

      - 以下、実行順に処理の流れを解説
        - まず、（＊2）EchoSystemクラス（echo_system.py）を実行
        - （＊2）EchoSystemクラスのメイン処理で自身のインスタンスをTelegramBotクラスのコンストラクタに渡し、（＊1）TelegramBotクラスの runメソッド をコール
        - （＊1）TelegramBotクラスの runメソッドでは、telegramサーバー側のUpdater関数にてアクセストークンを設定後、自身のstartメソッドをコマンドハンドラとして、messageメソッドをメッセージハンドラとして設定し、コマンドハンドラとメッセージハンドラの受付を開始（待機状態）
        - Telegramクライアントで「start」ボタンをクリックするとTelegramサーバーがstartコマンドを発行し、上記で設定（待機）していたコマンドハンドラを受付け、startメソッドが実行される
        - startメソッドでは、まずユーザーの発話情報を保持する input(dict型) オブジェクトを定義し、uttは発話内容、 sessionIdはセッションIDを格納<br>
            ※ Telegramの対話はすべて、システム側（Bot側）の発話から始まるため、utt（発話内容）は None を設定し、sessionIdには、ユーザーのセッションIDを設定している。
        - 次に initial_message でBotの初回発話内容を取得後、Telegramサーバー側の reply_text メソッドをコールし、Botの発話内容（ 'utt': 'こんにちは。対話を始めましょう。' ）を送信
            ※ initial_messageの戻り値dict型のendは、対話の完了フラグ（True:完了、False:継続）<br>
        - その後、ユーザーがTelegramクライアントから発話すると、上記で設定（待機）していたメッセージハンドラを受付け、messageメソッドが実行される
        - messageメソッドでは、まずユーザーの発話内容（Telegramサーバー側の text から取得したutt（発話内容））とユーザーのセッションIDでユーザー発話情報inputを定義
        続けて reply メソッドで発話内容を取得後（＊1）、Telegramサーバー側の reply_text メソッドに発信内容を渡して送信。<br>
            （＊1）発話内容は、オウム返し するため、引数の発話内容 input['utt'] をそのまま返している。


    - 上記「対話サンプル (オウム返し)」の実行確認<br>
        以下、(1)、(2)の実行確認結果。<br>
        ※「telegram_bot.py」のアクセストークン(TOKEN)を、自身のものに置き換えることを忘れずに。

        「echo_system.py」の実行にて対話を開始。
        ```python
        $ python ~/gitlocalrep/dsbook/echo_system.py
        /root/gitlocalrep/dsbook/telegram_bot.py:29: TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/fxJuV for details
        updater = Updater(TOKEN)
        ```

        上記コンソールが実行中の状態。

        ↓ ユーザーの入力をすべてオウム返しする。<br>
        ※ 対話(オウム返し)を終了する場合は「Ctrl + C」で終了。<br>
        ![pid40_2](/static/tblog/img/pid40_2.png)

## まとめ
- OpenWeatherMapは天気情報取得、Telegramは対話インターフェースとして使う。
- python-telegram-botを使うと、PythonからTelegram Botを実装できる。
- 本格実装の前に、APIとBotの疎通確認を分けて行うと安全。

### 参考文献
- 東中 竜一郎、稲葉 通将、水上 雅博（\\(2020\\)）『Pythonでつくる対話システム』株式会社オーム社
- [OpenWeather - Current weather data（英語・現在天気APIの公式仕様）](https://openweathermap.org/api/current)
- [OpenWeather - 5 day weather forecast（英語・予報APIの公式仕様）](https://openweathermap.org/api/forecast5)
- [Telegram - Bot API（英語・Bot APIの公式仕様）](https://core.telegram.org/bots/api)
- [python-telegram-bot 12.8 公式ドキュメント（英語・記事で使用する旧版APIの仕様）](https://docs.python-telegram-bot.org/en/v12.8/)
