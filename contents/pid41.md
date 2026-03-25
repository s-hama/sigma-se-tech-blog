## タイトル
Python - タスク指向型対話 : 天気情報案内 > 状態遷移ベースの実装

## 目的
この記事では、天気情報案内（状態遷移ベース）の実装と実行確認について記載する。

※ 学習用の簡易的なものであるため、地名の指定は都道府県のみ、取得範囲は今日か明日のみ、種別は天気と気温のみとする。

## 実装内容
### 状態遷移ベースの実装

先行ページで解説した文章解析の`MeCab`、状態遷移の`SCXML`、天気情報取得の`OpenWeatherMap`、メッセンジャーアプリの`Telegram`を使用して、タスク指向型の天気情報案内対話システムを実装する。

- SCXML (states.scxml)<br>
    以下、天気情報案内の状態遷移。

    ※ 各項目(状態)の解説については、下記先行ページを参照。<br>
    [Python - タスク指向型対話 : 状態遷移ベースの環境準備 > MeCab, SCXML > 状態遷移によるタスクを遂行する「SCXML」の概要とインストール](<https://sigma-se.com/detail/39/#:~:text=%E7%8A%B6%E6%85%8B%E9%81%B7%E7%A7%BB%E3%81%AB%E3%82%88%E3%82%8B%E3%82%BF%E3%82%B9%E3%82%AF%E3%82%92%E9%81%82%E8%A1%8C%E3%81%99%E3%82%8B%E3%80%8CSCXML%E3%80%8D%E3%81%AE%E6%A6%82%E8%A6%81%E3%81%A8%E3%82%A4%E3%83%B3%E3%82%B9%E3%83%88%E3%83%BC%E3%83%AB>)


    ```xml
    <?xml version="1.0" encoding="UTF-8"?>
    <scxml xmlns="http://www.w3.org/2005/07/scxml" version="1.0" initial="ask_place">
    <state id="ask_place">
        <transition event="place" target="ask_date"/>
    </state>
    <state id="ask_date">
        <transition event="date" target="ask_type"/>
    </state>
    <state id="ask_type">
        <transition event="type" target="tell_info"/>
    </state>
    <final id="tell_info"/>
    </scxml>
    ```

- WeatherSystemクラス (weather_system.py)<br>
    Telegramクライアントの発話内容を解析し、状態遷移に応じた応答制御と遷移制御を行う。<br>

    ※ 実行前に`APPID`を自身のものに書換えること。
    ```python
    import sys
    from PySide2 import QtCore, QtScxml
    import requests
    import json
    from datetime import datetime, timedelta, time
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
    from telegram_bot import TelegramBot

    class WeatherSystem:

        # 都道府県名のリスト
        prefs = ['三重', '京都', '佐賀', '兵庫', '北海道', '千葉', '和歌山', '埼玉', '大分',
                '大阪', '奈良', '宮城', '宮崎', '富山', '山口', '山形', '山梨', '岐阜', '岡山',
                '岩手', '島根', '広島', '徳島', '愛媛', '愛知', '新潟', '東京',
                '栃木', '沖縄', '滋賀', '熊本', '石川', '神奈川', '福井', '福岡', '福島', '秋田',
                '群馬', '茨城', '長崎', '長野', '青森', '静岡', '香川', '高知', '鳥取', '鹿児島']

        # 都道府県名から緯度と経度を取得するための辞書
        latlondic = {'北海道': (43.06, 141.35), '青森': (40.82, 140.74), '岩手': (39.7, 141.15), '宮城': (38.27, 140.87),
                    '秋田': (39.72, 140.1), '山形': (38.24, 140.36), '福島': (37.75, 140.47), '茨城': (36.34, 140.45),
                    '栃木': (36.57, 139.88), '群馬': (36.39, 139.06), '埼玉': (35.86, 139.65), '千葉': (35.61, 140.12),
                    '東京': (35.69, 139.69), '神奈川': (35.45, 139.64), '新潟': (37.9, 139.02), '富山': (36.7, 137.21),
                    '石川': (36.59, 136.63), '福井': (36.07, 136.22), '山梨': (35.66, 138.57), '長野': (36.65, 138.18),
                    '岐阜': (35.39, 136.72), '静岡': (34.98, 138.38), '愛知': (35.18, 136.91), '三重': (34.73, 136.51),
                    '滋賀': (35.0, 135.87), '京都': (35.02, 135.76), '大阪': (34.69, 135.52), '兵庫': (34.69, 135.18),
                    '奈良': (34.69, 135.83), '和歌山': (34.23, 135.17), '鳥取': (35.5, 134.24), '島根': (35.47, 133.05),
                    '岡山': (34.66, 133.93), '広島': (34.4, 132.46), '山口': (34.19, 131.47), '徳島': (34.07, 134.56),
                    '香川': (34.34, 134.04), '愛媛': (33.84, 132.77), '高知': (33.56, 133.53), '福岡': (33.61, 130.42),
                    '佐賀': (33.25, 130.3), '長崎': (32.74, 129.87), '熊本': (32.79, 130.74), '大分': (33.24, 131.61),
                    '宮崎': (31.91, 131.42), '鹿児島': (31.56, 130.56), '沖縄': (26.21, 127.68)}

        # 状態とシステム発話を紐づけた辞書
        uttdic = {"ask_place": "地名を言ってください",
                "ask_date": "日付を言ってください",
                "ask_type": "情報種別を言ってください"}

        current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
        forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
        appid = '' # 自身のAPPIDを入れてください

        def __init__(self):
            # Qtに関するおまじない
            app = QtCore.QCoreApplication()

            # 対話セッションを管理するための辞書
            self.sessiondic = {}

        # テキストから都道府県名を抽出する関数．見つからない場合は空文字を返す．
        def get_place(self, text):
            for pref in self.prefs:
                if pref in text:
                    return pref
            return ""

        # テキストに「今日」もしくは「明日」があればそれを返す．見つからない場合は空文字を返す．
        def get_date(self, text):
            if "今日" in text:
                return "今日"
            elif "明日" in text:
                return "明日"
            else:
                return ""

        # テキストに「天気」もしくは「気温」があればそれを返す．見つからない場合は空文字を返す．
        def get_type(self, text):
            if "天気" in text:
                return "天気"
            elif "気温" in text:
                return "気温"
            else:
                return ""

        def get_current_weather(self, lat,lon):
            # 天気情報を取得
            response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.current_weather_url,lat,lon,self.appid))
            return response.json()

        def get_tomorrow_weather(self, lat,lon):
            # 今日の時間を取得
            today = datetime.today()
            # 明日の時間を取得
            tomorrow = today + timedelta(days=1)
            # 明日の正午の時間を取得
            tomorrow_noon = datetime.combine(tomorrow, time(12,0))
            # UNIX時間に変換
            timestamp = tomorrow_noon.timestamp()
            # 天気情報を取得
            response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.forecast_url,lat,lon,self.appid))
            dic = response.json()
            # 3時間おきの天気情報についてループ
            for i in range(len(dic["list"])):
                # i番目の天気情報（UNIX時間）
                dt = float(dic["list"][i]["dt"])
                # 明日の正午以降のデータになった時点でその天気情報を返す
                if dt >= timestamp:
                    return dic["list"][i]
            return ""

        def initial_message(self, input):
            text = input["utt"]
            sessionId = input["sessionId"]

            self.el  = QtCore.QEventLoop()

            # SCXMLファイルの読み込み
            sm  = QtScxml.QScxmlStateMachine.fromFile('states.scxml')

            # セッションIDとセッションに関連する情報を格納した辞書
            self.sessiondic[sessionId] = {"statemachine":sm, "place":"", "date":"", "type":""}

            # 初期状態に遷移
            sm.start()
            self.el.processEvents()

            # 初期状態の取得
            current_state = sm.activeStateNames()[0]
            print("current_state=", current_state)

            # 初期状態に紐づいたシステム発話の取得と出力
            sysutt = self.uttdic[current_state]

            return {"utt":"こちらは天気情報案内システムです。" + sysutt, "end":False}

        def reply(self, input):
            text = input["utt"]
            sessionId = input["sessionId"]

            sm = self.sessiondic[sessionId]["statemachine"]
            current_state = sm.activeStateNames()[0]
            print("current_state=", current_state)

            # ユーザ入力を用いて状態遷移
            if current_state == "ask_place":
                place = self.get_place(text)
                if place != "":
                    sm.submitEvent("place")
                    self.el.processEvents()
                    self.sessiondic[sessionId]["place"] = place
            elif current_state == "ask_date":
                date = self.get_date(text)
                if date != "":
                    sm.submitEvent("date")
                    self.el.processEvents()
                    self.sessiondic[sessionId]["date"] = date
            elif current_state == "ask_type":
                _type = self.get_type(text)
                if _type != "":
                    sm.submitEvent("type")
                    self.el.processEvents()
                    self.sessiondic[sessionId]["type"] = _type

            # 遷移先の状態を取得
            current_state = sm.activeStateNames()[0]
            print("current_state=", current_state)

            # 遷移先がtell_infoの場合は情報を伝えて終了
            if current_state == "tell_info":
                utts = []
                utts.append("お伝えします")
                place = self.sessiondic[sessionId]["place"]
                date = self.sessiondic[sessionId]["date"]
                _type = self.sessiondic[sessionId]["type"]

                lat = self.latlondic[place][0] # placeから緯度を取得
                lon = self.latlondic[place][1] # placeから経度を取得
                print("lat=",lat,"lon=",lon)
                if date == "今日":
                    cw = self.get_current_weather(lat,lon)
                    if _type == "天気":
                        utts.append(cw["weather"][0]["description"]+"です")
                    elif _type == "気温":
                        utts.append(str(cw["main"]["temp"])+"度です")
                elif date == "明日":
                    tw = self.get_tomorrow_weather(lat,lon)
                    if _type == "天気":
                        utts.append(tw["weather"][0]["description"]+"です")
                    elif _type == "気温":
                        utts.append(str(tw["main"]["temp"])+"度です")
                utts.append("ご利用ありがとうございました")
                del self.sessiondic[sessionId]
                return {"utt":"。".join(utts), "end": True}

            else:
                # その他の遷移先の場合は状態に紐づいたシステム発話を生成
                sysutt = self.uttdic[current_state]
                return {"utt":sysutt, "end": False}

    if __name__ == '__main__':
        system = WeatherSystem()
        bot = TelegramBot(system)
        bot.run()
    ```

- TelegramBotクラス (telegram_bot.py)<br>
    先行記事で解説したTelegramサーバー(Bot)との通信処理。<br>
    Telegramサーバーとの通信を開始し、上記 WeatherSystemクラス(応答制御)の結果をBotに送信する。<br>
    ※ 実行前に`TOKEN`を自身のものに書換えること。

    ```python
    from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

    # アクセストークン
    TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"


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

### 状態遷移ベースの解説
以下、上記の`SCXML`, `WeatherSystem`, `TelegramBot`について実行順に解説する。

- 最初にWeatherSystemクラス (weather_system.py)を実行
  ```bash
  $ python ~/gitlocalrep/dsbook/weather_system.py
  /root/gitlocalrep/dsbook/telegram_bot.py:29: TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/fxJuV for details
    updater = Updater(TOKEN)
  ```

- WeatherSystemクラスのメイン処理で自身のインスタンスを（＊1）TelegramBotクラスのコンストラクタ（＊2）で連携後、（＊3）TelegramBotクラスの`run`メソッをコール
  ```python
  … (省略) …
  if __name__ == '__main__':
      system = WeatherSystem()
      bot = TelegramBot(system)
      bot.run()
  ```
  - （＊1）WeatherSystemクラスのコンストラクタ<br>
      QCoreApplicationでQtモジュールのメインインスタンス「app」を生成し、sessiondicを辞書型(dict)で定義する。
      ```python
      … (省略) …
          def __init__(self):
              # Qtに関するおまじない
              app = QtCore.QCoreApplication()
              # 対話セッションを管理するための辞書
              self.sessiondic = {}
      … (省略) …
      ```
  - （＊2）TelegramBotクラスのコンストラクタ<br>
      自身のsystemにWeatherSystemクラスのインスタンスを設定する。
      ```python
      … (省略) …
          def __init__(self, system):
              self.system = system
      … (省略) …
      ```
  - （＊3）TelegramBotクラスの`run`メソッド<br>
      telegramサーバー側のUpdater関数にてアクセストークンを設定後、自身のstartメソッドをコマンドハンドラとして、messageメソッドをメッセージハンドラとして設定し、コマンドハンドラとメッセージハンドラの受付を開始している。（待機状態）
      ```python
          def run(self):
              updater = Updater(TOKEN)
              dp = updater.dispatcher
              dp.add_handler(CommandHandler("start", self.start))
              dp.add_handler(MessageHandler(Filters.text, self.message))
              updater.start_polling()
              updater.idle()
      ```
- Telegramクライアントでユーザーがstartコマンドを実行<br>
  ユーザーが`/start`と入力するとTelegramサーバーがstartコマンドを発行し、上記で設定（待機）していたコマンドハンドラを受付け、startメソッドが実行される。
  startメソッドでは、まずユーザーの発話情報を保持する`input`（dict型）オブジェクトを定義し、`utt`は発話内容、`sessionId`はセッションIDを格納する。
  ※ Telegramの対話はすべて、システム側（Bot側）の発話から始まるため、`utt`は、`None`を設定し、`sessionId`には、ユーザーのセッションIDを設定している。
  ```python
  … (省略) …
      def start(self, bot, update):
          # 辞書型 inputにユーザIDを設定
          input = {'utt': None, 'sessionId': str(update.message.from_user.id)}
          … (省略) …
  ```
- `initial_message`メソッドの実行<br>
  次に`initial_message`メソッドへ、ユーザー発話情報`input`を渡し、`initial_message`メソッドでは、（＊4）のイベントループの初期設定、及び（＊5）の状態遷移の初期設定と（＊6）Botの初回発話内容を作成し返す。
  そして、戻り値の発話内容("utt")をTelegramサーバー側の`reply_text`メソッドの引数に添え、発話内容を送信する。
  - （＊4）QEventLoopメソッドにてWeatherSystemクラスのイベントループ（el : イベント待機(監視)を永続実行する仕組み）を同期に設定。
  - （＊5）SCXMLファイルの読み込み、WeatherSystemクラスにセッションID単位の状態遷移情報（place、date、type）を保持するsessiondicを定義。
  - （＊6）状態遷移を初期に設定後、初期状態の状態遷移ID（"ask_place"）の内容（"地名を言ってください"）を取得し、戻り値でuttと連結したものを返す。<br>
  （イベントループのprocessEventsでは、実行中のイベントループロック（処理が重い場合など）により、処理が止まることを回避している。）
  - `start`メソッド
      ```python
      … (省略) …
          def start(self, bot, update):
              # 辞書型 inputにユーザIDを設定
              input = {'utt': None, 'sessionId': str(update.message.from_user.id)}
              # システムからの最初の発話をinitial_messageから取得し，送信
              update.message.reply_text(self.system.initial_message(input)["utt"])
      … (省略) …
      ```
  - （＊4）〜（＊6）`initial_message`メソッド
      ```python
      … (省略) …
          def initial_message(self, input):
              text = input["utt"]
              sessionId = input["sessionId"]
              self.el  = QtCore.QEventLoop()
              # SCXMLファイルの読み込み
              sm  = QtScxml.QScxmlStateMachine.fromFile('states.scxml')
              # セッションIDとセッションに関連する情報を格納した辞書
              self.sessiondic[sessionId] = {"statemachine":sm, "place":"", "date":"", "type":""}
              # 初期状態に遷移
              sm.start()
              self.el.processEvents()
              # 初期状態の取得
              current_state = sm.activeStateNames()[0]
              print("current_state=", current_state)
              # 初期状態に紐づいたシステム発話の取得と出力
              sysutt = self.uttdic[current_state]
              return {"utt":"こちらは天気情報案内システムです。" + sysutt, "end":False}
      … (省略) …
      ```
- `message`メソッドの実行<br>
  その後、ユーザーがTelegramクライアントから発話したタイミングで上記で設定（待機）していたメッセージハンドラを受付け、messageメソッドが実行される。
  messageメソッドでは、まずユーザーの発話内容（Telegramサーバー側の text から取得したutt（発話内容））とユーザーのセッションIDでユーザー発話情報`input`を定義する。
  -  `message`メソッド
      ```python
      … (省略) …
          def message(self, bot, update):
              # 辞書型 inputにユーザからの発話とユーザIDを設定
              input = {'utt': update.message.text, 'sessionId': str(update.message.from_user.id)}
              … (省略) …
      ```
- `reply`メソッドの実行<br>
  次に`reply`メソッドへ、ユーザー発話情報`input`を渡し、`reply`メソッドにて、次の状態遷移を設定（＊7）する。
  - （＊7）現在の状態遷移を取得後、その状態遷移と応じた発話内容が有効でない場合、発話前の状態遷移に戻す。発話内容が有効である場合、遷移先を状態遷移情報（sm）に送信（submit）し、WeatherSystemクラスのsessiondicに状態遷移別の有効値を設定 →（＊8）、（＊9）、（＊10）
  - （＊8）状態遷移がask_place（地名指定）で、発話内容に「都道府県」が含まれる場合、有効値と見なし、sessiondicに設定
  - （＊9）状態遷移がask_date（日時）で、発話内容に「今日」または「明日」が含まれる場合、有効値と見なし、sessiondicに設定
  - （＊10）状態遷移がask_type（種別：天気 or 気温）で、発話内容に「天気」または「気温」が含まれる場合、有効値と見なし、sessiondicに設定<br>
    （イベントループ`el`のprocessEventsでは、実行中のイベントループロック（処理が重い場合など）により、処理が止まることを回避している。）
      -  `message`メソッド
          ```python
          … (省略) …
              def message(self, bot, update):
                  # 辞書型 inputにユーザからの発話とユーザIDを設定
                  input = {'utt': update.message.text, 'sessionId': str(update.message.from_user.id)}
                  # replyメソッドによりinputから発話を生成
                  system_output = self.system.reply(input)
                  # 発話を送信
                  update.message.reply_text(system_output["utt"])
          … (省略) …
          ```
      - （＊7）〜（＊10）`reply`メソッド
          ```python
          … (省略) …
              def reply(self, input):
                  text = input["utt"]
                  sessionId = input["sessionId"]
                  sm = self.sessiondic[sessionId]["statemachine"]
                  current_state = sm.activeStateNames()[0]
                  print("current_state=", current_state)
                  # ユーザ入力を用いて状態遷移
                  if current_state == "ask_place":
                      place = self.get_place(text)
                      if place != "":
                          sm.submitEvent("place")
                          self.el.processEvents()
                          self.sessiondic[sessionId]["place"] = place
                  elif current_state == "ask_date":
                      date = self.get_date(text)
                      if date != "":
                          sm.submitEvent("date")
                          self.el.processEvents()
                          self.sessiondic[sessionId]["date"] = date
                  elif current_state == "ask_type":
                      _type = self.get_type(text)
                      if _type != "":
                          sm.submitEvent("type")
                          self.el.processEvents()
                          self.sessiondic[sessionId]["type"] = _type
                  # 遷移先の状態を取得
                  current_state = sm.activeStateNames()[0]
                  print("current_state=", current_state)
                  … (省略) …
          ```
- 発話内容の送信<br>
  上記に続き（＊11）、（＊12）で状態遷移を設定後、発話内容を取得し、Telegramサーバー側の`reply_text`メソッドの引数に添え、発話内容を送信する。
  - （＊11）遷移先がtell_infoである場合は、（＊13）、（＊14）で天気情報を取得し、発話内容（utt）と対話完了フラグ（end）をTrue（完了）で返す。
  - （＊12）遷移先がtell_infoでない場合は、遷移先に応じた発話内容（utt）と対話完了フラグ（end）をFalse（継続）で返す。
  - （＊13）現在の天気情報取得API（http://api.openweathermap.org/data/2.5/weather）に 緯度、経度、APPID を渡し、結果をJSON形式で返す。
  - （＊14）未来の天気情報取得API（http://api.openweathermap.org/data/2.5/forecast）に 緯度、経度、APPID を渡し、明日正午頃（12時～15時までのどこか）の天気情報を抽出し、JSON形式で返す。
  - （＊11）、（＊12）`reply`メソッド
      ```python
      … (省略) …
          def reply(self, input):
              … (省略) …
              # 遷移先がtell_infoの場合は情報を伝えて終了
              if current_state == "tell_info":
                  utts = []
                  utts.append("お伝えします")
                  place = self.sessiondic[sessionId]["place"]
                  date = self.sessiondic[sessionId]["date"]
                  _type = self.sessiondic[sessionId]["type"]
                  lat = self.latlondic[place][0] # placeから緯度を取得
                  lon = self.latlondic[place][1] # placeから経度を取得
                  print("lat=",lat,"lon=",lon)
                  if date == "今日":
                      cw = self.get_current_weather(lat,lon)
                      if _type == "天気":
                          utts.append(cw["weather"][0]["description"]+"です")
                      elif _type == "気温":
                          utts.append(str(cw["main"]["temp"])+"度です")
                  elif date == "明日":
                      tw = self.get_tomorrow_weather(lat,lon)
                      if _type == "天気":
                          utts.append(tw["weather"][0]["description"]+"です")
                      elif _type == "気温":
                          utts.append(str(tw["main"]["temp"])+"度です")
                  utts.append("ご利用ありがとうございました")
                  del self.sessiondic[sessionId]
                  return {"utt":"。".join(utts), "end": True}
              else:
                  # その他の遷移先の場合は状態に紐づいたシステム発話を生成
                  sysutt = self.uttdic[current_state]
                  return {"utt":sysutt, "end": False}
      … (省略) …
      ```
  - （＊13）`get_current_weather`メソッド
      ```python
      … (省略) …
          def get_current_weather(self, lat,lon):
              # 天気情報を取得
              response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.current_weather_url,lat,lon,self.appid))
              return response.json()
      … (省略) …
      ```
  - （＊14）`get_tomorrow_weather`メソッド
      ```python
      … (省略) …
          def get_tomorrow_weather(self, lat,lon):
              # 今日の時間を取得
              today = datetime.today()
              # 明日の時間を取得
              tomorrow = today + timedelta(days=1)
              # 明日の正午の時間を取得
              tomorrow_noon = datetime.combine(tomorrow, time(12,0))
              # UNIX時間に変換
              timestamp = tomorrow_noon.timestamp()
              # 天気情報を取得
              response = requests.get("{}?lat={}&lon={}&lang=ja&units=metric&APPID={}".format(self.forecast_url,lat,lon,self.appid))
              dic = response.json()
              # 3時間おきの天気情報についてループ
              for i in range(len(dic["list"])):
                  # i番目の天気情報（UNIX時間）
                  dt = float(dic["list"][i]["dt"])
                  # 明日の正午以降のデータになった時点でその天気情報を返す
                  if dt >= timestamp:
                      return dic["list"][i]
              return ""
      … (省略) …
      ```

このように、ユーザーの入力に応じて状態遷移を制御し、天気情報や気温情報を返す対話システムが実現されている。

### 状態遷移ベースの実行確認

以下、上記の実装プログラム（＊1）〜（＊3）の実行確認。

- 最初にWeatherSystemクラス (weather_system.py)を実行
    ```bash
    $ python ~/gitlocalrep/dsbook/weather_system.py
    /root/gitlocalrep/dsbook/telegram_bot.py:29: TelegramDeprecationWarning: Old Handler API is deprecated - see https://git.io/fxJuV for details
    updater = Updater(TOKEN)
    ```

    ※ 下記の例のようなIndexErrorが発生する場合、initial_messageメソッドのfromFileでstates.scxmlの読み込みに失敗しているため、パスを通すなりフルパスを指定するなり各自の環境に合わせること。
    ```bash
    File "/var/www/vops/lib64/python3.6/site-packages/telegram/ext/dispatcher.py", line 340, in process_update
        handler.handle_update(update, self, check, context)
    File "/var/www/vops/lib64/python3.6/site-packages/telegram/ext/handler.py", line 122, in handle_update
        return self.callback(dispatcher.bot, update, **optional_args)
    File "/root/gitlocalrep/dsbook/telegram_bot.py", line 23, in message
        system_output = self.system.reply(input)
    File "/root/gitlocalrep/dsbook/weather_system.py", line 129, in reply
        current_state = sm.activeStateNames()[0]
    IndexError: list index out of range
    ```

- 続けてstartコマンドを実行<br>
    Telegramクライアントから「/start」を入力して、対話を開始する。<br>
    以降、地名、日付（今日 or 明日）、情報種別（天気 or 気温）の入力による状態遷移で天気情報を返す。

- 東京で今日（実行時となる2020/08/22 22:30分頃）の天気と気温
    ![pid41_1](/static/tblog/img/pid41_1.png)

- 福岡で明日正午頃（12時～15時までのどこか）の天気と気温
    ![pid41_2](/static/tblog/img/pid41_2.png)

今日（東京）、明日（福岡）ともに実装に沿った期待通りの結果が得られた。

### 参考文献
- 東中 竜一郎、稲葉 通将、水上 雅博（\\(2020\\)）『Pythonでつくる対話システム』株式会社オーム社

### GitHubサポートページ
- https://github.com/dsbook/dsbook
