import practicetest
import sqlite3
import time


#以下是创建数据表
#cur.execute('''CREATE TABLE WeatherData

#            (City text NOT NULL ,WeatherDay text , WeatherNight text,
#             TemperatureHigh real , TemperatureDailylow real ,
#             WindDirection text , WindScale INTEGER ,
#             PRIMARY KEY (City)) ''')

con = sqlite3.connect('weather3.db',check_same_thread=False)#check_same_thread=False保证只有一个线程在运行
cur = con.cursor()
#

def serch_weather_db(userserch):
    #以下是传入一个用户输入的城市，为了这句话用：format(', '.join('?' for _ in city)), city
    city = [userserch]
    #以下是为了做判断空的用的
    ListForCompare =[]
    cur.execute('SELECT * FROM WeatherData WHERE City in ({0})'.format(', '.join('?' for _ in city)), city)

    # 上面这句查询语句作用就是能把一横行的数据都查出来
    row = cur.fetchall()
    #    以下if完成两件事情
    #    1、调用接口查数据
    #    2、查到数据保存在数据库里。
    if row == ListForCompare:#如果数据库里没有查询的城市的情况
        print('稍等片刻...')
        #以下是调用practicetest的函数SearchWeather的返回值
        WeatherDayDaily = practicetest.SearchWeather(userserch)[1]
        WeatherNightDaily = practicetest.SearchWeather(userserch)[2]
        TemperatureHighDaily = practicetest.SearchWeather(userserch)[3]
        TemperatureLowDaily = practicetest.SearchWeather(userserch)[4]
        WindDirectionDaily = practicetest.SearchWeather(userserch)[5]
        WindScaleDaily = practicetest.SearchWeather(userserch)[6]
        #以下是将函数返回值插入数据库
        cur.execute(
        "INSERT INTO WeatherData(City, WeatherDay,WeatherNight,TemperatureHigh,TemperatureDailylow,WindDirection,WindScale)\
         VALUES(?,?,?,?,?,?,?)",\
         (userserch,WeatherDayDaily,WeatherNightDaily,TemperatureHighDaily,TemperatureLowDaily,WindDirectionDaily,WindScaleDaily))
        cur.execute('SELECT * FROM WeatherData WHERE City in ({0})'.format(', '.join('?' for _ in city)), city)
        row1 = cur.fetchall()
        weather_strin =f'''{userserch}的天气为：
          白天:{row1[0][1]}，夜间:{row1[0][2]}
          最高温度:{row1[0][3]}度,最低温度:{row1[0][4]}度
          风向:{row1[0][5]},风级:{row1[0][6]}级'''

        return weather_strin

    #以下内容如果查询的城市在数据库里，直接显示
    else:

        weather_strin =f'''{userserch}的天气为：
          白天:{row[0][1]}，夜间:{row[0][2]}
          最高温度:{row[0][3]}度,最低温度:{row[0][4]}度
          风向:{row[0][5]},风级:{row[0][6]}级'''

        return weather_strin
    con.commit()


def update_weather(city,weather):
    cur.execute('UPDATE WeatherData SET WeatherDay = ? where City = ?',(weather,city))
    con.commit()


def auto_update():

        cur.execute('select City from WeatherData')
        try:
            for Cityi in cur.fetchall():#取出数据库的关键字进行更新
                #Cityi[0]是数据库的城市名称
                WeatherDay1 = practicetest.SearchWeather(Cityi[0])[1]
                WeatherNight1 = practicetest.SearchWeather(Cityi[0])[2]
                TemperatureHigh1 = practicetest.SearchWeather(Cityi[0])[3]
                TemperatureLow1 = practicetest.SearchWeather(Cityi[0])[4]
                WindDirection1 = practicetest.SearchWeather(Cityi[0])[5]
                WindScale1 = practicetest.SearchWeather(Cityi[0])[6]

                cur.execute('UPDATE WeatherData SET WeatherDay = ? WHERE City= ?',(WeatherDay1,Cityi[0]) )
                cur.execute('UPDATE WeatherData SET WeatherNight = ? WHERE City= ?',(WeatherNight1,Cityi[0]) )
                cur.execute('UPDATE WeatherData SET TemperatureHigh = ? WHERE City= ?',(TemperatureHigh1,Cityi[0]) )
                cur.execute('UPDATE WeatherData SET TemperatureDailylow = ? WHERE City= ?',(TemperatureLow1,Cityi[0]) )
                cur.execute('UPDATE WeatherData SET WindDirection = ? WHERE City= ?',(WindDirection1,Cityi[0]) )
                cur.execute('UPDATE WeatherData SET WindScale = ? WHERE City= ?',(WindScale1,Cityi[0]) )

                time.sleep(10)#注意参数是秒

        except sqlite3.OperationalError:
            print("database locked!!!")
        con.commit()#每次更新完之后保存
        #time.sleep(1200)#注意参数是秒
if __name__ =='__main__':
    UserInputCity = input('请输入所要查询的城市>>>')
    serch_weather_db(UserInputCity)
    auto_update()
