import datetime
import schedule
import time
import tweepy
import requests
import json
import re



# 認証に必要なキーとトークン
API_KEY = 'YOURKEY'
API_SECRET = 'YOURKEY'
ACCESS_TOKEN = 'YOURKEY'
ACCESS_TOKEN_SECRET = 'YOURKEY'



# APIの認証
auth = tweepy.OAuthHandler(API_KEY, API_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)

# キーワードからツイートを取得
api = tweepy.API(auth)



def job():



  # 札幌の気象庁データの取得
  sapporo_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/016000.json"
  sapporo_json = requests.get(sapporo_url).json()
  #札幌
  sapporo = sapporo_json[0]['timeSeries'][0]['areas'][0]['weathers'][0]




  # 東京の気象庁データの取得
  tokyo_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/130000.json"
  tokyo_json = requests.get(tokyo_url).json()
  #東京
  tokyo = tokyo_json[0]['timeSeries'][0]['areas'][0]['weathers'][0]




  # 大阪の気象庁データの取得
  oosaka_url = "https://www.jma.go.jp/bosai/forecast/data/forecast/270000.json"
  oosaka_json = requests.get(oosaka_url).json()
  #大阪
  oosaka = oosaka_json[0]['timeSeries'][0]['areas'][0]['weathers'][0]




  print("おはよう" + "\n\n【東京の天気】\n" + tokyo + "\n【大阪の天気】\n" + oosaka + "\n【札幌の天気】\n" + sapporo)





  #札幌
  sapporo_url = "https://weather.tsukumijima.net/api/forecast/city/016010"

  try:
      sapporo_response = requests.get(sapporo_url)
      sapporo_response.raise_for_status()     # ステータスコード200番台以外は例外とする
  except requests.exceptions.RequestException as e:
      print("Error:{}".format(e))

  else:
    sapporo_weather = sapporo_response.json()
    #7時時点の降水確率
    sapporo_cor = sapporo_weather['forecasts'][0]['chanceOfRain']['T06_12']

  #札幌の降水確率
  rain_sapporo = "☂️ {}".format(sapporo_cor)



  #東京
  tokyo_url = "https://weather.tsukumijima.net/api/forecast/city/130010"

  try:
    tokyo_response = requests.get(tokyo_url)
    tokyo_response.raise_for_status()     # ステータスコード200番台以外は例外とする
  except requests.exceptions.RequestException as e:
    print("Error:{}".format(e))

  else:
    tokyo_weather = tokyo_response.json()
    #7時時点の降水確率
    tokyo_cor = tokyo_weather['forecasts'][0]['chanceOfRain']['T06_12']
    
  #札幌の降水確率
  rain_tokyo = "☂️ {}".format(tokyo_cor)




  #大阪
  oosaka_url = "https://weather.tsukumijima.net/api/forecast/city/270000"

  try:
    oosaka_response = requests.get(oosaka_url)
    oosaka_response.raise_for_status()     # ステータスコード200番台以外は例外とする
  except requests.exceptions.RequestException as e:
    print("Error:{}".format(e))

  else:
    oosaka_weather = oosaka_response.json()
    #7時時点の降水確率
    oosaka_cor = oosaka_weather['forecasts'][0]['chanceOfRain']['T06_12']
    
  #札幌の降水確率
  rain_oosaka = "☂️ {}".format(oosaka_cor)

  print(rain_sapporo, rain_tokyo, rain_oosaka)




  t_delta = datetime.timedelta(hours=9)
  JST = datetime.timezone(t_delta, 'JST')
  now = datetime.datetime.now(JST)

  d_week = '日月火水木金土日'  # インデックス0の'日'は使用されない
  idx = now.strftime('%u')  # '%u'では月曜日がインデックス'1'となる
  w = d_week[int(idx)]
  d = now.strftime('%Y年%m月%d日') + f'（{w}）'


  if w == "月":
   text = "もう月曜!"

  elif w == "火":
    text = "  まだ火曜〜"

  elif w == "水":
    text = "   折り返し地点！"

  elif w == "木":
    text = "   あと一踏ん張り(ᐡᴗ ̫ ᴗᐡ)"

  elif w == "金":
    text = "  金曜日🌙"

  elif w == "土":
    text = "   やっと土曜(ᐡᴗ ̫ ᴗᐡ)"

  elif w == "日":
    text = "   にちようびᕱ⑅ᕱ゛"

  def tweet():
    api.update_status("おはようございます！ 今日は" + str(d) + "❣️" + text  + "\n\n【TOKYO】\n" + tokyo + rain_tokyo.rjust(8) + "\n【OSAKA】\n" + oosaka + rain_oosaka.rjust(8)+ "\n【SAPPORO】\n" + sapporo + rain_sapporo.rjust(8))


  tweet()


schedule.every().day.at("07:20").do(job)



 
while True:
  schedule.run_pending()
  time.sleep(1)
