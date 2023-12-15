import requests
from lxml import etree
import csv

def getWeather(url):
    weather_info = [] #新建一个列表，将爬取的每月数据放进去
    headers={
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0'
    }
    resp = requests.get(url,headers=headers)

    resp_html = etree.HTML(resp.text)
    resp_list = resp_html.xpath('//ul[@class="thrui"]/li')

    for item in resp_list:
        day_weather_info = {} # 将数据放到这个空字典里

        #日期
        day_weather_info['data_time'] = item.xpath("./div[1]/text()")[0].split(' ')[0]
        # 最高气温
        high = item.xpath("./div[2]/text()")[0]
        day_weather_info['high'] = high[:high.find('℃')]
        #最低气温
        low = item.xpath("./div[3]/text()")[0]
        day_weather_info['low'] = low[:low.find('℃')]
        #天气
        day_weather_info['weather'] = item.xpath("./div[4]/text()")[0]
        weather_info.append(day_weather_info)
    return weather_info

weathers = []

for month in range(1,13):
    weather_time = '2022' + ('0'+str(month) if month <10 else str(month))
    print(weather_time)
    url = f'https://lishi.tianqi.com/qingyuan3/{weather_time}.html'
    weather =getWeather(url)
    weathers.append(weather)
print(weathers)

with open('weather.csv','w', newline='') as cf:
    writer = csv.writer(cf)
    writer.writerow(["日期","最高气温","最低气温","天气"])
    writer.writerows([list(day_weather_dict.values()) for month_weather in weathers for day_weather_dict in month_weather])