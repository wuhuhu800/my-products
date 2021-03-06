'''
天气查询程序
'''

import os
import sys
import requests
import ast

url = "https://api.seniverse.com/v3/weather/daily.json" #知心天气API

def SearchWeather(UserInput):

    try:
        paramsdict ={'key': 'lom0ftfaihx65jh0','location':UserInput ,'language': 'zh-Hans','unit': 'c'}
        req = requests.get(url,params=paramsdict,timeout =5)
        m1= req.json()#知心天气接口返回值为str，需要转为dict
        WeatherDayDaily = m1['results'][0]['daily'][0]['text_day']#当日白天天气
        WeatherNightDaily = m1['results'][0]['daily'][0]['text_night']#当日夜晚天气
        TemperatureHighDaily = m1['results'][0]['daily'][0]['high']
        TemperatureLowDaily = m1['results'][0]['daily'][0]['low']
        WindDirectionDaily = m1['results'][0]['daily'][0]['wind_direction']
        WindScaleDaily = m1['results'][0]['daily'][0]['wind_scale']#风级
        lasttime =m1['results'][0]['last_update']#更新时间
        weather_str =f'''{UserInput}的天气为：
          白天:{WeatherDayDaily}，夜间:{WeatherNightDaily}
          最高温度:{TemperatureHighDaily}度,最低温度:{TemperatureLowDaily}度
          风向:{WindDirectionDaily},风级:{WindScaleDaily}级'''
        return weather_str

    except KeyError:
        return "该城市目前没有被收录,请重新输入"
    except ConnectionError:
        return "ConnectionError"

if __name__ == "__main__":
    UserInput = input('请输入所要查询的天气>>> ')
    SearchWeather(UserInput)
