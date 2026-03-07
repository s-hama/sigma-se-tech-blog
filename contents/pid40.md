## タイトル
Python - タスク指向型対話 : 状態遷移ベースの環境準備 > OpenWeatherMap, Telegram

## 目的
この記事では、状態遷移ベースのタスク指向型対話システムを作るために使用するOpenWeatherMapとTelegramの利用登録、python-telegram-botの使用方法（インストールと対話の実装サンプル）について記載する。

## 概要の説明と実装サンプル

### 天気情報を取得する「OpenWeatherMap」WebAPIの概要と利用登録

天気情報は、無償で天気情報を取得できる`OpenWeatherMap`のWebAPIを用いて取得する。<br>
下記トップページにアクセスすると`GUI`でも天気情報を確認することができる。

【OpenWeatherMap】: https://openweathermap.org/<br>

また、Freeプランでも毎分最大60回APIをコールでき、3時間毎の天気予報を5日後まで取得できるので学習用としては十分。<br>
そして、APIをコールするには、`API Key`が必要でアカウント作成する必要がある。

- OpenWeatherMapのアカウント作成<br>
    下記のアカウント作成ページ【Create New Account】を開き、`Username`、`Enter email`、`Password`、`Repeat password`を入力し、「Create Account」ボタンクリックでアカウントを作成する。

    【Create New Account】: https://home.openweathermap.org/users/sign_up

    アカウント作成後、ログインした状態で下記のAPIKey確認ページ【api_keys】開くと`Key`欄にAPIKeyが表示されるので、ここからAPIKeyを確認する。<br>
    ※ 登録完了のメール本文でもAPIKeyを確認できる。

    【api_keys】: https://home.openweathermap.org/api_keys

    また、PythonからURLへアクセスするため、サードパーティライブラリである`Requests`が必要。<br>
    ※ 標準ライブラリ`urllib`でもアクセスできるが、`Requests`の方がシンプルであるため、これを使用する。

- Requestsのインストール
    ```bash
    $ pip3 install requests
    ```

    以上で`OpenWeatherMap`APIを呼ぶ準備が完了。<br>
    以下、準備されている2つのAPI**現在の天気情報**と**天気予報**の呼出確認となる。

- 呼出し確認（現在の天気情報）<br>
    福岡県（県庁）の緯度、経度を指定して現在の天気情報（JSON）を取得する。<br>
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
        >>> current_weather_url = 'http://api.openweathermap.org/data/2.5/weather'
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
    上記と同じ、福岡県（県庁）の緯度、経度を指定して天気予報を取得する。<br>
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
        >>> forecast_url = 'http://api.openweathermap.org/data/2.5/forecast'
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
